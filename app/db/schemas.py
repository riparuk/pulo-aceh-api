
from pydantic import BaseModel, EmailStr, condecimal
from typing import Optional, List

# ------------------ User Schemas ------------------

class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    photo_url: Optional[str] = None
    
class PlaceBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[condecimal(max_digits=10, decimal_places=6)] = None
    longitude: Optional[condecimal(max_digits=10, decimal_places=6)] = None
    rating: Optional[float] = 0.0
    image_url: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    hashed_password: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    photo_url: Optional[str] = None

class UserResponse(UserBase):
    id: int
    saved_places: Optional[List[PlaceBase]] = []

    class Config:
        orm_mode = True

# ------------------ Admin Schemas ------------------

class AdminBase(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True

class AdminCreate(AdminBase):
    username: str
    hashed_password: str

class AdminUpdate(AdminBase):
    name: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None

class AdminResponse(AdminBase):
    id: int

    class Config:
        orm_mode = True

# ------------------ Place Schemas ------------------

class PlaceCreate(PlaceBase):
    name: str
    latitude: condecimal(max_digits=10, decimal_places=6)
    longitude: condecimal(max_digits=10, decimal_places=6)

class PlaceUpdate(PlaceBase):
    name: Optional[str] = None
    description: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[condecimal(max_digits=10, decimal_places=6)] = None
    longitude: Optional[condecimal(max_digits=10, decimal_places=6)] = None
    rating: Optional[float] = None
    image_url: Optional[str] = None

class PlaceResponse(PlaceBase):
    id: int
    users: Optional[List[UserBase]] = []

    class Config:
        orm_mode = True