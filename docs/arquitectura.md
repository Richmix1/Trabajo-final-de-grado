# Arquitectura

## Visión general
TaskWise IA se divide en dos aplicaciones independientes:

- **Frontend (React + Vite)**: interfaz de usuario para registro, login y gestión de tareas.
- **Backend (FastAPI + MongoDB)**: API REST con autenticación JWT y lógica de IA.

## Componentes
- **Frontend**
  - `App.jsx`: gestiona el flujo de autenticación, listado y formulario de tareas.
  - `api.js`: capa de comunicación HTTP con el backend.

- **Backend**
  - `app/main.py`: configuración de FastAPI y CORS.
  - `app/routers/auth.py`: endpoints de registro y login.
  - `app/routers/tasks.py`: CRUD de tareas.
  - `app/routers/ai.py`: endpoint de sugerencias IA.
  - `app/services/ai.py`: lógica de IA con fallback determinista.
  - `app/db/mongo.py`: conexión asíncrona a MongoDB.

## Flujo de autenticación
1. El usuario se registra o inicia sesión.
2. El backend genera un JWT con `sub = user_id`.
3. El frontend guarda el token en `localStorage` y lo envía en cada petición.

## IA y fallback
- Si `AI_ENABLED=true` y hay `AI_API_KEY`, el backend llama a un proveedor compatible con OpenAI.
- Si falla o no hay clave, se usa un algoritmo local determinista para sugerir prioridad y descripción.

## Seguridad
- Contraseñas con hashing bcrypt.
- JWT firmado con secreto configurable.
- CORS limitado a `localhost:5173`.
