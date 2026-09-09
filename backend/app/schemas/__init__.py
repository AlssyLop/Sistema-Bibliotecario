from backend.app.schemas.autor import AutorBase, AutorCreate, AutorUpdate, AutorResponse
from backend.app.schemas.estudiante import EstudianteBase, EstudianteCreate, EstudianteUpdate, EstudianteResponse
from backend.app.schemas.libro import LibroBase, LibroCreate, LibroUpdate, LibroResponse
from backend.app.schemas.prestamo import PrestamoCreate, PrestamoDevolucion, PrestamoResponse
from backend.app.schemas.dashboard import DashboardMetricsResponse

__all__ = [
    "AutorBase", "AutorCreate", "AutorUpdate", "AutorResponse",
    "EstudianteBase", "EstudianteCreate", "EstudianteUpdate", "EstudianteResponse",
    "LibroBase", "LibroCreate", "LibroUpdate", "LibroResponse",
    "PrestamoCreate", "PrestamoDevolucion", "PrestamoResponse",
    "DashboardMetricsResponse",
]
