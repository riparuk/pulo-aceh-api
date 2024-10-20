from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List

from app.auth.jwt import get_current_user
from app.db.schemas import PlaceCreate, PlaceResponse, PlaceUpdate, UserResponse
from app.db.crud import get_place_by_id, get_places, create_place, update_place, delete_place
from app.db.database import get_db
from app.dependencies import SECRET_KEY
from geopy.distance import geodesic

router = APIRouter(
    prefix="/places",
    tags=["places"],
    responses={404: {"description": "Not Found"}},
)

# ------------------ Get List of Places ------------------

@router.get("/", response_model=List[PlaceResponse])
def read_places(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), search: str = None, min_rating: float = None):
    places = get_places(db=db, skip=skip, limit=limit, search=search, min_rating=min_rating)
    return places

# ------------------ Get Place by ID ------------------

@router.get("/{place_id}", response_model=PlaceResponse)
def read_place(
    place_id: int,
    user_lat: float | None = None,
    user_lon: float | None = None,
    db: Session = Depends(get_db),
):
    # Ambil data tempat dari database
    db_place = get_place_by_id(db=db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Hitung jarak jika koordinat user diberikan
    distance = None
    if user_lat is not None and user_lon is not None:
        place_location = (db_place.latitude, db_place.longitude)
        user_location = (user_lat, user_lon)
        distance = geodesic(place_location, user_location).kilometers

    # Konversi objek SQLAlchemy ke dictionary
    response = {column.name: getattr(db_place, column.name) for column in db_place.__table__.columns}
    response['distance'] = distance

    return response

# ------------------ Create New Place ------------------

@router.post("/", response_model=PlaceResponse, status_code=status.HTTP_201_CREATED)
def create_new_place(current_user: Annotated[UserResponse, Depends(get_current_user)], place: PlaceCreate, db: Session = Depends(get_db), secret_key: str = None):
    if secret_key != SECRET_KEY and current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Invalid secret key for admin registration and unauthorized user")
    
    return create_place(db=db, place=place)

# ------------------ Update Place ------------------

@router.put("/{place_id}", response_model=PlaceResponse)
def update_existing_place(current_user: Annotated[UserResponse, Depends(get_current_user)], place_id: int, place: PlaceUpdate, db: Session = Depends(get_db), secret_key: str = None):
    if secret_key != SECRET_KEY and current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Invalid secret key for admin registration and unauthorized user")
    
    db_place = get_place_by_id(db=db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    return update_place(db=db, place_id=place_id, place=place)

# ------------------ Delete Place ------------------

@router.delete("/{place_id}", response_model=PlaceResponse)
def delete_existing_place(current_user: Annotated[UserResponse, Depends(get_current_user)], place_id: int, db: Session = Depends(get_db), secret_key: str = None):
    if secret_key != SECRET_KEY and current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Invalid secret key for admin registration and unauthorized user")
    
    db_place = get_place_by_id(db=db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    return delete_place(db=db, place_id=place_id)