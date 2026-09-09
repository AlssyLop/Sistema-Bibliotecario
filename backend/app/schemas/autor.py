from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AutorBase(BaseModel):
    documento_identidad: str = Field(..., min_length=3, max_length=50, description="Documento de identidad del autor")
    nombre_completo: str = Field(..., min_length=3, max_length=150, description="Nombre y apellidos del autor")
    correo: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico de contacto")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")


class AutorCreate(AutorBase):
    pass


class AutorUpdate(BaseModel):
    documento_identidad: Optional[str] = Field(None, min_length=3, max_length=50)
    nombre_completo: Optional[str] = Field(None, min_length=3, max_length=150)
    correo: Optional[EmailStr] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    estado: Optional[bool] = None


class AutorResponse(AutorBase):
    id: str
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)
