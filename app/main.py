

from fastapi import FastAPI
from app.db import models
from app.db.database import engine
from app.routers import user, place
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user.router)
app.include_router(place.router)