from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models.estudiante import Estudiante
from backend.app.schemas.estudiante import EstudianteCreate, EstudianteUpdate
from backend.app.repositories.estudiante_repository import EstudianteRepository


class EstudianteService:
    def __init__(self, db: Session):
        self.repository = EstudianteRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        return self.repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, estudiante_id: str) -> Estudiante:
        estudiante = self.repository.get_by_id(estudiante_id)
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID '{estudiante_id}' no encontrado."
            )
        return estudiante

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        return self.repository.search(query=query, skip=skip, limit=limit)

    def create(self, estudiante_in: EstudianteCreate) -> Estudiante:
        # Validación de documento de identidad único
        if self.repository.get_by_documento(estudiante_in.documento_identidad):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un estudiante con el documento '{estudiante_in.documento_identidad}'."
            )
        # Validación de correo institucional único
        if self.repository.get_by_correo(estudiante_in.correo_institucional):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El correo institucional '{estudiante_in.correo_institucional}' ya se encuentra registrado."
            )
        return self.repository.create(estudiante_in)

    def update(self, estudiante_id: str, estudiante_in: EstudianteUpdate) -> Estudiante:
        estudiante = self.get_by_id(estudiante_id)
        if estudiante_in.documento_identidad and estudiante_in.documento_identidad != estudiante.documento_identidad:
            existente = self.repository.get_by_documento(estudiante_in.documento_identidad)
            if existente and existente.id != estudiante_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro estudiante con el documento '{estudiante_in.documento_identidad}'."
                )
        if estudiante_in.correo_institucional and estudiante_in.correo_institucional != estudiante.correo_institucional:
            existente = self.repository.get_by_correo(estudiante_in.correo_institucional)
            if existente and existente.id != estudiante_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El correo '{estudiante_in.correo_institucional}' ya pertenece a otro estudiante."
                )
        # Si se desea inhabilitar (estado=False), verificar préstamos
        if estudiante_in.estado is False and self.repository.has_pending_loans(estudiante_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede inhabilitar al estudiante: registra préstamos activos o atrasados pendientes de devolución."
            )
        return self.repository.update(estudiante, estudiante_in)

    def delete(self, estudiante_id: str) -> None:
        estudiante = self.get_by_id(estudiante_id)
        # Regla de negocio: No eliminar si tiene préstamos pendientes
        if self.repository.has_pending_loans(estudiante_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar al estudiante: cuenta con préstamos pendientes de devolución."
            )
        self.repository.soft_delete(estudiante_id)
