# Base de Datos de Pacientes - Python + FastAPI + WebSockets

Sistema completo de gestión de pacientes con API REST y WebSockets en tiempo real.

## Características

✅ **API REST** - Operaciones HTTP (GET, POST, PUT, DELETE)  
✅ **WebSockets** - Conexiones en tiempo real  
✅ **SQLite** - Base de datos local  
✅ **SQLAlchemy ORM** - Mapeo de datos  
✅ **FastAPI** - Framework moderno  
✅ **Documentación automática** - Swagger UI  

## Instalación

```bash
cd bd-psico
pip install -r requirements.txt
python init_db.py
```

## Ejecutar servidor

```bash
python main.py
```

El servidor estará disponible en:
- **API**: http://localhost:8000
- **Documentación interactiva**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws

## API REST Endpoints

### Crear Paciente
```bash
curl -X POST http://localhost:8000/pacientes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido": "García",
    "email": "juan@email.com",
    "telefono": "555-1234",
    "género": "Masculino"
  }'
```

### Listar Pacientes
```bash
curl http://localhost:8000/pacientes
curl "http://localhost:8000/pacientes?skip=0&limit=10"
```

### Obtener Paciente
```bash
curl http://localhost:8000/pacientes/1
```

### Actualizar Paciente
```bash
curl -X PUT http://localhost:8000/pacientes/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan Carlos"}'
```

### Eliminar Paciente
```bash
curl -X DELETE http://localhost:8000/pacientes/1
```

### Buscar por Nombre
```bash
curl "http://localhost:8000/pacientes/buscar/nombre?q=Juan"
```

## WebSocket Uso

El servidor notifica a todos los clientes conectados sobre cambios en tiempo real:
- `paciente_nuevo` - Nuevo paciente creado
- `paciente_actualizado` - Paciente modificado  
- `paciente_eliminado` - Paciente borrado

**Ver guía completa**: [WEBSOCKET_GUIDE.md](WEBSOCKET_GUIDE.md)

### Inicio Rápido

**Modo simple** (envíos secuenciales):
```bash
python cliente_ws.py simple
```

**Modo avanzado** (envío + escucha simultáneos):
```bash
python cliente_ws.py ambos
```

**Ejemplos avanzados**:
```bash
python ejemplos_ws.py monitoreo      # Monitoreo time real
python ejemplos_ws.py bidireccional  # Comunicación bidireccional
python ejemplos_ws.py multiples      # Múltiples clientes
python ejemplos_ws.py errores        # Manejo de reconexión
```

### Cliente Python - Uso manual

```python
from cliente_ws import ClienteWebSocket
import asyncio

async def main():
    cliente = ClienteWebSocket()
    await cliente.conectar()
    await cliente.enviar_ping()
    await cliente.desconectar()

asyncio.run(main())
```

### Arquitectura del cliente

El cliente utiliza `asyncio.Queue` para manejar correctamente los mensajes:
- Una tarea en background lee continuamente desde `websocket.recv()`
- Los mensajes se almacenan en una cola
- Las operaciones de envío/recepción no entran en conflicto

Esto permite enviar mensajes **mientras se escuchan otros simultáneamente**, sin errores de "cannot call recv while another coroutine is already waiting".

### Mensajes WebSocket

**Ping**:
```json
{"tipo": "ping"}
```

**Conexión**:
```json
{"tipo": "conectado"}
```

**Broadcast**:
```json
{"tipo": "broadcast", "datos": {"evento": "actualización"}}
```

## Estructura del Proyecto

```
bd-psico/
├── main.py              # Servidor FastAPI
├── models.py            # Modelos SQLAlchemy
├── crud.py              # Operaciones CRUD
├── schemas.py           # Esquemas Pydantic
├── config.py            # Configuración BD
├── init_db.py           # Script crear tablas
├── cliente_ws.py        # Cliente WebSocket
├── ejemplo.py           # Ejemplo uso
├── requirements.txt     # Dependencias
└── pacientes.db         # Base de datos (SQLite)
```

## Modelos

### Paciente
- `id` - Identificador único
- `nombre`, `apellido` - Nombre completo
- `email` - Email único
- `telefono` - Teléfono
- `fecha_nacimiento` - Fecha nacimiento
- `género` - Género
- `diagnostico` - Diagnóstico
- `medicamentos` - Medicamentos
- `antecedentes` - Antecedentes médicos
- `número_sesiones` - Total de sesiones
- `última_sesión` - Última fecha sesión
- `próxima_sesión` - Próxima sesión
- `activo` - Estado
- `notas` - Notas generales
- `fecha_registro` - Fecha registro
- `fecha_actualización` - Última actualización

## Notificaciones WebSocket

El servidor notifica a todos los clientes conectados sobre eventos:

- `paciente_nuevo` - Nuevo paciente creado
- `paciente_actualizado` - Paciente actualizado
- `paciente_eliminado` - Paciente eliminado
- `mensaje` - Mensajes de broadcast
- `error` - Errores

Ejemplo de notificación:
```json
{
  "tipo": "paciente_nuevo",
  "datos": {"id": 1, "nombre": "Juan", "email": "juan@email.com"},
  "timestamp": "2026-04-28T01:30:03.144815"
}
```

## Uso en Producción

Para producción, usa Gunicorn con Uvicorn workers:

```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Próximos pasos

- [ ] Autenticación JWT
- [ ] Roles y permisos
- [ ] Historiales clínicos
- [ ] Sistema de reportes
- [ ] Base de datos PostgreSQL
- [ ] Frontend web (React/Vue)
