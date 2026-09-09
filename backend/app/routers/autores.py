from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.autor import AutorCreate, AutorUpdate, AutorResponse
from backend.app.services.autor_service import AutorService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> AutorService:
    return AutorService(db)


@router.get("", response_model=List[AutorResponse], summary="Listar o buscar autores")
def listar_autores(
    q: Optional[str] = Query(None, description="Término de búsqueda por nombre o documento"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    service: AutorService = Depends(get_service)
):
    if q:
        return service.search(query=q, skip=skip, limit=limit)
    return service.get_all(skip=skip, limit=limit)


@router.get("/{autor_id}", response_model=AutorResponse, summary="Consultar autor por ID")
def obtener_autor(autor_id: str, service: AutorService = Depends(get_service)):
    return service.get_by_id(autor_id)


@router.post("", response_model=AutorResponse, status_code=status.HTTP_201_CREATED, summary="Registrar autor")
def registrar_autor(autor_in: AutorCreate, service: AutorService = Depends(get_service)):
    return service.create(autor_in)


@router.put("/{autor_id}", response_model=AutorResponse, summary="Actualizar información de autor")
def actualizar_autor(autor_id: str, autor_in: AutorUpdate, service: AutorService = Depends(get_service)):
    return service.update(autor_id, autor_in)


@router.delete("/{autor_id}", status_code=status.HTTP_200_OK, summary="Dar de baja autor")
def eliminar_autor(autor_id: str, service: AutorService = Depends(get_service)):
    service.delete(autor_id)
    return {"message": "Autor dado de baja correctamente del sistema."}
