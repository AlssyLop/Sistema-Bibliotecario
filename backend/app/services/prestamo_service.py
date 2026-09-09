from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models.prestamo import Prestamo
from backend.app.schemas.prestamo import PrestamoCreate, PrestamoDevolucion
from backend.app.repositories.prestamo_repository import PrestamoRepository
from backend.app.repositories.estudiante_repository import EstudianteRepository
from backend.app.repositories.libro_repository import LibroRepository


class PrestamoService:
    def __init__(self, db: Session):
        self.repository = PrestamoRepository(db)
        self.estudiante_repo = EstudianteRepository(db)
        self.libro_repo = LibroRepository(db)

    def get_by_id(self, prestamo_id: str) -> Prestamo:
        prestamo = self.repository.get_by_id(prestamo_id)
        if not prestamo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Préstamo con ID '{prestamo_id}' no encontrado."
            )
        return prestamo

    def get_activos(self, skip: int = 0, limit: int = 100) -> List[Prestamo]:
        return self.repository.get_activos(skip=skip, limit=limit)

    def get_pendientes_devolucion(self, skip: int = 0, limit: int = 100) -> List[Prestamo]:
        return self.repository.get_pendientes_devolucion(skip=skip, limit=limit)

    def search(
        self,
        query: Optional[str] = None,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        estado_prestamo: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Prestamo]:
        return self.repository.search(
            query=query,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado_prestamo=estado_prestamo,
            skip=skip,
            limit=limit
        )

    def crear_prestamo(self, prestamo_in: PrestamoCreate) -> Prestamo:
        # 1. Validar que el estudiante exista y esté activo
        estudiante = self.estudiante_repo.get_by_id(prestamo_in.estudiante_id)
        if not estudiante or not estudiante.estado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estudiante no existe o se encuentra inactivo/inhabilitado para préstamos."
            )

        # 2. Validar que el libro exista y esté activo
        libro = self.libro_repo.get_by_id(prestamo_in.libro_id)
        if not libro or not libro.estado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El libro no existe o fue dado de baja del catálogo."
            )

        # 3. Validar disponibilidad de stock físico
        if libro.cantidad_disponible <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No hay ejemplares disponibles en estantería para el libro '{libro.titulo}'."
            )

        # 4. Validar coherencia de fechas
        fecha_salida = prestamo_in.fecha_salida or datetime.now()
        if prestamo_in.fecha_pactada <= fecha_salida:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha pactada de devolución debe ser posterior a la fecha de salida del ejemplar."
            )

        # 5. Decrementar stock disponible del libro
        self.libro_repo.adjust_stock(libro.id, delta=-1)

        # 6. Registrar la transacción de préstamo
        datos = prestamo_in.model_dump()
        datos["fecha_salida"] = fecha_salida
        datos["estado_prestamo"] = "Activo"
        datos["fecha_real"] = None

        return self.repository.create(datos)

    def registrar_devolucion(self, prestamo_id: str, devolucion_in: Optional[PrestamoDevolucion] = None) -> Prestamo:
        prestamo = self.get_by_id(prestamo_id)

        # Validar que no haya sido devuelto con anterioridad
        if prestamo.estado_prestamo == "Devuelto":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este préstamo ya fue devuelto previamente."
            )

        # 1. Establecer fecha real de devolución
        fecha_real = (devolucion_in.fecha_real if devolucion_in and devolucion_in.fecha_real else datetime.now())
        prestamo.fecha_real = fecha_real
        prestamo.estado_prestamo = "Devuelto"

        # 2. Reingresar el ejemplar a los disponibles (+1)
        self.libro_repo.adjust_stock(prestamo.libro_id, delta=+1)

        self.repository.db.commit()
        self.repository.db.refresh(prestamo)
        return prestamo
