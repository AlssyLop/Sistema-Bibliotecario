from pydantic import BaseModel, Field


class DashboardMetricsResponse(BaseModel):
    total_estudiantes: int = Field(..., ge=0, description="Total de estudiantes registrados y activos")
    total_autores: int = Field(..., ge=0, description="Total de autores registrados y activos")
    total_libros: int = Field(..., ge=0, description="Total de libros en catálogo activos")
    total_prestamos_activos: int = Field(..., ge=0, description="Total de préstamos vigentes")
    total_devoluciones_pendientes: int = Field(..., ge=0, description="Total de préstamos vencidos sin devolución física")
