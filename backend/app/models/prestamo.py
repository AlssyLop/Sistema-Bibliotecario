from sqlalchemy import Column, DateTime, ForeignKey, CHAR, Enum
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from backend.app.models.base import BaseModelMixin


class Prestamo(Base, BaseModelMixin):
    __tablename__ = "prestamos"

    estudiante_id = Column(
        CHAR(36),
        ForeignKey("estudiantes.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    libro_id = Column(
        CHAR(36),
        ForeignKey("libros.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    fecha_salida = Column(DateTime, nullable=False)
    fecha_pactada = Column(DateTime, nullable=False)
    fecha_real = Column(DateTime, nullable=True)
    estado_prestamo = Column(
        Enum("Activo", "Devuelto", "Atrasado", name="estado_prestamo_enum"),
        nullable=False,
        default="Activo",
        index=True
    )

    # Relaciones
    estudiante = relationship("Estudiante", back_populates="prestamos", lazy="joined")
    libro = relationship("Libro", back_populates="prestamos", lazy="joined")
