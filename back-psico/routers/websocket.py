"""
Router para WebSocket
"""
from fastapi import APIRouter, WebSocket
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["WebSocket"]
)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint WebSocket para conexiones en tiempo real
    
    Mensajes esperados:
    - {"tipo": "ping"} -> responde con pong
    - {"tipo": "conectado"} -> confirmación
    """
    from main import manager
    
    await manager.connect(websocket)
    
    try:
        while True:
            # Recibir mensaje del cliente
            datos = await websocket.receive_text()
            logger.info(f"Mensaje recibido: {datos}")
            
            try:
                mensaje = json.loads(datos)
                tipo = mensaje.get("tipo", "desconocido")
                
                if tipo == "ping":
                    await websocket.send_json({
                        "tipo": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                    logger.info("Ping -> Pong")
                
                elif tipo == "conectado":
                    await websocket.send_json({
                        "tipo": "conexión_confirmada",
                        "mensaje": "Conectado al servidor",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                
                elif tipo == "broadcast":
                    # Retransmitir mensaje a todos
                    await manager.broadcast({
                        "tipo": "mensaje",
                        "datos": mensaje.get("datos", {}),
                        "timestamp": datetime.utcnow().isoformat()
                    })
                
                else:
                    await websocket.send_json({
                        "tipo": "error",
                        "detalle": f"Tipo de mensaje desconocido: {tipo}"
                    })
            
            except json.JSONDecodeError:
                await websocket.send_json({
                    "tipo": "error",
                    "detalle": "Formato JSON inválido"
                })
    
    except Exception as e:
        logger.error(f"Error WebSocket: {e}")
    
    finally:
        manager.disconnect(websocket)
