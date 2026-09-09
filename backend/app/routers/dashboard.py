from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.dashboard import DashboardMetricsResponse
from backend.app.services.dashboard_service import DashboardService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(db)


@router.get("/metrics", response_model=DashboardMetricsResponse, summary="Obtener tarjetas métricas del Dashboard")
def obtener_metricas(service: DashboardService = Depends(get_service)):
    """
    Retorna el total de estudiantes, autores, libros, préstamos activos y devoluciones pendientes
    para visualización en las tarjetas del panel principal.
    """
    return service.get_metrics()
