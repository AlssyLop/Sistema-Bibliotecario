from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models.autor import Autor
from backend.app.schemas.autor import AutorCreate, AutorUpdate
from backend.app.repositories.autor_repository import AutorRepository


class AutorService:
    def __init__(self, db: Session):
        self.repository = AutorRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Autor]:
        return self.repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, autor_id: str) -> Autor:
        autor = self.repository.get_by_id(autor_id)
        if not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Autor con ID '{autor_id}' no encontrado."
            )
        return autor

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Autor]:
        return self.repository.search(query=query, skip=skip, limit=limit)

    def create(self, autor_in: AutorCreate) -> Autor:
        # Validación de documento de identidad único
        if self.repository.get_by_documento(autor_in.documento_identidad):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un autor con el documento '{autor_in.documento_identidad}'."
            )
        # Validación de correo único si fue provisto
        if autor_in.correo and self.repository.get_by_correo(autor_in.correo):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un autor registrado con el correo '{autor_in.correo}'."
            )
        return self.repository.create(autor_in)

    def update(self, autor_id: str, autor_in: AutorUpdate) -> Autor:
        autor = self.get_by_id(autor_id)
        # Validar duplicados si se actualiza el documento
        if autor_in.documento_identidad and autor_in.documento_identidad != autor.documento_identidad:
            existente = self.repository.get_by_documento(autor_in.documento_identidad)
            if existente and existente.id != autor_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro autor con el documento '{autor_in.documento_identidad}'."
                )
        # Validar duplicados si se actualiza el correo
        if autor_in.correo and autor_in.correo != autor.correo:
            existente = self.repository.get_by_correo(autor_in.correo)
            if existente and existente.id != autor_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro autor con el correo '{autor_in.correo}'."
                )
        return self.repository.update(autor, autor_in)

    def delete(self, autor_id: str) -> None:
        autor = self.get_by_id(autor_id)
        # Regla de negocio: Dar de baja siempre que no tenga libros asociados con préstamos activos
        if self.repository.has_active_loans(autor_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar el autor: tiene libros asociados con préstamos activos o pendientes."
            )
        self.repository.soft_delete(autor_id)
