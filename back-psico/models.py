"""
Modelos de la base de datos para pacientes
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from config import Base
import enum


class Juego(enum.Enum):
    """Opciones de juegos"""
    TBOI = "The Binding of Isaac"
    minecraft = "Minecraft"


# Tabla de unión para la relación muchos-a-muchos entre Paciente y JuegoActivo
paciente_juego_association = Table(
    'paciente_juego',
    Base.metadata,
    Column('paciente_id', Integer, ForeignKey('pacientes.id'), primary_key=True),
    Column('juego_activo_id', Integer, ForeignKey('juegos_activos.id'), primary_key=True)
)

class Boss(Base):
    """Modelo para almacenar información de bosses en The Binding of Isaac"""
    __tablename__ = "bosses"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    dificultad = Column(String(50))  # Dificultad del boss (Normal, Hard, etc.)
    descripcion = Column(Text)  # Descripción del boss y sus ataques
    estrategias = Column(Text)  # Estrategias recomendadas para derrotar al boss

    def __repr__(self):
        return f"<Boss(id={self.id}, nombre={self.nombre}, piso={self.piso_asociado})>"

class JuegoActivo(Base):
    """Modelo base para almacenar juegos activos de un paciente"""
    __tablename__ = "juegos_activos"

    id = Column(Integer, primary_key=True, index=True)
    tipo_juego = Column(String(50), nullable=False)  # Discriminator para herencia
    activo = Column(Boolean, default=True)
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_fin = Column(DateTime, nullable=True)
    notas = Column(Text)
    pacientes = relationship(
        "Paciente",
        secondary=paciente_juego_association,
        back_populates="juegos_activos"
    )

    __mapper_args__ = {
        "polymorphic_identity": "juego_base",
        "polymorphic_on": tipo_juego,
    }

    def __repr__(self):
        return f"<JuegoActivo(id={self.id}, tipo={self.tipo_juego}, activo={self.activo})>"


class JuegoActivoTBOI(JuegoActivo):
    """Modelo para The Binding of Isaac con datos específicos"""
    __tablename__ = "juegos_tboi"

    id = Column(Integer, ForeignKey("juegos_activos.id"), primary_key=True)
    boss_id = Column(Integer, ForeignKey("bosses.id"), nullable=True)
    
    # Datos específicos de The Binding of Isaac
    progreso_pisos = Column(Integer, default=0)  # Número de pisos completados
    items_recolectados = Column(Text)  # Lista de items encontrados
    personaje = Column(String(100))  # Personaje jugado
    logros = Column(Text)  # Logros desbloqueados
    dificultad = Column(String(50))  # Dificultad (Normal, Hard, Greed Mode, etc.)
    cronograma_semanal = Column(Text)  # Cronograma de las actividades semanales
    frase_semanal = Column(String(500))  # Frase o motivación semanal
    objetivos = Column(Text)  # Objetivos del jugador
    recompensas = Column(Text)  # Recompensas alcanzadas
    corazones = Column(Integer, default=0)  # Puntos de vida
    keys = Column(Integer, default=0)  # Llaves recolectadas
    bombas = Column(Integer, default=0)  # Bombas recolectadas
    monedas = Column(Integer, default=0)  # Monedas recolectadas
    
    __mapper_args__ = {
        "polymorphic_identity": "tboi",
    }

    def __repr__(self):
        return f"<JuegoActivoTBOI(id={self.id}, personaje={self.personaje}, pisos={self.progreso_pisos})>"


class JuegoActivoMinecraft(JuegoActivo):
    """Modelo para Minecraft con datos específicos"""
    __tablename__ = "juegos_minecraft"

    id = Column(Integer, ForeignKey("juegos_activos.id"), primary_key=True)
    
    # Datos específicos de Minecraft
    nivel_experiencia = Column(Integer, default=0)
    modo_juego = Column(String(50))  # Survival, Creative, Adventure, Spectator
    nombre_mundo = Column(String(255))
    bloques_minados = Column(Integer, default=0)
    bloques_colocados = Column(Integer, default=0)
    distancia_caminada = Column(Float, default=0.0)  # En bloques
    mobs_derrotados = Column(Text)  # JSON con tipos de mobs y cantidad
    estructuras_encontradas = Column(Text)  # Pueblo, Fortaleza, etc.
    tiempo_juego = Column(Integer, default=0)  # Minutos jugados
    bioma_actual = Column(String(100))
    
    __mapper_args__ = {
        "polymorphic_identity": "minecraft",
    }

    def __repr__(self):
        return f"<JuegoActivoMinecraft(id={self.id}, mundo={self.nombre_mundo}, modo={self.modo_juego})>"


class Paciente(Base):
    """Modelo para almacenar datos de pacientes"""
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    apellido = Column(String(255), nullable=False)
    telefono = Column(String(20))
    fecha_nacimiento = Column(DateTime)
    diagnostico = Column(Text)
    medicamentos = Column(Text)
    antecedentes = Column(Text)
    notas = Column(Text)
    activo = Column(Boolean, default=True)
    juegos_activos = relationship(
        "JuegoActivo",
        secondary=paciente_juego_association,
        back_populates="pacientes",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Paciente(id={self.id}, nombre={self.nombre} {self.apellido})>"
