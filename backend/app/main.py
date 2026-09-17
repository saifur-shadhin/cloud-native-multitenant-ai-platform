from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users")
def create_user(user: User):
    return user

@app.get("/")
def root():
    return {"message": "Cloud-Native Multi-Tenant AI Platform is running!"}
