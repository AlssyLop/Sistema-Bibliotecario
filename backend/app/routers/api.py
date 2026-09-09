from fastapi import APIRouter
from backend.app.routers import dashboard, autores, estudiantes, libros, prestamos

api_router = APIRouter()

api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(autores.router, prefix="/autores", tags=["Autores"])
api_router.include_router(estudiantes.router, prefix="/estudiantes", tags=["Estudiantes"])
api_router.include_router(libros.router, prefix="/libros", tags=["Libros"])
api_router.include_router(prestamos.router, prefix="/prestamos", tags=["Préstamos"])
