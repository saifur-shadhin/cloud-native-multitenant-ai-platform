from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from sqlalchemy.orm import Session
from fastapi import Depends

from backend.app.core.database import get_db
from backend.app.models.user import User as UserModel
from backend.app.models.organization import Organization

app=FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int = Field(ge=1, le=100)

# GET all users
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@app.post("/users")
def create_user(user: User):
    for existing_user in users:
        if existing_user.id == user.id:
            raise HTTPException(
                status_code=400,
                detail="User ID already exists"
            )

    users.append(user)
    return user

# GET single user
@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


# PUT - update user
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            users[index] = updated_user
            return updated_user

    raise HTTPException(status_code=404, detail="User not found")


# DELETE - delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user

    raise HTTPException(status_code=404, detail="User not found")


# Root
@app.get("/")
def root():
    return {
        "message": "Cloud-Native Multi-Tenant AI Platform is running!"
    }
@app.get("/organizations")
def get_organizations(db: Session = Depends(get_db)):
    organizations = db.query(Organization).all()
    return organizations

@app.get("/organizations/{organization_id}/users")
def get_organization_users(
    organization_id: int,
    db: Session = Depends(get_db)
):
    users = db.query(UserModel).filter(
        UserModel.organization_id == organization_id
    ).all()

    return users
