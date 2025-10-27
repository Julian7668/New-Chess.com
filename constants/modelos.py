from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from constants import (
    ROLES,
    ESTADOS_TORNEO,
    FORMATOS_TORNEO,
    RESULTADOS_PARTIDA,
)


# Modelo base para Usuario
class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=2, max_length=50)
    apellido: str = Field(..., min_length=2, max_length=50)
    rol: str = Field(default=ROLES["jugador"])

    @validator("rol")
    def validar_rol(cls, v):
        if v not in ROLES.values():
            raise ValueError(f"Rol debe ser uno de: {list(ROLES.values())}")
        return v


# Modelo para crear usuario (con contraseña)
class UsuarioCrear(UsuarioBase):
    password: str = Field(..., min_length=8)


# Modelo para usuario en base de datos (con hash y timestamps)
class UsuarioDB(UsuarioBase):
    id: int
    password_hash: str
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: Optional[datetime] = None
    activo: bool = True


# Modelo para respuesta de usuario (sin contraseña)
class UsuarioRespuesta(UsuarioBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    activo: bool


# Modelo para login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Modelo para tokens
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Modelo para token data (payload JWT)
class TokenData(BaseModel):
    user_id: int
    email: str
    rol: str


# Modelo para actualizar perfil
class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    apellido: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None


# Modelo para cambiar contraseña
class CambiarPassword(BaseModel):
    password_actual: str
    password_nueva: str = Field(..., min_length=8)


# Modelo base para Torneo
class TorneoBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    formato: str = Field(default=FORMATOS_TORNEO["suizo"])
    max_rondas: int = Field(default=7, ge=1, le=20)
    estado: str = Field(default=ESTADOS_TORNEO["abierto"])

    @validator("formato")
    def validar_formato(cls, v):
        if v not in FORMATOS_TORNEO.values():
            raise ValueError(
                f"Formato debe ser uno de: {list(FORMATOS_TORNEO.values())}"
            )
        return v

    @validator("estado")
    def validar_estado(cls, v):
        if v not in ESTADOS_TORNEO.values():
            raise ValueError(f"Estado debe ser uno de: {list(ESTADOS_TORNEO.values())}")
        return v

    @validator("fecha_fin")
    def validar_fechas(cls, v, values):
        if v and "fecha_inicio" in values and v <= values["fecha_inicio"]:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        return v


# Modelo para crear torneo
class TorneoCrear(TorneoBase):
    pass


# Modelo para torneo en base de datos
class TorneoDB(TorneoBase):
    id: int
    organizador_id: int
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: Optional[datetime] = None


# Modelo para respuesta de torneo
class TorneoRespuesta(TorneoBase):
    id: int
    organizador_id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None


# Modelo para actualizar torneo
class TorneoActualizar(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    formato: Optional[str] = None
    max_rondas: Optional[int] = Field(None, ge=1, le=20)
    estado: Optional[str] = None

    @validator("formato")
    def validar_formato(cls, v):
        if v and v not in FORMATOS_TORNEO.values():
            raise ValueError(
                f"Formato debe ser uno de: {list(FORMATOS_TORNEO.values())}"
            )
        return v

    @validator("estado")
    def validar_estado(cls, v):
        if v and v not in ESTADOS_TORNEO.values():
            raise ValueError(f"Estado debe ser uno de: {list(ESTADOS_TORNEO.values())}")
        return v


# Modelo para inscripción
class InscripcionBase(BaseModel):
    usuario_id: int
    torneo_id: int
    rating_inicial: int = Field(default=1200, ge=0, le=3000)


# Modelo para crear inscripción
class InscripcionCrear(BaseModel):
    torneo_id: int


# Modelo para inscripción en base de datos
class InscripcionDB(InscripcionBase):
    id: int
    fecha_inscripcion: datetime = Field(default_factory=datetime.utcnow)
    puntos: int = 0


# Modelo para respuesta de inscripción
class InscripcionRespuesta(InscripcionBase):
    id: int
    fecha_inscripcion: datetime
    puntos: int


# Modelo para partida
class PartidaBase(BaseModel):
    torneo_id: int
    ronda: int = Field(..., ge=1)
    jugador_blancas_id: int
    jugador_negras_id: int
    resultado: Optional[str] = None

    @validator("resultado")
    def validar_resultado(cls, v):
        if v and v not in RESULTADOS_PARTIDA.values():
            raise ValueError(
                f"Resultado debe ser uno de: {list(RESULTADOS_PARTIDA.values())}"
            )
        return v


# Modelo para crear partida
class PartidaCrear(PartidaBase):
    pass


# Modelo para partida en base de datos
class PartidaDB(PartidaBase):
    id: int
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_resultado: Optional[datetime] = None


# Modelo para respuesta de partida
class PartidaRespuesta(PartidaBase):
    id: int
    fecha_creacion: datetime
    fecha_resultado: Optional[datetime] = None


# Modelo para actualizar resultado de partida
class PartidaActualizarResultado(BaseModel):
    resultado: str

    @validator("resultado")
    def validar_resultado(cls, v):
        if v not in RESULTADOS_PARTIDA.values():
            raise ValueError(
                f"Resultado debe ser uno de: {list(RESULTADOS_PARTIDA.values())}"
            )
        return v


# Modelo para rating
class RatingBase(BaseModel):
    usuario_id: int
    rating: int = Field(..., ge=0, le=3000)
    fecha: datetime = Field(default_factory=datetime.utcnow)


# Modelo para rating en base de datos
class RatingDB(RatingBase):
    id: int


# Modelo para respuesta de rating
class RatingRespuesta(RatingBase):
    id: int


# Modelo para tabla de posiciones
class PosicionTabla(BaseModel):
    usuario_id: int
    nombre: str
    apellido: str
    puntos: float
    rating: int
    victorias: int
    derrotas: int
    tablas: int
