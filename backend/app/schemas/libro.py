from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.autor import AutorResponse


class LibroBase(BaseModel):
    isbn: str = Field(..., min_length=5, max_length=20, description="Código ISBN")
    titulo: str = Field(..., min_length=1, max_length=200, description="Título de la obra")
    editorial: str = Field(..., min_length=2, max_length=100, description="Sello editorial")
    anio_publicacion: int = Field(..., ge=1000, le=2100, description="Año de publicación")
    categoria: str = Field(..., min_length=2, max_length=100, description="Categoría o género literario")
    cantidad_total: int = Field(..., ge=0, description="Inventario total")


class LibroCreate(LibroBase):
    autor_id: str = Field(..., min_length=36, max_length=36, description="UUID del autor")
    cantidad_disponible: Optional[int] = Field(None, ge=0, description="Ejemplares disponibles inicialmente")


class LibroUpdate(BaseModel):
    isbn: Optional[str] = Field(None, min_length=5, max_length=20)
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    autor_id: Optional[str] = Field(None, min_length=36, max_length=36)
    editorial: Optional[str] = Field(None, min_length=2, max_length=100)
    anio_publicacion: Optional[int] = Field(None, ge=1000, le=2100)
    categoria: Optional[str] = Field(None, min_length=2, max_length=100)
    cantidad_total: Optional[int] = Field(None, ge=0)
    cantidad_disponible: Optional[int] = Field(None, ge=0)
    estado: Optional[bool] = None


class LibroResponse(LibroBase):
    id: str
    autor_id: str
    cantidad_disponible: int
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    autor: Optional[AutorResponse] = None

    model_config = ConfigDict(from_attributes=True)
