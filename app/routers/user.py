from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated, List

from app.auth.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, Token, create_access_token, get_current_active_user
from app.routers.otp import send_otp
from app.db.schemas import UserCreate, UserResponse, UserUpdate, UserUpdateProfile
from app.db.crud import authenticate_user, get_user_by_id, get_user_by_email, get_users, create_user, unsave_place_from_user, update_user, delete_user, save_place_to_user, update_user_photo, verify_otp_by_email
from app.db.database import get_db
from app.dependencies import SECRET_KEY


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}}
)

# ------------------ Get List of Users ------------------

@router.get("/", response_model=List[UserResponse])
def read_users(current_user: Annotated[UserResponse, Depends(get_current_active_user)], skip: int = 0, limit: int = 10, db: Session = Depends(get_db), secret_key: str = None):
    if secret_key != SECRET_KEY and current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Invalid secret key for admin registration and unauthorized user")
        
    users = get_users(db=db, skip=skip, limit=limit)
    return users

# ------------------ Get User by ID ------------------

@router.get("/{user_id}", response_model=UserResponse)
def read_user(current_user: Annotated[UserResponse, Depends(get_current_active_user)], user_id: int, db: Session = Depends(get_db), secret_key: str = None):
    if secret_key != SECRET_KEY and current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Invalid secret key for admin registration and unauthorized user")
    
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ------------------ Verify OTP ------------------
@router.post("/auth/register/verify-otp", status_code=status.HTTP_201_CREATED)
def verify_email_otp(email: str, otp: str, db: Session = Depends(get_db)):
    try:
        is_verified = verify_otp_by_email(db, email, otp)
        
        if not is_verified:
            raise HTTPException(status_code=400, detail="Invalid OTP")
    
        user = get_user_by_email(db=db, email=email)
        print(user)
        
        # Activate the user
        update_user(db=db, user_id=user.id, user=UserUpdate(is_active=True))
        
        return {"message": "User verified successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
# ------------------ Register New User ------------------
@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db), secret_key: str = None):
    if user.is_admin:
        if secret_key != SECRET_KEY:
            raise HTTPException(status_code=403, detail="Invalid secret key for admin registration")
    
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        send_otp(email=user.email, db=db)
        create_user(db=db, user=user)
        return {"message": "Kode OTP telah dikirim ke email"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

# ------------------ forget password with otp ------------------
@router.post("/auth/forget-password-otp", status_code=status.HTTP_201_CREATED)
def change_password_with_otp(email: str, new_password: str, otp: str, db: Session = Depends(get_db)):
    try:
        is_verified = verify_otp_by_email(db, email, otp)
        
        if not is_verified:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        
        user = get_user_by_email(db=db, email=email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return update_user(db=db, user_id=user.id, user=UserUpdate(password=new_password))
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    
# ------------------ Login User ------------------
@router.post("/auth/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# ------------------ Get User Profile ------------------
@router.get("/auth/me", response_model=UserResponse)
async def get_current_user(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
):
    return current_user

# ------------------ Update User Profile Photo ------------------

@router.put("/auth/me/photo", response_model=UserResponse)
async def update_profile_photo(
    photo: Annotated[UploadFile, File(description="A File containing an image")],
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    
    # Assuming you have a function to handle photo update
    updated_user = update_user_photo(db=db, user_id=current_user.id, photo=photo)
    return updated_user

# ------------------ Update User ------------------

@router.put("/auth/me", response_model=UserResponse)
def update_current_user(user: UserUpdateProfile, current_user: Annotated[UserResponse, Depends(get_current_active_user)], db: Session = Depends(get_db), secret_key: str = None):
    if user.is_admin:
        if secret_key != SECRET_KEY:
            raise HTTPException(status_code=403, detail="Invalid secret key for admin editing")
    
    return update_user(db=db, user_id=current_user.id, user=UserUpdate(**user.model_dump()))

# ------------------ change me email with otp ------------------
@router.post("/auth/me/change-email-otp", status_code=status.HTTP_201_CREATED)
def change_email_with_otp(new_email: str, otp: str, current_user: Annotated[UserResponse, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    
    try:
        is_verified = verify_otp_by_email(db, new_email, otp)
        
        if not is_verified:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        
        return update_user(db=db, user_id=current_user.id, user=UserUpdate(email=new_email))
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
# ------------------ Delete User ------------------

@router.delete("/{user_id}", response_model=UserResponse)
def delete_existing_user(current_user: Annotated[UserResponse, Depends(get_current_active_user)], user_id: int, db: Session = Depends(get_db), secret_key: str = None):
    if secret_key != SECRET_KEY and current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Invalid secret key for admin registration and unauthorized user")
    
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return delete_user(db=db, user_id=user_id)

# ------------------ Save Place to User ------------------

@router.post("/save/{place_id}")
def save_place_to_current_user(place_id: int, current_user: Annotated[UserResponse, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    result  = save_place_to_user(db=db, user_id=current_user.id, place_id=place_id)
    if isinstance(result, dict):
        # Jika result adalah dictionary, kita kembalikan pesan yang sesuai
        return result
    
    return {"message": "Place saved to user's list successfully"}

# ------------------ Unsave Place from User ------------------

@router.delete("/unsave/{place_id}")
def unsave_place_from_current_user(place_id: int, current_user: Annotated[UserResponse, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    result = unsave_place_from_user(db=db, user_id=current_user.id, place_id=place_id)
    if isinstance(result, dict):
        # Jika result adalah dictionary, kita kembalikan pesan yang sesuai
        return result
    
    return {"message": "Place removed from user's list successfully"}