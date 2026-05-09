"""
Esquemas Pydantic para validación de datos
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal, List


# ==================== BOSS ====================

class BossCreate(BaseModel):
    """Esquema para crear un Boss"""
    nombre: str
    dificultad: Optional[str] = None
    descripcion: Optional[str] = None
    estrategias: Optional[str] = None


class BossResponse(BaseModel):
    """Esquema de respuesta para Boss"""
    id: int
    nombre: str
    dificultad: Optional[str] = None
    descripcion: Optional[str] = None
    estrategias: Optional[str] = None
    
    class Config:
        from_attributes = True


class BossUpdate(BaseModel):
    """Esquema para actualizar un Boss"""
    nombre: Optional[str] = None
    dificultad: Optional[str] = None
    descripcion: Optional[str] = None
    estrategias: Optional[str] = None


# ==================== JUEGOS ACTIVOS ====================

class JuegoActivoBase(BaseModel):
    """Esquema base para JuegoActivo"""
    activo: bool = True
    notas: Optional[str] = None


class JuegoActivoTBOICreate(JuegoActivoBase):
    """Esquema para crear JuegoActivoTBOI"""
    personaje: Optional[str] = None
    progreso_pisos: int = 0
    items_recolectados: Optional[str] = None
    logros: Optional[str] = None
    dificultad: Optional[str] = None
    boss_id: Optional[int] = None
    cronograma_semanal: Optional[str] = None
    frase_semanal: Optional[str] = None
    objetivos: Optional[str] = None
    recompensas: Optional[str] = None
    corazones: int = 0
    keys: int = 0
    bombas: int = 0
    monedas: int = 0


class JuegoActivoTBOIUpdate(BaseModel):
    """Esquema para actualizar JuegoActivoTBOI"""
    personaje: Optional[str] = None
    cronograma_semanal: Optional[str] = None
    frase_semanal: Optional[str] = None
    boss: Optional[BossResponse] = None
    objetivos: Optional[str] = None
    recompensas: Optional[str] = None
    corazones: int
    keys: int 
    bombas: int
    monedas: int

class JuegoActivoTBOIResponse(JuegoActivoBase):
    """Esquema de respuesta para JuegoActivoTBOI"""
    id: int
    tipo_juego: str
    progreso_pisos: int
    items_recolectados: Optional[str] = None
    personaje: Optional[str] = None
    logros: Optional[str] = None
    dificultad: Optional[str] = None
    cronograma_semanal: Optional[str] = None
    frase_semanal: Optional[str] = None
    boss: Optional[BossResponse] = None
    objetivos: Optional[str] = None
    recompensas: Optional[str] = None
    corazones: Optional[int] = 0
    keys: Optional[int] = 0
    bombas: Optional[int] = 0
    monedas: Optional[int] = 0
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class JuegoActivoMinecraftCreate(JuegoActivoBase):
    """Esquema para crear JuegoActivoMinecraft"""
    modo_juego: Optional[str] = None
    nombre_mundo: Optional[str] = None
    nivel_experiencia: int = 0
    tiempo_juego: int = 0
    bioma_actual: Optional[str] = None


class JuegoActivoMinecraftUpdate(BaseModel):
    """Esquema para actualizar JuegoActivoMinecraft"""
    modo_juego: Optional[str] = None
    nombre_mundo: Optional[str] = None
    nivel_experiencia: Optional[int] = None
    bloques_minados: Optional[int] = None
    bloques_colocados: Optional[int] = None
    distancia_caminada: Optional[float] = None
    mobs_derrotados: Optional[str] = None
    estructuras_encontradas: Optional[str] = None
    tiempo_juego: Optional[int] = None
    bioma_actual: Optional[str] = None
    activo: Optional[bool] = None
    fecha_fin: Optional[datetime] = None
    notas: Optional[str] = None


class JuegoActivoMinecraftResponse(JuegoActivoBase):
    """Esquema de respuesta para JuegoActivoMinecraft"""
    id: int
    tipo_juego: str
    nivel_experiencia: int
    modo_juego: Optional[str] = None
    nombre_mundo: Optional[str] = None
    bloques_minados: int = 0
    bloques_colocados: int = 0
    distancia_caminada: float = 0.0
    mobs_derrotados: Optional[str] = None
    estructuras_encontradas: Optional[str] = None
    tiempo_juego: int = 0
    bioma_actual: Optional[str] = None
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Unión de tipos para respuestas generales
JuegoActivoResponse = JuegoActivoTBOIResponse | JuegoActivoMinecraftResponse


class PacienteBase(BaseModel):
    """Esquema base para Paciente"""
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None


class PacienteCreate(PacienteBase):
    """Esquema para crear Paciente"""
    pass


class PacienteUpdate(BaseModel):
    """Esquema para actualizar Paciente"""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None


class PacienteResponse(PacienteBase):
    """Esquema de respuesta para Paciente"""
    id: int
    activo: bool
    juegos_activos: List[JuegoActivoResponse] = []
    
    class Config:
        from_attributes = True


class PacienteListResponse(BaseModel):
    """Respuesta para lista de pacientes"""
    total: int
    pacientes: list[PacienteResponse]


class MensajeWebSocket(BaseModel):
    """Mensaje genérico por WebSocket"""
    tipo: str  # "paciente_nuevo", "actualización", "error", etc.
    datos: dict
    timestamp: datetime = None


class ErrorResponse(BaseModel):
    """Respuesta de error"""
    error: str
    detalle: Optional[str] = None
