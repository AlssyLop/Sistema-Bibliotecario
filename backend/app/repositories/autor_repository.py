from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from backend.app.models.autor import Autor
from backend.app.models.libro import Libro
from backend.app.models.prestamo import Prestamo
from backend.app.repositories.base import BaseRepository


class AutorRepository(BaseRepository[Autor]):
    def __init__(self, db: Session):
        super().__init__(Autor, db)

    def get_by_documento(self, documento: str) -> Optional[Autor]:
        return self.db.query(Autor).filter(
            Autor.documento_identidad == documento,
            Autor.estado == True
        ).first()

    def get_by_correo(self, correo: str) -> Optional[Autor]:
        return self.db.query(Autor).filter(
            Autor.correo == correo,
            Autor.estado == True
        ).first()

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Autor]:
        search_filter = f"%{query}%"
        return self.db.query(Autor).filter(
            Autor.estado == True,
            or_(
                Autor.nombre_completo.ilike(search_filter),
                Autor.documento_identidad.ilike(search_filter),
                Autor.correo.ilike(search_filter)
            )
        ).order_by(desc(Autor.fecha_creacion)).offset(skip).limit(limit).all()

    def has_active_loans(self, autor_id: str) -> bool:
        """
        Verifica si el autor tiene libros asociados que actualmente tengan préstamos activos o atrasados.
        Requisito: no permitir eliminar si tiene libros con préstamos activos.
        """
        active_loans_count = (
            self.db.query(Prestamo)
            .join(Libro, Prestamo.libro_id == Libro.id)
            .filter(
                Libro.autor_id == autor_id,
                Prestamo.estado == True,
                Prestamo.estado_prestamo.in_(["Activo", "Atrasado"])
            )
            .count()
        )
        return active_loans_count > 0
