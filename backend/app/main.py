from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.mongo import close_mongo_connection, connect_to_mongo, get_database
from app.routers.ai import router as ai_router
from app.routers.auth import router as auth_router
from app.routers.tasks import router as tasks_router

app = FastAPI(title="TaskWise IA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(ai_router)


@app.on_event("startup")
async def on_startup() -> None:
    connect_to_mongo()
    db = get_database()
    await db.users.create_index("email", unique=True)
    await db.tasks.create_index("user_id")


@app.on_event("shutdown")
def on_shutdown() -> None:
    close_mongo_connection()
