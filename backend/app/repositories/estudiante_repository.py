from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from backend.app.models.estudiante import Estudiante
from backend.app.models.prestamo import Prestamo
from backend.app.repositories.base import BaseRepository


class EstudianteRepository(BaseRepository[Estudiante]):
    def __init__(self, db: Session):
        super().__init__(Estudiante, db)

    def get_by_documento(self, documento: str) -> Optional[Estudiante]:
        return self.db.query(Estudiante).filter(
            Estudiante.documento_identidad == documento,
            Estudiante.estado == True
        ).first()

    def get_by_correo(self, correo: str) -> Optional[Estudiante]:
        return self.db.query(Estudiante).filter(
            Estudiante.correo_institucional == correo,
            Estudiante.estado == True
        ).first()

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        search_filter = f"%{query}%"
        return self.db.query(Estudiante).filter(
            Estudiante.estado == True,
            or_(
                Estudiante.nombre_completo.ilike(search_filter),
                Estudiante.documento_identidad.ilike(search_filter),
                Estudiante.correo_institucional.ilike(search_filter),
                Estudiante.carrera.ilike(search_filter)
            )
        ).order_by(desc(Estudiante.fecha_creacion)).offset(skip).limit(limit).all()

    def has_pending_loans(self, estudiante_id: str) -> bool:
        """
        Verifica si el estudiante tiene préstamos pendientes (Activos o Atrasados).
        Requisito: no permitir eliminar o inhabilitar si tiene préstamos pendientes.
        """
        pending_count = self.db.query(Prestamo).filter(
            Prestamo.estudiante_id == estudiante_id,
            Prestamo.estado == True,
            Prestamo.estado_prestamo.in_(["Activo", "Atrasado"])
        ).count()
        return pending_count > 0
