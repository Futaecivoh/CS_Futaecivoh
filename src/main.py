from fastapi import FastAPI
from schemas import UserCreate
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import FastAPI, Request, Depends,HTTPException, Form, UploadFile, File
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
import bleach
import uuid
import os
import shutil
import filetype
from cryptography.fernet import Fernet
from io import BytesIO
from fastapi.responses import StreamingResponse

load_dotenv("../.env")

key = os.getenv("ENCRYPTION_KEY")
if not key:
    raise RuntimeError("ENCRYPTION_KEY is missing in .env file!")
cipher_suite = Fernet(key.encode())

def clean_text(text: str):
    allowed_tags = ['b', 'i', 'u', 'em', 'strong']
    return bleach.clean(text, tags=allowed_tags, attributes={}, strip=True)

app = FastAPI(title="файловый менеджер")
templates = Jinja2Templates(directory="../templates")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-change-in-production-12345")

users_db = {
    "alice": {"username": "alice", "role": "user", "password": "123"},
    "bob": {"username": "bob", "role": "user", "password": "456"},
    "admin": {"username": "admin", "role": "admin", "password": "000"},
}

files_db = [
    {"id": 1, "filename": "report_alice.pdf", "owner": "alice", "size": 1024},
    {"id": 2, "filename": "photo_bob.jpg", "owner": "bob", "size": 2048},
    {"id": 3, "filename": "admin_keys.txt", "owner": "admin", "size": 12},
]

def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    return user

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    user = users_db.get(username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if user["password"] != password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    request.session["user"] = {
        "username": user["username"],
        "role": user["role"]
    }

    return {
        "status": "ok"
    }

def check_file_permissions(file_id: int, user: dict = Depends(get_current_user)):
    file = next((f for f in files_db if f["id"] == file_id), None)

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    is_owner = file["owner"] == user["username"]
    is_admin = user["role"] == "admin"

    if not (is_owner or is_admin):
        raise HTTPException(status_code=404, detail="File not found")

    return file

@app.middleware("http")
async def add_security_headers(request: Request, call_next):

    response = await call_next(request)

    if request.url.path in [
        "/docs",
        "/redoc",
        "/openapi.json"
    ]:
        return response

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self';"
    )

    return response

@app.post("/registration")
def register_user(user: UserCreate):
    return {"msg": "User created", "user": user.username}

comments_db = []

@app.get("/comments", response_class=HTMLResponse)
async def get_comments(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="comments.html",
    context={"comments": comments_db}
)

@app.post("/comments")
async def post_comment(request: Request, text: str = Form(...)):
    safe_text = clean_text(text)
    comments_db.append(safe_text)
    return templates.TemplateResponse(
    request=request,
    name="comments.html",
    context={"comments": comments_db}
)

@app.get("/files/my")
def get_my_files(user: dict = Depends(get_current_user)):
    my_files = [f for f in files_db if f["owner"] == user["username"]]
    return my_files

@app.get("/files/all")
def get_all_files(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return files_db

@app.get("/files/{file_id}")
def get_file(file: dict = Depends(check_file_permissions)):
    return file

@app.get("/files/{file_id}/download")
def download_file(
    file: dict = Depends(check_file_permissions)
):
    file_path = file.get("path")
    original_name = file.get("filename")

    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    if not file.get("is_encrypted"):
         return FileResponse(
            path=file_path,
            filename=original_name,
            media_type="application/octet-stream"
        )

    with open(file_path, "rb") as f:
        encrypted_data = f.read()

    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data)
    except Exception:

        raise HTTPException(status_code=500, detail="Failed to decrypt file.")

    return StreamingResponse(
        BytesIO(decrypted_data),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={original_name}"}
    )

@app.delete("/files/{file_id}")
def delete_file(
    file: dict = Depends(check_file_permissions)
):
    files_db[:] = [
        f for f in files_db
        if f["id"] != file["id"]
    ]

    return {
        "status": "deleted",
        "file_id": file["id"]
    }

MAX_FILE_SIZE = 2 * 1024 * 1024
STORAGE_DIR = "../storage"

@app.post("/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    encrypt: bool = False,
    user: dict = Depends(get_current_user)
):
    head = await file.read(2048)
    kind = filetype.guess(head)

    is_valid_image = kind is not None and kind.mime in ["image/jpeg", "image/png"]
    is_text_file = file.filename.endswith(".txt")

    if not (is_valid_image or is_text_file):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only JPEG, PNG and TXT are allowed."
        )

    await file.seek(0)

    new_filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    file_path = os.path.join(STORAGE_DIR, new_filename)

    file_data = await file.read()

    if len(file_data) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File is too large.")

    if encrypt:
        file_data = cipher_suite.encrypt(file_data)

    with open(file_path, "wb") as buffer:
        buffer.write(file_data)

    total_size = 0

    new_id = max([f["id"] for f in files_db] + [0]) + 1

    file_meta = {
        "id": new_id,
        "filename": file.filename,
        "path": file_path,
        "owner": user["username"],
        "size": total_size,
        "is_encrypted": encrypt
    }

    files_db.append(file_meta)

    return {"message": "File uploaded successfully", "file_id": new_id, "encrypted": encrypt}
