from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.prestamo import PrestamoCreate, PrestamoDevolucion, PrestamoResponse
from backend.app.services.prestamo_service import PrestamoService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> PrestamoService:
    return PrestamoService(db)


@router.get("/activos", response_model=List[PrestamoResponse], summary="Pestaña Préstamos Activos")
def listar_prestamos_activos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    service: PrestamoService = Depends(get_service)
):
    """
    Listar únicamente los préstamos vigentes con sus respectivos datos de vencimiento.
    """
    return service.get_activos(skip=skip, limit=limit)


@router.get("/pendientes", response_model=List[PrestamoResponse], summary="Pestaña Devoluciones Pendientes")
def listar_devoluciones_pendientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    service: PrestamoService = Depends(get_service)
):
    """
    Listar los préstamos cuya fecha pactada ha vencido o están atrasados y aún no registran retorno.
    """
    return service.get_pendientes_devolucion(skip=skip, limit=limit)


@router.get("", response_model=List[PrestamoResponse], summary="Historial general de préstamos y consultas")
def consultar_prestamos(
    q: Optional[str] = Query(None, description="Buscar por estudiante (nombre/documento) o libro (título/ISBN)"),
    fecha_inicio: Optional[datetime] = Query(None, description="Filtrar por fecha de salida desde"),
    fecha_fin: Optional[datetime] = Query(None, description="Filtrar por fecha de salida hasta"),
    estado_prestamo: Optional[str] = Query(None, description="Filtrar por estado: 'Activo', 'Devuelto', 'Atrasado'"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    service: PrestamoService = Depends(get_service)
):
    return service.search(
        query=q,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado_prestamo=estado_prestamo,
        skip=skip,
        limit=limit
    )


@router.get("/{prestamo_id}", response_model=PrestamoResponse, summary="Consultar préstamo por ID")
def obtener_prestamo(prestamo_id: str, service: PrestamoService = Depends(get_service)):
    return service.get_by_id(prestamo_id)


@router.post("", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED, summary="Registrar nuevo préstamo")
def registrar_prestamo(prestamo_in: PrestamoCreate, service: PrestamoService = Depends(get_service)):
    """
    Asigna un libro disponible a un estudiante activo, decrementando los ejemplares disponibles.
    """
    return service.crear_prestamo(prestamo_in)


@router.post("/{prestamo_id}/devolucion", response_model=PrestamoResponse, summary="Registrar devolución física del libro")
def registrar_devolucion(
    prestamo_id: str,
    devolucion_in: Optional[PrestamoDevolucion] = None,
    service: PrestamoService = Depends(get_service)
):
    """
    Finaliza el préstamo, actualizando la fecha real de retorno y reponiendo el inventario del libro.
    """
    return service.registrar_devolucion(prestamo_id, devolucion_in)
