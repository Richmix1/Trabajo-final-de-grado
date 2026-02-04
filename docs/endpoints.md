# Endpoints

## Auth
### POST /auth/register
- **Descripción**: registro de usuario.
- **Body**:
  ```json
  {"email": "user@example.com", "password": "supersecreto"}
  ```
- **Respuesta**:
  ```json
  {"access_token": "...", "token_type": "bearer"}
  ```

### POST /auth/login
- **Descripción**: login y obtención de JWT.
- **Body**:
  ```json
  {"email": "user@example.com", "password": "supersecreto"}
  ```

## Tasks (JWT)
### GET /tasks
- **Descripción**: lista tareas del usuario.

### POST /tasks
- **Descripción**: crea una tarea.
- **Body**:
  ```json
  {
    "title": "Preparar entrega",
    "description": "Notas y demo",
    "priority": "ALTA",
    "status": "PENDIENTE",
    "due_date": "2025-01-15T00:00:00"
  }
  ```

### PUT /tasks/{task_id}
- **Descripción**: actualiza una tarea.

### DELETE /tasks/{task_id}
- **Descripción**: elimina una tarea.

## IA (JWT)
### POST /tasks/ai/suggest
- **Descripción**: sugiere prioridad y descripción.
- **Body**:
  ```json
  {"title": "Preparar informe", "description": "Borrador", "due_date": "2025-01-15T00:00:00"}
  ```
- **Respuesta**:
  ```json
  {"priority_suggested": "MEDIA", "description_generated": "..."}
  ```
