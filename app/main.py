

from fastapi import FastAPI
from app.db import models
from app.db.database import engine
from app.routers import user, place, admin

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router)
app.include_router(user.router)
app.include_router(place.router)