# TaskWise IA Backend

Backend para **TaskWise IA** usando FastAPI + MongoDB (Motor async) con autenticación JWT.

## Requisitos
- Python 3.10+
- MongoDB en ejecución (local)

## Configuración
1. Copia el archivo de variables de entorno:
   ```bash
   cp .env.example .env
   ```
2. Ajusta los valores según tu entorno.

Variables principales:
- `MONGO_URI` (por defecto `mongodb://localhost:27017`)
- `MONGO_DB` (por defecto `taskwise`)
- `JWT_SECRET`
- `JWT_EXPIRE_MINUTES`
- `AI_ENABLED` (true/false)
- `AI_API_KEY` (opcional)
- `AI_BASE_URL` (opcional)
- `AI_MODEL` (opcional)

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Tests
```bash
pytest
```

## Endpoints
- `POST /auth/register`
- `POST /auth/login`
- `GET /tasks`
- `POST /tasks`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`
- `POST /tasks/ai/suggest`

El token JWT se devuelve en la respuesta y debe enviarse como `Authorization: Bearer <token>`.
