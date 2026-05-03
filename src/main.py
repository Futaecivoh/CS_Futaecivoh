from fastapi import FastAPI
from schemas import UserCreate
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Depends,HTTPException, Form
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
import bleach

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
