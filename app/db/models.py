from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Association table for the many-to-many relationship between Users and Places
user_place_association = Table(
    'user_place_association', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('place_id', ForeignKey('places.id'), primary_key=True)
)

class Rating(Base):
    __tablename__ = 'ratings'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    place_id = Column(Integer, ForeignKey('places.id'))
    rating = Column(Float, nullable=False)
    message = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    user = relationship('User', back_populates='ratings')
    place = relationship('Place', back_populates='ratings')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    photo_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)

    ratings = relationship('Rating', back_populates='user')
    saved_places = relationship('Place', secondary=user_place_association, back_populates='users')
    
    
class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    location_name = Column(String, nullable=True)
    latitude = Column(Numeric(precision=10, scale=6))
    longitude = Column(Numeric(precision=10, scale=6))
    image_url = Column(String)
    average_rating = Column(Float, default=0.0)

    # Back reference to users who saved this place
    users = relationship('User', secondary=user_place_association, back_populates='saved_places')
    ratings = relationship('Rating', back_populates='place')
    
class OTPVerification(Base):
    __tablename__ = 'otp_verifications'

    email = Column(String, primary_key=True, index=True)
    otp = Column(String)  # Simpan hash OTP, bukan teks asli
    expires_at = Column(DateTime)
