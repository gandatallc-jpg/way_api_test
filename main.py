from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI(title="FastAPI Demo")

@app.get("/") # route зам ямаар нэгэн утгагүй ингээд ирээрэй гэвэл доорх функцийг дуудна.
def root():
    return {"message": "Hello FastAPI 🚀 it's ganchimeg from way academy"} #{} json формайтаар бичээд өгч байна.

@app.get("/health") # route health зам дээр доорх функцийг дуудна.
def health():
    return {"status": "ok"}


@app.get("/users",
         summary="Бүх хэрэглэгчдийг шинэээс хуучин руу жагсаах",
    description="Шинэ нь дээрээ бүх хэрэглэгчдийг жагсаана.")
def list_users(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT id, name FROM users ORDER BY id DESC")).mappings().all()
    return rows
    
    # Доор үйлдлийг дээр код нь нэг мөрөөр бичиж байна.
    #result = db.execute(text("SELECT id, name, email FROM users"))
    #users = [{"id": row.id, "name": row.name, "email": row.email} for row in result]
    #return {"users": users}



@app.get("/users/{user_id}",
    summary="Хэрэглэгчийн мэдээллийг харах",
    description="Хэрэглэгчийн ID-аар хэрэглэгчийн мэдээллийг харна.")
def get_user(user_id: int, db: Session = Depends(get_db)):
    row = db.execute(text("SELECT id, name FROM users WHERE id = :user_id"), {"user_id": user_id}).mappings().first()
    return row