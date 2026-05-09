"""
Servidor FastAPI con WebSockets y API REST para gestión de pacientes
"""
from fastapi import FastAPI, WebSocket, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import json
import logging
from typing import Set

from config import SessionLocal, engine, Base
from models import Paciente
from crud import GestorPacientes
from schemas import (
    PacienteCreate,
    PacienteUpdate,
    PacienteResponse,
    PacienteListResponse,
    MensajeWebSocket,
    ErrorResponse
)

# Importar routers modulares
from routers.pacientes import router as router_pacientes
from routers.juegos import router as router_juegos
from routers.websocket import router as router_websocket

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar app FastAPI
app = FastAPI(
    title="API Pacientes con WebSockets",
    description="Sistema de gestión de pacientes con conexiones en tiempo real",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gestión de conexiones WebSocket activas
class ConnectionManager:
    """Gestor de conexiones WebSocket"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Conectar un cliente"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Cliente conectado. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Desconectar un cliente"""
        self.active_connections.discard(websocket)
        logger.info(f"Cliente desconectado. Total: {len(self.active_connections)}")
    
    async def broadcast(self, mensaje: dict):
        """Enviar mensaje a todos los clientes conectados"""
        for conexión in self.active_connections:
            try:
                await conexión.send_json(mensaje)
            except Exception as e:
                logger.error(f"Error al enviar mensaje: {e}")


manager = ConnectionManager()

# Registrar routers modulares
app.include_router(router_pacientes, prefix="/api/v1")
app.include_router(router_juegos, prefix="/api/v1")
app.include_router(router_websocket)


# Dependencia para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== ENDPOINT RAÍZ ====================

@app.get("/", tags=["Raíz"])
async def root():
    """Endpoint raíz de bienvenida"""
    return {
        "mensaje": "Bienvenido a la API de Pacientes",
        "versión": "1.0.0",
        "endpoints": {
            "pacientes": "/pacientes",
            "pacientes_por_id": "/pacientes/{id}",
            "websocket": "/ws"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
