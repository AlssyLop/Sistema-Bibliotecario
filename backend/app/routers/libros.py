from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.libro import LibroCreate, LibroUpdate, LibroResponse
from backend.app.services.libro_service import LibroService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> LibroService:
    return LibroService(db)


@router.get("", response_model=List[LibroResponse], summary="Listar catálogo o buscar libros")
def listar_libros(
    q: Optional[str] = Query(None, description="Término de búsqueda por título, ISBN, categoría o autor"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    service: LibroService = Depends(get_service)
):
    if q:
        return service.search(query=q, skip=skip, limit=limit)
    return service.get_all(skip=skip, limit=limit)


@router.get("/{libro_id}", response_model=LibroResponse, summary="Consultar libro por ID")
def obtener_libro(libro_id: str, service: LibroService = Depends(get_service)):
    return service.get_by_id(libro_id)


@router.post("", response_model=LibroResponse, status_code=status.HTTP_201_CREATED, summary="Registrar libro en catálogo")
def registrar_libro(libro_in: LibroCreate, service: LibroService = Depends(get_service)):
    return service.create(libro_in)


@router.put("/{libro_id}", response_model=LibroResponse, summary="Modificar datos o inventario del libro")
def actualizar_libro(libro_id: str, libro_in: LibroUpdate, service: LibroService = Depends(get_service)):
    return service.update(libro_id, libro_in)


@router.delete("/{libro_id}", status_code=status.HTTP_200_OK, summary="Remover libro del catálogo")
def eliminar_libro(libro_id: str, service: LibroService = Depends(get_service)):
    service.delete(libro_id)
    return {"message": "Libro removido del catálogo correctamente."}
