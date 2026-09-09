from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EstudianteBase(BaseModel):
    documento_identidad: str = Field(..., min_length=3, max_length=50, description="Cédula, TI o Código")
    nombre_completo: str = Field(..., min_length=3, max_length=150, description="Nombre completo del estudiante")
    correo_institucional: EmailStr = Field(..., max_length=100, description="Correo universitario @pca.edu.co")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    carrera: str = Field(..., min_length=3, max_length=100, description="Programa académico")


class EstudianteCreate(EstudianteBase):
    pass


class EstudianteUpdate(BaseModel):
    documento_identidad: Optional[str] = Field(None, min_length=3, max_length=50)
    nombre_completo: Optional[str] = Field(None, min_length=3, max_length=150)
    correo_institucional: Optional[EmailStr] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    carrera: Optional[str] = Field(None, min_length=3, max_length=100)
    estado: Optional[bool] = None


class EstudianteResponse(EstudianteBase):
    id: str
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)
