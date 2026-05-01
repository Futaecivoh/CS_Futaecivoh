from fastapi import FastAPI
from schemas import UserCreate
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Form
from dotenv import load_dotenv
import bleach

def clean_text(text: str):
    allowed_tags = ['b', 'i', 'u', 'em', 'strong']
    return bleach.clean(text, tags=allowed_tags, attributes={}, strip=True)

app = FastAPI(title="файловый менеджер")
templates = Jinja2Templates(directory="../templates")

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    policy = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self';"
    )

    response.headers["Content-Security-Policy"] = policy
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
