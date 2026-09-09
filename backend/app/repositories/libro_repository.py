from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from backend.app.models.libro import Libro
from backend.app.models.autor import Autor
from backend.app.models.prestamo import Prestamo
from backend.app.repositories.base import BaseRepository


class LibroRepository(BaseRepository[Libro]):
    def __init__(self, db: Session):
        super().__init__(Libro, db)

    def get_by_isbn(self, isbn: str) -> Optional[Libro]:
        return self.db.query(Libro).filter(
            Libro.isbn == isbn,
            Libro.estado == True
        ).first()

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Libro]:
        search_filter = f"%{query}%"
        return self.db.query(Libro).outerjoin(Autor, Libro.autor_id == Autor.id).filter(
            Libro.estado == True,
            or_(
                Libro.titulo.ilike(search_filter),
                Libro.isbn.ilike(search_filter),
                Libro.categoria.ilike(search_filter),
                Libro.editorial.ilike(search_filter),
                Autor.nombre_completo.ilike(search_filter)
            )
        ).order_by(desc(Libro.fecha_creacion)).offset(skip).limit(limit).all()

    def has_active_loans(self, libro_id: str) -> bool:
        """
        Verifica si el libro tiene préstamos activos o atrasados.
        Requisito: no permitir eliminar libro del catálogo si tiene préstamos activos.
        """
        count = self.db.query(Prestamo).filter(
            Prestamo.libro_id == libro_id,
            Prestamo.estado == True,
            Prestamo.estado_prestamo.in_(["Activo", "Atrasado"])
        ).count()
        return count > 0

    def adjust_stock(self, libro_id: str, delta: int) -> Optional[Libro]:
        """
        Ajusta la cantidad disponible (+1 al devolver, -1 al prestar).
        """
        libro = self.get_by_id(libro_id, only_active=True)
        if not libro:
            return None
        nuevo_stock = libro.cantidad_disponible + delta
        if nuevo_stock < 0 or nuevo_stock > libro.cantidad_total:
            raise ValueError(f"Stock inválido ({nuevo_stock}) para el libro con total {libro.cantidad_total}")
        libro.cantidad_disponible = nuevo_stock
        self.db.commit()
        self.db.refresh(libro)
        return libro
