import uuid
from sqlalchemy import Column, String, Boolean, DateTime, CHAR
from sqlalchemy.sql import func
from backend.app.core.database import Base


class BaseModelMixin:
    """
    Mixin con atributos universales para todas las entidades del dominio:
    - Identificador global UUID (CHAR(36)).
    - Control de baja lógica (estado booleano).
    - Marcas temporales de auditoría automáticas (fecha_creacion y fecha_actualizacion).
    """
    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False
    )
    estado = Column(
        Boolean,
        default=True,
        nullable=False
    )
    fecha_creacion = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    fecha_actualizacion = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
