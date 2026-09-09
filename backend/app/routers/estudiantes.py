from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.estudiante import EstudianteCreate, EstudianteUpdate, EstudianteResponse
from backend.app.services.estudiante_service import EstudianteService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> EstudianteService:
    return EstudianteService(db)


@router.get("", response_model=List[EstudianteResponse], summary="Listar o buscar estudiantes")
def listar_estudiantes(
    q: Optional[str] = Query(None, description="Término de búsqueda por nombre, documento o correo"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    service: EstudianteService = Depends(get_service)
):
    if q:
        return service.search(query=q, skip=skip, limit=limit)
    return service.get_all(skip=skip, limit=limit)


@router.get("/{estudiante_id}", response_model=EstudianteResponse, summary="Consultar estudiante por ID")
def obtener_estudiante(estudiante_id: str, service: EstudianteService = Depends(get_service)):
    return service.get_by_id(estudiante_id)


@router.post("", response_model=EstudianteResponse, status_code=status.HTTP_201_CREATED, summary="Registrar estudiante")
def registrar_estudiante(estudiante_in: EstudianteCreate, service: EstudianteService = Depends(get_service)):
    return service.create(estudiante_in)


@router.put("/{estudiante_id}", response_model=EstudianteResponse, summary="Actualizar datos del estudiante")
def actualizar_estudiante(estudiante_id: str, estudiante_in: EstudianteUpdate, service: EstudianteService = Depends(get_service)):
    return service.update(estudiante_id, estudiante_in)


@router.delete("/{estudiante_id}", status_code=status.HTTP_200_OK, summary="Inhabilitar o remover estudiante")
def eliminar_estudiante(estudiante_id: str, service: EstudianteService = Depends(get_service)):
    service.delete(estudiante_id)
    return {"message": "Estudiante inhabilitado/removido correctamente del sistema."}
