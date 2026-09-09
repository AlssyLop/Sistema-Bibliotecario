from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.estudiante import EstudianteResponse
from backend.app.schemas.libro import LibroResponse


class PrestamoCreate(BaseModel):
    estudiante_id: str = Field(..., min_length=36, max_length=36, description="UUID del estudiante")
    libro_id: str = Field(..., min_length=36, max_length=36, description="UUID del libro")
    fecha_salida: Optional[datetime] = Field(None, description="Fecha de entrega física (por defecto ahora)")
    fecha_pactada: datetime = Field(..., description="Fecha límite de entrega pactada")


class PrestamoDevolucion(BaseModel):
    fecha_real: Optional[datetime] = Field(None, description="Fecha de retorno físico (por defecto ahora)")


class PrestamoResponse(BaseModel):
    id: str
    estudiante_id: str
    libro_id: str
    fecha_salida: datetime
    fecha_pactada: datetime
    fecha_real: Optional[datetime] = None
    estado_prestamo: str
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    estudiante: Optional[EstudianteResponse] = None
    libro: Optional[LibroResponse] = None

    model_config = ConfigDict(from_attributes=True)
