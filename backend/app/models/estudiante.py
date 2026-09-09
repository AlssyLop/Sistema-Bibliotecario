from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from backend.app.models.base import BaseModelMixin


class Estudiante(Base, BaseModelMixin):
    __tablename__ = "estudiantes"

    documento_identidad = Column(String(50), unique=True, nullable=False, index=True)
    nombre_completo = Column(String(150), nullable=False, index=True)
    correo_institucional = Column(String(100), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)
    carrera = Column(String(100), nullable=False, index=True)

    # Relación uno a muchos con préstamos
    prestamos = relationship("Prestamo", back_populates="estudiante", lazy="selectin")
