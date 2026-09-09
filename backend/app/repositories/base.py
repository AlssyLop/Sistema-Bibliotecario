from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from backend.app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Repositorio genérico con operaciones CRUD estándar para SQLAlchemy:
    - Bajas lógicas (Soft Delete) automáticas.
    - Ordenamiento descendente predeterminado por fecha de creación.
    """

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: str, only_active: bool = True) -> Optional[ModelType]:
        query = self.db.query(self.model).filter(self.model.id == id)
        if only_active and hasattr(self.model, "estado"):
            query = query.filter(self.model.estado == True)
        return query.first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True,
        order_desc: bool = True
    ) -> List[ModelType]:
        query = self.db.query(self.model)
        if only_active and hasattr(self.model, "estado"):
            query = query.filter(self.model.estado == True)
        if order_desc and hasattr(self.model, "fecha_creacion"):
            query = query.order_by(desc(self.model.fecha_creacion))
        return query.offset(skip).limit(limit).all()

    def count(self, only_active: bool = True) -> int:
        query = self.db.query(self.model)
        if only_active and hasattr(self.model, "estado"):
            query = query.filter(self.model.estado == True)
        return query.count()

    def create(self, obj_in: Any) -> ModelType:
        if isinstance(obj_in, BaseModel):
            obj_data = obj_in.model_dump()
        elif isinstance(obj_in, dict):
            obj_data = obj_in
        else:
            obj_data = obj_in.__dict__
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, obj_in: Any) -> ModelType:
        if isinstance(obj_in, BaseModel):
            update_data = obj_in.model_dump(exclude_unset=True)
        elif isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.__dict__

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def soft_delete(self, id: str) -> bool:
        db_obj = self.get_by_id(id, only_active=False)
        if not db_obj:
            return False
        if hasattr(db_obj, "estado"):
            db_obj.estado = False
            self.db.commit()
            return True
        return False
