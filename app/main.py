from fastapi import Depends
from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import auth_router
from app.auth import get_current_user
from app.database import create_tables
from app.database import get_db
from app.models import User
from app.storage import upload_to_minio, download_from_minio

app = FastAPI(title="SecureCloud", version="1.0")
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await create_tables()


@app.get("/")
async def home(user: dict = Depends(get_current_user)):
    return {"message": f"Welcome {user['username']}!"}


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    data = await file.read()
    return {"message": upload_to_minio(file.filename, data)}


@app.get("/download/{file_name}")
async def download(file_name: str):
    return {"file": file_name, "content": download_from_minio(file_name)}


@app.websocket("/sync")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("WebSocket connection active")
    while True:
        data = await websocket.receive_text()
        print(f"New update : {data}")


@app.get("/users/")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(User.__table__.select())
    users = result.scalars().all()
    return users
