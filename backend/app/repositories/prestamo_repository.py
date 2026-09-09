from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from backend.app.models.prestamo import Prestamo
from backend.app.models.estudiante import Estudiante
from backend.app.models.libro import Libro
from backend.app.repositories.base import BaseRepository


class PrestamoRepository(BaseRepository[Prestamo]):
    def __init__(self, db: Session):
        super().__init__(Prestamo, db)

    def get_activos(self, skip: int = 0, limit: int = 100) -> List[Prestamo]:
        """
        Pestaña Préstamos Activos: Listar únicamente los préstamos vigentes.
        """
        return (
            self.db.query(Prestamo)
            .filter(
                Prestamo.estado == True,
                Prestamo.estado_prestamo == "Activo"
            )
            .order_by(desc(Prestamo.fecha_salida))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_pendientes_devolucion(self, skip: int = 0, limit: int = 100) -> List[Prestamo]:
        """
        Pestaña Devoluciones Pendientes: Listar los préstamos cuya fecha pactada
        ha vencido o están en estado 'Atrasado' y aún no registran retorno físico.
        """
        ahora = datetime.now()
        return (
            self.db.query(Prestamo)
            .filter(
                Prestamo.estado == True,
                Prestamo.fecha_real.is_(None),
                or_(
                    Prestamo.estado_prestamo == "Atrasado",
                    (Prestamo.estado_prestamo == "Activo") & (Prestamo.fecha_pactada < ahora)
                )
            )
            .order_by(Prestamo.fecha_pactada.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
        self,
        query: Optional[str] = None,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        estado_prestamo: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Prestamo]:
        q = (
            self.db.query(Prestamo)
            .outerjoin(Estudiante, Prestamo.estudiante_id == Estudiante.id)
            .outerjoin(Libro, Prestamo.libro_id == Libro.id)
            .filter(Prestamo.estado == True)
        )

        if query:
            search_filter = f"%{query}%"
            q = q.filter(
                or_(
                    Estudiante.nombre_completo.ilike(search_filter),
                    Estudiante.documento_identidad.ilike(search_filter),
                    Libro.titulo.ilike(search_filter),
                    Libro.isbn.ilike(search_filter)
                )
            )

        if fecha_inicio:
            q = q.filter(Prestamo.fecha_salida >= fecha_inicio)

        if fecha_fin:
            q = q.filter(Prestamo.fecha_salida <= fecha_fin)

        if estado_prestamo:
            q = q.filter(Prestamo.estado_prestamo == estado_prestamo)

        return q.order_by(desc(Prestamo.fecha_salida)).offset(skip).limit(limit).all()

    def count_activos(self) -> int:
        return self.db.query(Prestamo).filter(
            Prestamo.estado == True,
            Prestamo.estado_prestamo == "Activo"
        ).count()

    def count_pendientes_devolucion(self) -> int:
        ahora = datetime.now()
        return self.db.query(Prestamo).filter(
            Prestamo.estado == True,
            Prestamo.fecha_real.is_(None),
            or_(
                Prestamo.estado_prestamo == "Atrasado",
                (Prestamo.estado_prestamo == "Activo") & (Prestamo.fecha_pactada < ahora)
            )
        ).count()
