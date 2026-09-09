from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from backend.app.models.base import BaseModelMixin


class Autor(Base, BaseModelMixin):
    __tablename__ = "autores"

    documento_identidad = Column(String(50), unique=True, nullable=False, index=True)
    nombre_completo = Column(String(150), nullable=False, index=True)
    correo = Column(String(100), unique=True, nullable=True)
    telefono = Column(String(20), nullable=True)

    # Relación uno a muchos con libros
    libros = relationship("Libro", back_populates="autor", lazy="selectin")
