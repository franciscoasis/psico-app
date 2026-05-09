"""
Router para gestión de pacientes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from config import SessionLocal
from crud import GestorPacientes
from schemas import (
    PacienteCreate,
    PacienteUpdate,
    PacienteResponse,
    PacienteListResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)

# Dependencia para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== ENDPOINTS PACIENTES ====================

@router.get("/", response_model=PacienteListResponse)
async def listar_pacientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Listar todos los pacientes con paginación"""
    from main import manager
    
    gestor = GestorPacientes(db)
    pacientes = gestor.obtener_todos_pacientes()
    total = len(pacientes)
    pacientes_paginados = pacientes[skip:skip + limit]
    
    return {
        "total": total,
        "pacientes": pacientes_paginados
    }


@router.post("", response_model=PacienteResponse)
async def crear_paciente(
    paciente: PacienteCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo paciente"""
    from main import manager
    
    try:
        gestor = GestorPacientes(db)
        
        paciente_nuevo = gestor.crear_paciente(
            nombre=paciente.nombre,
            apellido=paciente.apellido,
            telefono=paciente.telefono,
            fecha_nacimiento=paciente.fecha_nacimiento
        )
        
        # Notificar a clientes WebSocket
        await manager.broadcast({
            "tipo": "paciente_nuevo",
            "datos": {
                "id": paciente_nuevo.id,
                "nombre": paciente_nuevo.nombre,
                "apellido": paciente_nuevo.apellido
            },
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return paciente_nuevo
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al crear paciente: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{paciente_id}", response_model=PacienteResponse)
async def obtener_paciente(
    paciente_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un paciente por ID"""
    gestor = GestorPacientes(db)
    paciente = gestor.obtener_paciente(paciente_id)
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    return paciente


@router.put("/{paciente_id}", response_model=PacienteResponse)
async def actualizar_paciente(
    paciente_id: int,
    datos: PacienteUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar datos de un paciente"""
    from main import manager
    
    try:
        gestor = GestorPacientes(db)
        paciente_actual = gestor.obtener_paciente(paciente_id)
        
        if not paciente_actual:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        datos_actualizar = datos.model_dump(exclude_unset=True)
        paciente_actualizado = gestor.actualizar_paciente(paciente_id, **datos_actualizar)
        
        # Notificar a clientes WebSocket
        await manager.broadcast({
            "tipo": "paciente_actualizado",
            "datos": {
                "id": paciente_actualizado.id,
                "nombre": paciente_actualizado.nombre
            },
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return paciente_actualizado
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar paciente: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{paciente_id}")
async def eliminar_paciente(
    paciente_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un paciente"""
    from main import manager
    
    try:
        gestor = GestorPacientes(db)
        paciente = gestor.obtener_paciente(paciente_id)
        
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        gestor.eliminar_paciente(paciente_id)
        
        # Notificar a clientes WebSocket
        await manager.broadcast({
            "tipo": "paciente_eliminado",
            "datos": {"id": paciente_id},
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return {"mensaje": f"Paciente {paciente_id} eliminado correctamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar paciente: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/buscar/nombre", response_model=PacienteListResponse)
async def buscar_por_nombre(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Buscar pacientes por nombre"""
    gestor = GestorPacientes(db)
    pacientes = gestor.buscar_por_nombre(q)
    
    return {
        "total": len(pacientes),
        "pacientes": pacientes
    }
