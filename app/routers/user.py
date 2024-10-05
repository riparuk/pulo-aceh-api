from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.schemas import UserCreate, UserResponse, UserUpdate
from app.db.crud import authenticate_user, get_user_by_id, get_user_by_email, get_users, create_user, update_user, delete_user, save_place_to_user
from app.db.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)

# ------------------ Get List of Users ------------------

@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db=db, skip=skip, limit=limit)
    return users

# ------------------ Get User by ID ------------------

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ------------------ Register New User ------------------
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return create_user(db=db, user=user)

# ------------------ Login User ------------------
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Login successful"}

# ------------------ Update User ------------------

@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return update_user(db=db, user_id=user_id, user=user)

# ------------------ Delete User ------------------

@router.delete("/{user_id}", response_model=UserResponse)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return delete_user(db=db, user_id=user_id)

# ------------------ Save Place to User ------------------

@router.post("/{user_id}/places/{place_id}")
def save_place_to_user_list(user_id: int, place_id: int, db: Session = Depends(get_db)):
    result  = save_place_to_user(db=db, user_id=user_id, place_id=place_id)
    if isinstance(result, dict):
        # Jika result adalah dictionary, kita kembalikan pesan yang sesuai
        return result
    
    return {"message": "Place saved to user's list successfully"}