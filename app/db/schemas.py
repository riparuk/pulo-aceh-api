
from datetime import datetime
from pydantic import BaseModel, EmailStr, condecimal
from typing import Optional, List

# ------------------ User Schemas ------------------
    
class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_admin: bool = False
    photo_url: Optional[str] = None
    
class PlaceBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[condecimal(max_digits=10, decimal_places=7)] = None
    longitude: Optional[condecimal(max_digits=10, decimal_places=7)] = None
    image_url: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    is_admin: bool = False
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    
class UserUpdateProfile(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    saved_places: Optional[List[PlaceBase]] = []

    class Config:
        orm_mode = True

# ------------------ Place Schemas ------------------

class PlaceCreate(PlaceBase):
    name: str
    latitude: condecimal(max_digits=10, decimal_places=7)
    longitude: condecimal(max_digits=10, decimal_places=7)

class PlaceUpdate(PlaceBase):
    name: Optional[str] = None
    description: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[condecimal(max_digits=10, decimal_places=7)] = None
    longitude: Optional[condecimal(max_digits=10, decimal_places=7)] = None
    image_url: Optional[str] = None

class PlaceResponse(PlaceBase):
    id: int
    distance: Optional[float] = None
    average_rating: Optional[float] = 0.0
    # users: Optional[List[UserBase]] = []

    class Config:
        orm_mode = True

class RatingCreate(BaseModel):
    rating: float
    message: Optional[str] = None

class RatingResponse(BaseModel):
    id: int
    user_id: int
    place_id: int
    rating: float
    message: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True