# 📚 Guía de Routers - BD Psico Backend

Esta es una guía rápida de todos los endpoints disponibles para consumir desde el frontend.

**URL Base**: `http://localhost:8000/api/v1`

---

## 👥 ROUTER DE PACIENTES

**Prefijo**: `/pacientes`

### GET `/pacientes/` 
Listar todos los pacientes (con paginación)
- **Query params**: 
  - `skip`: número de registros a saltar (default: 0)
  - `limit`: cantidad de registros a retornar (default: 10, máximo: 100)
- **Respuesta**: Objeto con `total` y `pacientes[]`

### POST `/pacientes/`
Crear un nuevo paciente
- **Body JSON**:
  ```json
  {
    "nombre": "Juan",
    "apellido": "Pérez",
    "telefono": "1234567890",
    "fecha_nacimiento": "1990-05-15"
  }
  ```
- **Respuesta**: Objeto paciente con `id, nombre, apellido, ...`

### GET `/pacientes/{paciente_id}`
Obtener un paciente específico
- **Parámetro**: `paciente_id` (número)
- **Respuesta**: Objeto paciente completo

### PUT `/pacientes/{paciente_id}`
Actualizar datos de un paciente
- **Parámetro**: `paciente_id`
- **Body JSON**: Solo los campos a actualizar
- **Respuesta**: Paciente actualizado

### DELETE `/pacientes/{paciente_id}`
Eliminar un paciente
- **Parámetro**: `paciente_id`
- **Respuesta**: Mensaje de confirmación

### GET `/pacientes/buscar/nombre?q=termo`
Buscar pacientes por nombre
- **Query params**: `q` (término de búsqueda, mínimo 1 carácter)
- **Respuesta**: Objeto con `total` y `pacientes[]`

---

## 🎮 ROUTER DE JUEGOS

**Prefijo**: `/juegos`

### Juegos Activos (Generales)

#### GET `/juegos/`
Listar todos los juegos activos
- **Query params** (opcional): 
  - `paciente_id`: filtrar por paciente específico
- **Respuesta**: Objeto con `total` y `juegos[]`

#### GET `/juegos/{juego_id}`
Obtener un juego activo específico
- **Parámetro**: `juego_id`
- **Respuesta**: Objeto juego completo

#### DELETE `/juegos/{juego_id}`
Eliminar un juego activo
- **Parámetro**: `juego_id`
- **Respuesta**: Mensaje de confirmación

#### PATCH `/juegos/{juego_id}/desactivar`
Desactivar un juego (marcar como inactivo)
- **Parámetro**: `juego_id`
- **Respuesta**: Objeto con mensaje y juego desactivado

---

### 👹 Bosses

#### POST `/juegos/bosses`
Crear un nuevo boss
- **Body JSON**:
  ```json
  {
    "nombre": "Satan",
    "dificultad": "Hard",
    "descripcion": "Boss final del juego",
    "estrategias": "Evitar ataques de fuego"
  }
  ```
- **Respuesta**: Boss creado con `id`

#### GET `/juegos/bosses`
Listar todos los bosses disponibles
- **Respuesta**: Array de bosses

#### GET `/juegos/bosses/{boss_id}`
Obtener un boss específico
- **Parámetro**: `boss_id`
- **Respuesta**: Objeto boss completo

#### PUT `/juegos/bosses/{boss_id}`
Actualizar datos de un boss
- **Parámetro**: `boss_id`
- **Body JSON**: Solo los campos a actualizar
- **Respuesta**: Boss actualizado

#### DELETE `/juegos/bosses/{boss_id}`
Eliminar un boss
- **Parámetro**: `boss_id`
- **Respuesta**: Mensaje de confirmación

---

### 🎮 The Binding of Isaac (TBOI)

#### POST `/juegos/pacientes/{paciente_id}/tboi`
Crear un nuevo juego de TBOI para un paciente
- **Parámetro**: `paciente_id`
- **Body JSON**:
  ```json
  {
    "personaje": "Blue Baby",
    "progreso_pisos": 5,
    "items_recolectados": "Chocolate milk, Magic fingers",
    "logros": "Primer piso completado",
    "dificultad": "Normal",
    "boss_id": 1,
    "cronograma_semanal": "Lunes y Viernes",
    "frase_semanal": "Vencer 3 bosses",
    "objetivos": "Llegar al piso 10",
    "recompensas": "Puntos de psicología",
    "corazones": 6,
    "keys": 2,
    "bombas": 5,
    "monedas": 50,
    "notas": "El paciente progresa bien"
  }
  ```
- **Respuesta**: Juego TBOI creado con `id`

#### GET `/juegos/pacientes/{paciente_id}/tboi`
Obtener todos los juegos de TBOI de un paciente
- **Parámetro**: `paciente_id`
- **Respuesta**: Objeto con `total` y `juegos[]`

#### PUT `/juegos/tboi/{juego_id}`
Actualizar datos completos de un juego TBOI
- **Parámetro**: `juego_id`
- **Body JSON**: Solo los campos a actualizar
- **Respuesta**: TBOI actualizado

#### PATCH `/juegos/tboi/{juego_id}/progreso`
Actualizar solo el progreso de un juego TBOI
- **Parámetro**: `juego_id`
- **Query params**:
  - `progreso_pisos`: número opcional
  - `logros`: texto opcional
- **Respuesta**: Objeto con mensaje y juego actualizado

---

### 🏗️ Minecraft

#### POST `/juegos/pacientes/{paciente_id}/minecraft`
Crear un nuevo juego de Minecraft para un paciente
- **Parámetro**: `paciente_id`
- **Body JSON**:
  ```json
  {
    "nombre_mundo": "Mi Mundo",
    "modo_juego": "Creative",
    "bioma_actual": "Forest",
    "notas": "Construcción de casa de piedra"
  }
  ```
- **Respuesta**: Juego Minecraft creado con `id`

---

## 💡 Notas Generales

1. **Errores comunes**:
   - `404`: Recurso no encontrado (paciente, juego, boss no existe)
   - `500`: Error del servidor (revisar logs)
   - `422`: Datos inválidos en el body (revisar formato)

2. **Headers requeridos**:
   - `Content-Type: application/json` (solo para POST, PUT, PATCH)

3. **WebSocket** (notificaciones en tiempo real):
   - Los cambios de pacientes se notifican automáticamente a clientes conectados
   - Tipos de eventos: `paciente_nuevo`, `paciente_actualizado`, `paciente_eliminado`

4. **Paginación**:
   - Use `skip` y `limit` para listar grandes cantidades de pacientes

---

## 📋 Ejemplos rápidos (en JavaScript/Fetch)

### Crear paciente
```javascript
fetch('/api/v1/pacientes/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    nombre: 'Juan',
    apellido: 'Pérez',
    telefono: '1234567890',
    fecha_nacimiento: '1990-05-15'
  })
}).then(r => r.json()).then(console.log)
```

### Listar pacientes
```javascript
fetch('/api/v1/pacientes/?skip=0&limit=10')
  .then(r => r.json())
  .then(console.log)
```

### Crear juego TBOI
```javascript
fetch('/api/v1/juegos/pacientes/1/tboi', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    personaje: 'Blue Baby',
    progreso_pisos: 5,
    dificultad: 'Normal',
    corazones: 6
  })
}).then(r => r.json()).then(console.log)
```

### Buscar paciente por nombre
```javascript
fetch('/api/v1/pacientes/buscar/nombre?q=Juan')
  .then(r => r.json())
  .then(console.log)
```

---

**Última actualización**: 7 de mayo de 2026
