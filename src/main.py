from fastapi import FastAPI
from schemas import UserCreate

app = FastAPI(title="файловый менеджер")

@app.post("/registration")
def register_user(user: UserCreate):   
    return {"msg": "User created", "user": user.username}