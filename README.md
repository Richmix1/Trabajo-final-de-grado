# TaskWise IA (TFG DAM)

Proyecto de Trabajo de Fin de Grado (DAM, España) para una aplicación web sencilla de gestión de tareas con sugerencias de IA. Incluye backend en FastAPI y frontend en React + Vite.

## Requisitos
- **Python 3.10+**
- **Node.js 18+** (recomendado)
- **MongoDB local** instalado en Windows (sin Docker)

## Instalación de MongoDB en Windows (resumen)
1. Descarga **MongoDB Community Server** desde: https://www.mongodb.com/try/download/community
2. Instala con el servicio de Windows habilitado.
3. Comprueba el servicio:
   - Abre `Servicios` y confirma que **MongoDB Server** está en ejecución.
   - Si no, inicia el servicio manualmente.
4. Alternativa por consola:
   - Abre PowerShell y ejecuta:
     ```powershell
     "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath C:\data\db
     ```
   - Crea `C:\data\db` si no existe.

## Estructura del proyecto
```
/backend  -> FastAPI + MongoDB
/frontend -> React + Vite
/docs     -> documentación técnica
```

## Backend
Consulta el README específico en [`/backend/README.md`](./backend/README.md).

## Frontend
Consulta el README específico en [`/frontend/README.md`](./frontend/README.md).

## Variables de entorno
Ejemplos en:
- Backend: [`/backend/.env.example`](./backend/.env.example)
- Frontend: [`/frontend/.env.example`](./frontend/.env.example)

## Ejemplos CURL
### Registro
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@taskwise.com", "password":"supersecreto"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@taskwise.com", "password":"supersecreto"}'
```

### Crear tarea
```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"title":"Preparar memoria", "priority":"ALTA", "status":"PENDIENTE"}'
```

### Sugerencia IA
```bash
curl -X POST http://127.0.0.1:8000/tasks/ai/suggest \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"title":"Entregar informe", "description":"Versión inicial", "due_date":"2025-01-15T00:00:00"}'
```

## Notas de seguridad y limitaciones (TFG)
- El proyecto usa JWT y hashing con bcrypt, pero no incluye refresh tokens ni rotación de claves.
- El motor de IA es opcional y se apoya en un proveedor compatible con OpenAI; si falla, hay un fallback determinista.
- Las validaciones están pensadas para un entorno académico y no sustituyen auditorías de seguridad.

## Documentación técnica
Disponible en la carpeta [`/docs`](./docs):
- Arquitectura
- Endpoints
- Modelo de datos
