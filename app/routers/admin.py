from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import crud, schemas, models
from app.db.database import get_db

router = APIRouter(
    prefix="/admins",
    tags=["admins"],
    responses={404: {"description": "Not Found"}},
)

@router.post("/", response_model=schemas.AdminCreate)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = crud.get_admin_by_username(db, username=admin.username)
    if db_admin:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_admin(db=db, admin=admin)

@router.get("/", response_model=List[schemas.AdminResponse])
def read_admins(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    admins = crud.get_admins(db, skip=skip, limit=limit)
    return admins

@router.get("/{admin_id}", response_model=schemas.AdminResponse)
def read_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = crud.get_admin_by_id(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin

@router.put("/{admin_id}", response_model=schemas.AdminResponse)
def update_admin(admin_id: int, admin: schemas.AdminUpdate, db: Session = Depends(get_db)):
    db_admin = crud.get_admin_by_id(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return crud.update_admin(db=db, admin_id=admin_id, admin=admin)

@router.delete("/{admin_id}", response_model=schemas.AdminResponse)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = crud.get_admin_by_id(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return crud.delete_admin(db=db, admin_id=admin_id)