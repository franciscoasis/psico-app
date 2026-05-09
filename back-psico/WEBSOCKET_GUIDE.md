# WebSocket - Guía Completa

## Overview

El servidor incluye un cliente WebSocket completamente funcional con manejo correcto de concurrencia.

## Arquitectura

```
┌─────────────────────────────────────┐
│   Cliente WebSocket                 │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────┐   │
│  │ Tarea de Lectura (Background) │   │
│  │ Lee de websocket.recv()     │   │
│  │ Almacena en Cola            │   │
│  └──────────────┬──────────────┘   │
│                 │                   │
│  ┌──────────────▼──────────────┐   │
│  │   asyncio.Queue             │   │
│  │   (De-couples send/recv)    │   │
│  └──────────────┬──────────────┘   │
│                 │                   │
│  ┌──────────────▼──────────────┐   │
│  │ Tareas de Envío             │   │
│  │ enviar_ping()               │   │
│  │ enviar_mensaje()            │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
         ↓            ↑
    WebSocket (HTTP Upgrade)
```

**Ventaja**: Permite enviar y recibir simultáneamente sin errores de concurrencia.

## Uso Rápido

### Modo 1: Cliente Simple (Secuencial)

```bash
python cliente_ws.py simple
```

```python
from cliente_ws import ClienteWebSocket
import asyncio

async def main():
    cliente = ClienteWebSocket()
    await cliente.conectar()
    await cliente.enviar_ping()  # Espera respuesta
    await cliente.desconectar()

asyncio.run(main())
```

### Modo 2: Escucha Continua

```bash
python cliente_ws.py escucha
```

Útil para aplicaciones que solo reciben notificaciones.

### Modo 3: Envío + Escucha (Recomendado)

```bash
python cliente_ws.py ambos
```

Ambiente completo: el cliente escucha en background mientras puedes enviar mensajes cuando quieras.

## Ejemplos Avanzados

Ejecutar cualquiera con:
```bash
python ejemplos_ws.py {tipo}
```

### 1. Monitoreo en Tiempo Real

```bash
python ejemplos_ws.py monitoreo
```

```python
async def monitorear():
    cliente = ClienteWebSocket()
    await cliente.conectar()
    
    # Escucha en background
    tarea = asyncio.create_task(cliente.escuchar_mensajes())
    
    try:
        # Enviar eventos cada 2 segundos
        for i in range(5):
            await asyncio.sleep(2)
            await cliente.enviar_mensaje({"evento": f"evento_{i}"})
    finally:
        tarea.cancel()
        await cliente.desconectar()
```

### 2. Comunicación Bidireccional con Callback

```bash
python ejemplos_ws.py bidireccional
```

```python
async def procesar_mensaje(mensaje):
    print(f"Mensaje procesado: {mensaje}")

async def comunicar():
    cliente = ClienteWebSocket()
    await cliente.conectar()
    
    # Escucha con callback
    await cliente.escuchar_mensajes(callback=procesar_mensaje)
```

### 3. Múltiples Clientes Simultáneos

```bash
python ejemplos_ws.py multiples
```

```python
async def cliente_numero(n):
    cliente = ClienteWebSocket()
    await cliente.conectar()
    for i in range(3):
        await asyncio.sleep(1)
        await cliente.enviar_ping()
    await cliente.desconectar()

# 3 clientes simultáneamente
await asyncio.gather(
    cliente_numero(1),
    cliente_numero(2),
    cliente_numero(3)
)
```

### 4. Manejo de Errores y Reconexión

```bash
python ejemplos_ws.py errores
```

```python
async def conectar_con_reintentos(max_intentos=3):
    for intento in range(max_intentos):
        try:
            cliente = ClienteWebSocket()
            if await cliente.conectar():
                return cliente
        except Exception as e:
            print(f"Error intento {intento + 1}: {e}")
            await asyncio.sleep(2)
    return None
```

## API Reference

### Métodos Principal

#### `conectar()` → bool
Conecta al servidor. Retorna True si éxitoso.

```python
if await cliente.conectar():
    print("Conectado")
```

#### `enviar_ping()`
Envía un ping y espera pong.

```python
await cliente.enviar_ping()
# Output: → Ping enviado
#         ← {"tipo":"pong","timestamp":"..."}
```

#### `enviar_mensaje(datos: dict)`
Envía un mensaje de broadcast.

```python
await cliente.enviar_mensaje({"evento": "nuevo_paciente"})
```

#### `escuchar_mensajes(callback=None)`
Escucha continuamente. Opcional: procesa con callback.

```python
async def procesar(msg):
    print(f"Recibido: {msg}")

await cliente.escuchar_mensajes(callback=procesar)
```

#### `obtener_mensaje(timeout=None)` → dict | None
Obtiene UN mensaje de la cola.

```python
msg = await cliente.obtener_mensaje(timeout=5)
if msg:
    print(msg)
```

#### `desconectar()`
Cierra la conexión limpiamente.

```python
await cliente.desconectar()
```

## Patrones Comunes

### Patrón 1: Esperar una Respuesta

```python
await cliente.enviar_mensaje({"acción": "pedido"})
respuesta = await cliente.obtener_mensaje(timeout=5)
```

### Patrón 2: Loop de Lectura

```python
while True:
    msg = await cliente.obtener_mensaje()
    if msg:
        print(f"Recibido: {msg['contenido']}")
```

### Patrón 3: Múltiples Tareas

```python
async def leer():
    await cliente.escuchar_mensajes()

async def escribir():
    for i in range(10):
        await asyncio.sleep(1)
        await cliente.enviar_ping()

await asyncio.gather(leer(), escribir())
```

### Patrón 4: Manejo de Timeout

```python
try:
    respuesta = await asyncio.wait_for(
        cliente.obtener_mensaje(),
        timeout=5
    )
except asyncio.TimeoutError:
    print("Timeout: sin respuesta")
```

## Solución de Problemas

### Error: "RuntimeError: cannot call recv while another coroutine is already waiting"

**Causa**: Dos corrutinas llamando `recv()` simultáneamente.

**Solución**: Usar `escuchar_mensajes()` en background, que maneja esto internamente.

✓ Correcto:
```python
tarea = asyncio.create_task(cliente.escuchar_mensajes())
await cliente.enviar_ping()  # OK
```

✗ Incorrecto:
```python
tarea = asyncio.create_task(cliente.escuchar())  # recv() espera
await cliente.enviar_ping()  # Llama a recv() otra vez → ERROR
```

### Error: "Connection refused"

El servidor no está corriendo.

```bash
python main.py  # En otra terminal
```

### Error: "Timeout esperando respuesta"

El servidor no responde en tiempo.

- Aumentar timeout: `await cliente.obtener_mensaje(timeout=10)`
- Verificar servidor: `curl http://localhost:8000/`

## Testing

Todos los ejemplos tienen código para pruebas:

```bash
# Servidor
python main.py

# En otra terminal:
python cliente_ws.py simple     # Test básico
python cliente_ws.py ambos      # Test concurrencia
python ejemplos_ws.py monitoreo # Test real-time
```

## Notas de Rendimiento

- Usa `asyncio.Queue` → eficiente incluso con miles de mensajes
- Backpressure automática si la cola se llena
- Sin bloqueo en archivo/red

## Integración with FastAPI

El servidor está listo para integrar en aplicaciones reales:

```python
# Notificaciones en tiempo real
async def crear_paciente():
    # ... lógica ...
    await manager.broadcast({
        "tipo": "paciente_nuevo",
        "datos": paciente_dict
    })
```
