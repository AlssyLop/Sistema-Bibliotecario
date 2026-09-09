from backend.app.repositories.base import BaseRepository
from backend.app.repositories.autor_repository import AutorRepository
from backend.app.repositories.estudiante_repository import EstudianteRepository
from backend.app.repositories.libro_repository import LibroRepository
from backend.app.repositories.prestamo_repository import PrestamoRepository

__all__ = [
    "BaseRepository",
    "AutorRepository",
    "EstudianteRepository",
    "LibroRepository",
    "PrestamoRepository",
]
