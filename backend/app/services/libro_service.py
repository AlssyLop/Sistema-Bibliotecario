from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models.libro import Libro
from backend.app.schemas.libro import LibroCreate, LibroUpdate
from backend.app.repositories.libro_repository import LibroRepository
from backend.app.repositories.autor_repository import AutorRepository


class LibroService:
    def __init__(self, db: Session):
        self.repository = LibroRepository(db)
        self.autor_repo = AutorRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Libro]:
        return self.repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, libro_id: str) -> Libro:
        libro = self.repository.get_by_id(libro_id)
        if not libro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Libro con ID '{libro_id}' no encontrado."
            )
        return libro

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Libro]:
        return self.repository.search(query=query, skip=skip, limit=limit)

    def create(self, libro_in: LibroCreate) -> Libro:
        # Verificar que el autor existe y está activo
        autor = self.autor_repo.get_by_id(libro_in.autor_id)
        if not autor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El autor con ID '{libro_in.autor_id}' no existe o se encuentra inactivo."
            )
        # Verificar unicidad del ISBN
        if self.repository.get_by_isbn(libro_in.isbn):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un libro registrado con el ISBN '{libro_in.isbn}'."
            )

        # Si no se define cantidad disponible, por defecto es igual a la total
        datos = libro_in.model_dump()
        if datos.get("cantidad_disponible") is None:
            datos["cantidad_disponible"] = datos["cantidad_total"]

        if datos["cantidad_disponible"] > datos["cantidad_total"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cantidad disponible no puede exceder el inventario total adquirido."
            )

        return self.repository.create(datos)

    def update(self, libro_id: str, libro_in: LibroUpdate) -> Libro:
        libro = self.get_by_id(libro_id)

        # Si se actualiza el autor, verificar que exista
        if libro_in.autor_id and libro_in.autor_id != libro.autor_id:
            autor = self.autor_repo.get_by_id(libro_in.autor_id)
            if not autor:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El autor con ID '{libro_in.autor_id}' no existe o se encuentra inactivo."
                )

        # Si se actualiza el ISBN, verificar duplicado
        if libro_in.isbn and libro_in.isbn != libro.isbn:
            existente = self.repository.get_by_isbn(libro_in.isbn)
            if existente and existente.id != libro_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro libro con el ISBN '{libro_in.isbn}'."
                )

        # Validar coherencia de inventarios
        nueva_total = libro_in.cantidad_total if libro_in.cantidad_total is not None else libro.cantidad_total
        nueva_disp = libro_in.cantidad_disponible if libro_in.cantidad_disponible is not None else libro.cantidad_disponible
        if nueva_disp > nueva_total:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cantidad disponible no puede superar la cantidad total."
            )

        return self.repository.update(libro, libro_in)

    def delete(self, libro_id: str) -> None:
        libro = self.get_by_id(libro_id)
        # Regla de negocio: Restringido si tiene préstamos activos
        if self.repository.has_active_loans(libro_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar el libro del catálogo: tiene préstamos activos vigentes o atrasados."
            )
        self.repository.soft_delete(libro_id)
