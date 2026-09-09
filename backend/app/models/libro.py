from sqlalchemy import Column, String, Integer, ForeignKey, CHAR, CheckConstraint
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from backend.app.models.base import BaseModelMixin


class Libro(Base, BaseModelMixin):
    __tablename__ = "libros"
    __table_args__ = (
        CheckConstraint("cantidad_total >= 0", name="chk_libros_total"),
        CheckConstraint("cantidad_disponible >= 0", name="chk_libros_disponible"),
    )

    isbn = Column(String(20), unique=True, nullable=False, index=True)
    titulo = Column(String(200), nullable=False, index=True)
    autor_id = Column(
        CHAR(36),
        ForeignKey("autores.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    editorial = Column(String(100), nullable=False)
    anio_publicacion = Column(Integer, nullable=False)
    categoria = Column(String(100), nullable=False, index=True)
    cantidad_total = Column(Integer, nullable=False, default=0)
    cantidad_disponible = Column(Integer, nullable=False, default=0)

    # Relaciones
    autor = relationship("Autor", back_populates="libros", lazy="joined")
    prestamos = relationship("Prestamo", back_populates="libro", lazy="selectin")
