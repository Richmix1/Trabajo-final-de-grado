# TaskWise IA Backend

Backend inicial para **TaskWise IA** usando FastAPI + MongoDB (Motor async).

## Requisitos
- Python 3.10+
- MongoDB en ejecución

## Configuración
1. Copia el archivo de variables de entorno:
   ```bash
   cp .env.example .env
   ```
2. Ajusta los valores según tu entorno.

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints iniciales
- `POST /auth/register`
- `POST /auth/login`
- `GET /tasks`
- `POST /tasks`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`
- `POST /tasks/ai/suggest`

El token JWT se devuelve en la respuesta y debe enviarse como `Authorization: Bearer <token>`.
