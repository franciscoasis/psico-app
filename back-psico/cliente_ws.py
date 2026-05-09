"""
Cliente de prueba para el servidor WebSocket
"""
import asyncio
import websockets
import json
from datetime import datetime
from typing import Optional, Callable


class ClienteWebSocket:
    """Cliente para conectarse al servidor WebSocket con manejo correcto de recv/send"""
    
    def __init__(self, url: str = "ws://localhost:8000/ws"):
        self.url = url
        self.websocket = None
        self.cola_mensajes = asyncio.Queue()
        self.tarea_lectura = None
        self.conectado = False
    
    async def _leer_mensajes(self):
        """Lee mensajes del servidor y los pone en una cola (ejecutarse en background)"""
        try:
            while self.conectado:
                mensaje = await self.websocket.recv()
                await self.cola_mensajes.put({"tipo": "mensaje", "contenido": mensaje})
        except asyncio.CancelledError:
            pass
        except Exception as e:
            await self.cola_mensajes.put({"tipo": "error", "contenido": str(e)})
    
    async def conectar(self):
        """Conectar al servidor"""
        try:
            self.websocket = await websockets.connect(self.url)
            self.conectado = True
            print(f"✓ Conectado a {self.url}")
            
            # Iniciar tarea de lectura en background
            self.tarea_lectura = asyncio.create_task(self._leer_mensajes())
            
            # Enviar mensaje de conexión
            await self.websocket.send(json.dumps({
                "tipo": "conectado"
            }))
            
            # Esperar confirmación desde la cola
            confirmacion = await asyncio.wait_for(self.cola_mensajes.get(), timeout=5)
            print(f"Servidor: {confirmacion['contenido']}")
            
        except Exception as e:
            print(f"✗ Error al conectar: {e}")
            self.conectado = False
            return False
        
        return True
    
    async def enviar_ping(self):
        """Enviar ping al servidor"""
        mensaje = {"tipo": "ping"}
        await self.websocket.send(json.dumps(mensaje))
        print(f"→ Ping enviado")
        
        try:
            respuesta = await asyncio.wait_for(self.cola_mensajes.get(), timeout=5)
            print(f"← {respuesta['contenido']}")
        except asyncio.TimeoutError:
            print("✗ Timeout esperando respuesta")
    
    async def enviar_mensaje(self, datos: dict):
        """Enviar mensaje de broadcast"""
        mensaje = {
            "tipo": "broadcast",
            "datos": datos
        }
        await self.websocket.send(json.dumps(mensaje))
        print(f"→ Mensaje enviado: {datos}")
    
    async def obtener_mensaje(self, timeout: Optional[float] = None):
        """Obtener un mensaje de la cola (no bloquea recv)"""
        try:
            if timeout:
                return await asyncio.wait_for(self.cola_mensajes.get(), timeout=timeout)
            else:
                return await self.cola_mensajes.get()
        except asyncio.TimeoutError:
            return None
    
    async def escuchar_mensajes(self, callback: Optional[Callable] = None):
        """Escuchar mensaje continuamente (no usar con enviar_ping simultáneamente)"""
        print("Escuchando mensajes... (presiona Ctrl+C para detener)")
        try:
            while self.conectado:
                mensaje = await self.obtener_mensaje(timeout=1)
                if mensaje:
                    print(f"← {mensaje['contenido']}")
                    if callback:
                        await callback(mensaje)
        except KeyboardInterrupt:
            print("\nEscucha detenida")
    
    async def desconectar(self):
        """Desconectar del servidor"""
        self.conectado = False
        if self.tarea_lectura:
            self.tarea_lectura.cancel()
            try:
                await self.tarea_lectura
            except asyncio.CancelledError:
                pass
        
        if self.websocket:
            await self.websocket.close()
            print("✓ Desconectado")


async def ejemplo_cliente():
    """Ejemplo de uso del cliente - envíos secuenciales"""
    cliente = ClienteWebSocket()
    
    # Conectar
    if not await cliente.conectar():
        return
    
    print("\n--- Enviando pings ---")
    for i in range(3):
        await cliente.enviar_ping()
        await asyncio.sleep(1)
    
    print("\n--- Enviando mensajes ---")
    await cliente.enviar_mensaje({
        "evento": "nuevo_evento",
        "descripción": "Prueba de broadcast"
    })
    
    await asyncio.sleep(2)
    await cliente.desconectar()


async def ejemplo_escucha_continua():
    """Ejemplo: escuchar mensajes continuamente"""
    cliente = ClienteWebSocket()
    
    if not await cliente.conectar():
        return
    
    print("\n--- Escuchando mensajes en tiempo real ---")
    try:
        await cliente.escuchar_mensajes()
    except KeyboardInterrupt:
        pass
    finally:
        await cliente.desconectar()


async def ejemplo_envio_con_escucha():
    """Ejemplo: enviar mensajes MIENTRAS se escuchan (mode correcto)"""
    cliente = ClienteWebSocket()
    
    if not await cliente.conectar():
        return
    
    # Crear tarea de escucha que corre en background
    tarea_escucha = asyncio.create_task(cliente.escuchar_mensajes())
    
    try:
        # Enviar mensajes mientras se escucha
        await asyncio.sleep(1)
        
        print("\n--- Enviando ping 1 ---")
        await cliente.enviar_ping()
        
        await asyncio.sleep(2)
        
        print("\n--- Enviando broadcast ---")
        await cliente.enviar_mensaje({"tipo": "actualización", "estado": "activo"})
        
        await asyncio.sleep(3)
    
    except KeyboardInterrupt:
        print("\nInterrupción del usuario")
    
    finally:
        tarea_escucha.cancel()
        try:
            await tarea_escucha
        except asyncio.CancelledError:
            pass
        await cliente.desconectar()


if __name__ == "__main__":
    print("=== Cliente WebSocket de Prueba ===\n")
    
    # Seleccionar modo de prueba:
    import sys
    
    if len(sys.argv) > 1:
        modo = sys.argv[1]
    else:
        modo = "simple"
    
    if modo == "escucha":
        print("Modo: Escucha continua")
        asyncio.run(ejemplo_escucha_continua())
    elif modo == "ambos":
        print("Modo: Envío + Escucha simultáneos")
        asyncio.run(ejemplo_envio_con_escucha())
    else:
        print("Modo: Cliente simple (secuencial)")
        asyncio.run(ejemplo_cliente())
    
    print("\n✓ Finalizado")
