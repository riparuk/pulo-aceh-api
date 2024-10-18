from sqlalchemy.orm import Session
from .models import User, Place, user_place_association
from .schemas import UserCreate, PlaceCreate, UserUpdate, PlaceUpdate
from .utils import hash_password, verify_password
from typing import List, Optional

# ------------------ CRUD User ------------------

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        photo_url=user.photo_url,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = user.name or db_user.name
        db_user.email = user.email or db_user.email
        db_user.is_admin = user.is_admin if user.is_admin is not None else db_user.is_admin
        db_user.photo_url = user.photo_url or db_user.photo_url
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def save_place_to_user(db: Session, user_id: int, place_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    place = db.query(Place).filter(Place.id == place_id).first()
    if user and place:
        # Check if the place is already saved by the user
        if place in user.saved_places:
            return {"message": "Place already saved to user's list."}
        
        # If not saved, append the place and commit the transaction
        user.saved_places.append(place)
        db.commit()
        return user
    return {"message": "User or place not found."}

def unsave_place_from_user(db: Session, user_id: int, place_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    place = db.query(Place).filter(Place.id == place_id).first()
    if user and place:
        # Check if the place is saved by the user
        if place not in user.saved_places:
            return {"message": "Place not found in user's saved list."}
        
        # If saved, remove the place and commit the transaction
        user.saved_places.remove(place)
        db.commit()
        return user
    return {"message": "User or place not found."}

# ------------------ CRUD Place ------------------

def get_place_by_id(db: Session, place_id: int):
    return db.query(Place).filter(Place.id == place_id).first()

def get_places(db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None, min_rating: Optional[float] = None):
    query = db.query(Place)
    if search:
        query = query.filter(Place.name.ilike(f'%{search}%'))
    if min_rating is not None:
        query = query.filter(Place.rating >= min_rating)
    return query.offset(skip).limit(limit).all()

def create_place(db: Session, place: PlaceCreate):
    db_place = Place(
        name=place.name,
        description=place.description,
        location_name=place.location_name,
        latitude=place.latitude,
        longitude=place.longitude,
        rating=place.rating,
        image_url=place.image_url
    )
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

def update_place(db: Session, place_id: int, place: PlaceUpdate):
    db_place = db.query(Place).filter(Place.id == place_id).first()
    if db_place:
        db_place.name = place.name or db_place.name
        db_place.description = place.description or db_place.description
        db_place.location_name = place.location_name or db_place.location_name
        db_place.latitude = place.latitude or db_place.latitude
        db_place.longitude = place.longitude or db_place.longitude
        db_place.rating = place.rating if place.rating is not None else db_place.rating
        db_place.image_url = place.image_url or db_place.image_url
        db.commit()
        db.refresh(db_place)
    return db_place

def delete_place(db: Session, place_id: int):
    db_place = db.query(Place).filter(Place.id == place_id).first()
    if db_place:
        db.delete(db_place)
        db.commit()
    return db_place