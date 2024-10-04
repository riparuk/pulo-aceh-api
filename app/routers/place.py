from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.schemas import PlaceCreate, PlaceResponse, PlaceUpdate
from app.db.crud import get_place_by_id, get_places, create_place, update_place, delete_place
from app.db.database import get_db

router = APIRouter(
    prefix="/places",
    tags=["places"],
    responses={404: {"description": "Not Found"}},
)

# ------------------ Get List of Places ------------------

@router.get("/", response_model=List[PlaceResponse])
def read_places(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), search: str = None):
    places = get_places(db=db, skip=skip, limit=limit, search=search)
    return places

# ------------------ Get Place by ID ------------------

@router.get("/{place_id}", response_model=PlaceResponse)
def read_place(place_id: int, db: Session = Depends(get_db)):
    db_place = get_place_by_id(db=db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return db_place

# ------------------ Create New Place ------------------

@router.post("/", response_model=PlaceResponse, status_code=status.HTTP_201_CREATED)
def create_new_place(place: PlaceCreate, db: Session = Depends(get_db)):
    return create_place(db=db, place=place)

# ------------------ Update Place ------------------

@router.put("/{place_id}", response_model=PlaceResponse)
def update_existing_place(place_id: int, place: PlaceUpdate, db: Session = Depends(get_db)):
    db_place = get_place_by_id(db=db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    return update_place(db=db, place_id=place_id, place=place)

# ------------------ Delete Place ------------------

@router.delete("/{place_id}", response_model=PlaceResponse)
def delete_existing_place(place_id: int, db: Session = Depends(get_db)):
    db_place = get_place_by_id(db=db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    return delete_place(db=db, place_id=place_id)