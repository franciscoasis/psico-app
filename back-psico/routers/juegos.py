"""
Router para gestión de juegos activos
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging
from typing import Optional

from config import SessionLocal
from crud import GestorJuegosActivos, GestorPacientes, GestorBosses
from schemas import (
    BossCreate,
    BossUpdate,
    BossResponse,
    JuegoActivoTBOICreate,
    JuegoActivoTBOIUpdate,
    JuegoActivoTBOIResponse,
    JuegoActivoMinecraftCreate,
    JuegoActivoMinecraftUpdate,
    JuegoActivoMinecraftResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/juegos",
    tags=["Juegos Activos"]
)

# Dependencia para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== ENDPOINTS JUEGOS GENERALES ====================

@router.get("/")
async def listar_juegos_activos(
    paciente_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Listar todos los juegos activos, opcionalmente filtrados por paciente"""
    gestor = GestorJuegosActivos(db)
    
    if paciente_id:
        juegos = gestor.obtener_juegos_activos_por_paciente(paciente_id)
    else:
        juegos = gestor.obtener_todos_juegos_activos()
    
    return {
        "total": len(juegos),
        "juegos": juegos
    }


@router.get("/{juego_id}")
async def obtener_juego(
    juego_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un juego activo por ID"""
    gestor = GestorJuegosActivos(db)
    juego = gestor.obtener_juego_activo(juego_id)
    
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    
    return juego


@router.delete("/{juego_id}")
async def eliminar_juego(
    juego_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un juego activo"""
    gestor = GestorJuegosActivos(db)
    juego = gestor.obtener_juego_activo(juego_id)
    
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    
    gestor.eliminar_juego_activo(juego_id)
    
    return {"mensaje": f"Juego {juego_id} eliminado correctamente"}


@router.patch("/{juego_id}/desactivar")
async def desactivar_juego(
    juego_id: int,
    db: Session = Depends(get_db)
):
    """Desactivar un juego (marcar como inactivo)"""
    gestor = GestorJuegosActivos(db)
    juego = gestor.desactivar_juego(juego_id)
    
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    
    return {"mensaje": f"Juego {juego_id} desactivado", "juego": juego}


# ==================== ENDPOINTS BOSSES ====================

@router.post("/bosses", response_model=BossResponse)
async def crear_boss(
    datos: BossCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo boss"""
    try:
        gestor = GestorBosses(db)
        boss = gestor.crear_boss(
            nombre=datos.nombre,
            dificultad=datos.dificultad,
            descripcion=datos.descripcion,
            estrategias=datos.estrategias
        )
        return boss
    except Exception as e:
        logger.error(f"Error al crear boss: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bosses", response_model=list[BossResponse])
async def listar_bosses(
    db: Session = Depends(get_db)
):
    """Listar todos los bosses"""
    gestor = GestorBosses(db)
    bosses = gestor.obtener_todos_bosses()
    return bosses


@router.get("/bosses/{boss_id}", response_model=BossResponse)
async def obtener_boss(
    boss_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un boss por ID"""
    gestor = GestorBosses(db)
    boss = gestor.obtener_boss(boss_id)
    
    if not boss:
        raise HTTPException(status_code=404, detail="Boss no encontrado")
    
    return boss


@router.put("/bosses/{boss_id}", response_model=BossResponse)
async def actualizar_boss(
    boss_id: int,
    datos: BossUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un boss"""
    try:
        gestor = GestorBosses(db)
        boss = gestor.obtener_boss(boss_id)
        
        if not boss:
            raise HTTPException(status_code=404, detail="Boss no encontrado")
        
        datos_actualizar = datos.model_dump(exclude_unset=True)
        boss_actualizado = gestor.actualizar_boss(boss_id, **datos_actualizar)
        
        return boss_actualizado
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar boss: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/bosses/{boss_id}")
async def eliminar_boss(
    boss_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un boss"""
    gestor = GestorBosses(db)
    boss = gestor.obtener_boss(boss_id)
    
    if not boss:
        raise HTTPException(status_code=404, detail="Boss no encontrado")
    
    gestor.eliminar_boss(boss_id)
    return {"mensaje": f"Boss {boss_id} eliminado correctamente"}


# ==================== ENDPOINTS THE BINDING OF ISAAC ====================

@router.post("/pacientes/{paciente_id}/tboi", response_model=JuegoActivoTBOIResponse)
async def crear_tboi(
    paciente_id: int,
    datos: JuegoActivoTBOICreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo juego de The Binding of Isaac para un paciente"""
    try:
        gestor_juegos = GestorJuegosActivos(db)
        gestor_pacientes = GestorPacientes(db)
        
        # Verificar que el paciente existe
        paciente = gestor_pacientes.obtener_paciente(paciente_id)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        juego = gestor_juegos.crear_tboi(
            paciente_id=paciente_id,
            personaje=datos.personaje,
            dificultad=datos.dificultad,
            items_recolectados=datos.items_recolectados,
            notas=datos.notas,
            boss_id=datos.boss_id,
            cronograma_semanal=datos.cronograma_semanal,
            frase_semanal=datos.frase_semanal,
            objetivos=datos.objetivos,
            recompensas=datos.recompensas,
            corazones=datos.corazones,
            keys=datos.keys,
            bombas=datos.bombas,
            monedas=datos.monedas
        )
        
        return juego
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al crear juego TBOI: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pacientes/{paciente_id}/tboi")
async def listar_tboi_paciente(
    paciente_id: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los juegos de The Binding of Isaac de un paciente"""
    gestor_juegos = GestorJuegosActivos(db)
    gestor_pacientes = GestorPacientes(db)
    
    # Verificar que el paciente existe
    paciente = gestor_pacientes.obtener_paciente(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    juegos = gestor_juegos.obtener_tboi_por_paciente(paciente_id)
    
    return {
        "total": len(juegos),
        "juegos": juegos
    }


@router.patch("/tboi/{juego_id}/progreso")
async def actualizar_progreso_tboi(
    juego_id: int,
    progreso_pisos: Optional[int] = Query(None),
    logros: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Actualizar progreso de The Binding of Isaac"""
    try:
        gestor = GestorJuegosActivos(db)
        
        juego = gestor.update_tboi_progreso(
            juego_id=juego_id,
            progreso_pisos=progreso_pisos,
            logros=logros
        )
        
        if not juego:
            raise HTTPException(status_code=404, detail="Juego no encontrado")
        
        return {"mensaje": "Progreso actualizado", "juego": juego}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar progreso TBOI: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tboi/{juego_id}", response_model=JuegoActivoTBOIResponse)
async def actualizar_tboi(
    juego_id: int,
    datos: JuegoActivoTBOIUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar datos completos de un juego de The Binding of Isaac"""
    try:
        gestor = GestorJuegosActivos(db)
        
        datos_actualizar = datos.model_dump(exclude_unset=True)
        juego = gestor.actualizar_juego_activo(juego_id, **datos_actualizar)
        
        if not juego:
            raise HTTPException(status_code=404, detail="Juego no encontrado")
        
        return juego
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar juego TBOI: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ENDPOINTS MINECRAFT ====================

@router.post("/pacientes/{paciente_id}/minecraft", response_model=JuegoActivoMinecraftResponse)
async def crear_minecraft(
    paciente_id: int,
    datos: JuegoActivoMinecraftCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo juego de Minecraft para un paciente"""
    try:
        gestor_juegos = GestorJuegosActivos(db)
        gestor_pacientes = GestorPacientes(db)
        
        # Verificar que el paciente existe
        paciente = gestor_pacientes.obtener_paciente(paciente_id)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        juego = gestor_juegos.crear_minecraft(
            paciente_id=paciente_id,
            nombre_mundo=datos.nombre_mundo,
            modo_juego=datos.modo_juego,
            bioma_actual=datos.bioma_actual,
            notas=datos.notas
        )
        
        return juego
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al crear juego Minecraft: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pacientes/{paciente_id}/minecraft")
async def listar_minecraft_paciente(
    paciente_id: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los juegos de Minecraft de un paciente"""
    gestor_juegos = GestorJuegosActivos(db)
    gestor_pacientes = GestorPacientes(db)
    
    # Verificar que el paciente existe
    paciente = gestor_pacientes.obtener_paciente(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    juegos = gestor_juegos.obtener_minecraft_por_paciente(paciente_id)
    
    return {
        "total": len(juegos),
        "juegos": juegos
    }


@router.patch("/minecraft/{juego_id}/progreso")
async def actualizar_progreso_minecraft(
    juego_id: int,
    nivel_experiencia: Optional[int] = Query(None),
    bloques_minados: Optional[int] = Query(None),
    bloques_colocados: Optional[int] = Query(None),
    distancia_caminada: Optional[float] = Query(None),
    tiempo_juego: Optional[int] = Query(None),
    bioma_actual: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Actualizar progreso de Minecraft"""
    try:
        gestor = GestorJuegosActivos(db)
        
        juego = gestor.update_minecraft_progreso(
            juego_id=juego_id,
            nivel_experiencia=nivel_experiencia,
            bloques_minados=bloques_minados,
            bloques_colocados=bloques_colocados,
            distancia_caminada=distancia_caminada,
            tiempo_juego=tiempo_juego,
            bioma_actual=bioma_actual
        )
        
        if not juego:
            raise HTTPException(status_code=404, detail="Juego no encontrado")
        
        return {"mensaje": "Progreso actualizado", "juego": juego}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar progreso Minecraft: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/minecraft/{juego_id}", response_model=JuegoActivoMinecraftResponse)
async def actualizar_minecraft(
    juego_id: int,
    datos: JuegoActivoMinecraftUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar datos completos de un juego de Minecraft"""
    try:
        gestor = GestorJuegosActivos(db)
        
        datos_actualizar = datos.model_dump(exclude_unset=True)
        juego = gestor.actualizar_juego_activo(juego_id, **datos_actualizar)
        
        if not juego:
            raise HTTPException(status_code=404, detail="Juego no encontrado")
        
        return juego
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar juego Minecraft: {e}")
        raise HTTPException(status_code=500, detail=str(e))
