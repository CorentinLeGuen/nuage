from fastapi import Depends, HTTPException, Form
from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.auth import auth_router
from app.auth import get_current_user
from app.database import create_tables
from app.database import get_db
from app.models import User
from app.storage import upload_to_minio, download_from_minio, list_stored_files, delete_stored_file

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


@app.get("/files")
async def list_files(user: User = Depends(get_current_user)):
    try:
        files = list_stored_files(user.username)
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), folder: str = Form(""), user: User = Depends(get_current_user)):
    file_key = f"{user.username}/{folder}/{file.filename}" if folder else f"{user.username}/{file.filename}"

    try:
        upload_to_minio(file_key, file)

        return {"message": "File uploaded successfully", "file_name": file.filename, "folder": folder}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete/{file_name}")
async def delete_file(file_name: str, user: User = Depends(get_current_user)):
    file_key = f"{user.username}/{file_name}"

    try:
        delete_stored_file(file_key)
        return {"message": f"File {file_name} deleted successfully"}
    except Exception as e:
        return {"error": "Delete failed"}, 500



@app.get("/download/{file_name}")
async def download(file_name: str, user: User = Depends(get_current_user)):
    file_key = f"{user.username}/{file_name}"

    print(f"\t-> {file_key}")
    response = download_from_minio(file_key)
    file_stream = response["Body"]

    return StreamingResponse(
        file_stream,
        media_type="application/octet-stream",
        headers={
            "Content-disposition": "attachment;filename=" + file_name,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "*"
        }
    )


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
