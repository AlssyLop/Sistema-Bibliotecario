from sqlalchemy.orm import Session
from backend.app.schemas.dashboard import DashboardMetricsResponse
from backend.app.repositories.estudiante_repository import EstudianteRepository
from backend.app.repositories.autor_repository import AutorRepository
from backend.app.repositories.libro_repository import LibroRepository
from backend.app.repositories.prestamo_repository import PrestamoRepository


class DashboardService:
    def __init__(self, db: Session):
        self.estudiante_repo = EstudianteRepository(db)
        self.autor_repo = AutorRepository(db)
        self.libro_repo = LibroRepository(db)
        self.prestamo_repo = PrestamoRepository(db)

    def get_metrics(self) -> DashboardMetricsResponse:
        return DashboardMetricsResponse(
            total_estudiantes=self.estudiante_repo.count(only_active=True),
            total_autores=self.autor_repo.count(only_active=True),
            total_libros=self.libro_repo.count(only_active=True),
            total_prestamos_activos=self.prestamo_repo.count_activos(),
            total_devoluciones_pendientes=self.prestamo_repo.count_pendientes_devolucion()
        )
