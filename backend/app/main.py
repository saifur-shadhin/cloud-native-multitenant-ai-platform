from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.user import User as UserModel
from backend.app.models.organization import Organization


app = FastAPI()


# =========================
# Pydantic Schemas
# =========================

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int = Field(ge=1, le=100)


class UserCreate(BaseModel):
    name: str
    email: str
    age: int = Field(ge=1, le=100)
    organization_id: int


class OrganizationCreate(BaseModel):
    name: str


# =========================
# Root
# =========================

@app.get("/")
def root():
    return {
        "message": "Cloud-Native Multi-Tenant AI Platform is running!"
    }


# =========================
# User APIs
# =========================

# GET all users
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

# GET single user
@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

# PUT - update user
@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    updated_user: UserCreate,
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.name = updated_user.name
    user.email = updated_user.email
    user.age = updated_user.age
    user.organization_id = updated_user.organization_id

    db.commit()
    db.refresh(user)

    return user
# DELETE user
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }

# POST create user
@app.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    organization = db.query(Organization).filter(
        Organization.id == user.organization_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    new_user = UserModel(
        name=user.name,
        email=user.email,
        age=user.age,
        organization_id=user.organization_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================
# Organization APIs
# =========================

# GET all organizations
@app.get("/organizations")
def get_organizations(db: Session = Depends(get_db)):
    organizations = db.query(Organization).all()
    return organizations


# POST create organization
@app.post("/organizations")
def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db)
):
    existing_organization = db.query(Organization).filter(
        Organization.name == organization.name
    ).first()

    if existing_organization:
        raise HTTPException(
            status_code=400,
            detail="Organization already exists"
        )

    new_organization = Organization(
        name=organization.name
    )

    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)

    return new_organization


# POST create user inside an organization
@app.post("/organizations/{organization_id}/users")
def create_organization_user(
    organization_id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    organization = db.query(Organization).filter(
        Organization.id == organization_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    new_user = UserModel(
        name=user.name,
        email=user.email,
        age=user.age,
        organization_id=organization_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# GET users of a specific organization
@app.get("/organizations/{organization_id}/users")
def get_organization_users(
    organization_id: int,
    db: Session = Depends(get_db)
):
    organization = db.query(Organization).filter(
        Organization.id == organization_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    users = db.query(UserModel).filter(
        UserModel.organization_id == organization_id
    ).all()

    return users
