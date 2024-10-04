from sqlalchemy.orm import Session
from .models import User, Admin, Place, user_place_association
from .schemas import UserCreate, AdminCreate, PlaceCreate, UserUpdate, AdminUpdate, PlaceUpdate
from typing import List, Optional

# ------------------ CRUD User ------------------

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=user.hashed_password,
        is_active=user.is_active,
        photo_url=user.photo_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = user.name or db_user.name
        db_user.email = user.email or db_user.email
        db_user.is_active = user.is_active if user.is_active is not None else db_user.is_active
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

# ------------------ CRUD Admin ------------------

def get_admin_by_id(db: Session, admin_id: int):
    return db.query(Admin).filter(Admin.id == admin_id).first()

def get_admin_by_username(db: Session, username: str):
    return db.query(Admin).filter(Admin.username == username).first()

def create_admin(db: Session, admin: AdminCreate):
    db_admin = Admin(
        name=admin.name,
        username=admin.username,
        hashed_password=admin.hashed_password,
        is_active=admin.is_active
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def update_admin(db: Session, admin_id: int, admin: AdminUpdate):
    db_admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if db_admin:
        db_admin.name = admin.name or db_admin.name
        db_admin.username = admin.username or db_admin.username
        db_admin.is_active = admin.is_active if admin.is_active is not None else db_admin.is_active
        db.commit()
        db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session, admin_id: int):
    db_admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if db_admin:
        db.delete(db_admin)
        db.commit()
    return db_admin

# ------------------ CRUD Place ------------------

def get_place_by_id(db: Session, place_id: int):
    return db.query(Place).filter(Place.id == place_id).first()

def get_places(db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None):
    query = db.query(Place)
    if search:
        query = query.filter(Place.name.ilike(f'%{search}%'))
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