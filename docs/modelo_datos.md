# Modelo de datos

## Usuario
Colección: `users`

```json
{
  "_id": "uuid",
  "email": "user@example.com",
  "hashed_password": "bcrypt_hash",
  "created_at": "2025-01-01T10:00:00Z"
}
```

## Tarea
Colección: `tasks`

```json
{
  "_id": "uuid",
  "user_id": "uuid",
  "title": "Preparar presentación",
  "description": "Texto opcional",
  "priority": "ALTA",
  "status": "PENDIENTE",
  "due_date": "2025-01-15T00:00:00Z",
  "created_at": "2025-01-01T10:00:00Z"
}
```

## Enumeraciones
- `priority`: ALTA | MEDIA | BAJA
- `status`: PENDIENTE | EN_PROGRESO | COMPLETADA
