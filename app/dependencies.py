import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Header, HTTPException
        
# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(secret_key: str):
    if secret_key != SECRET_KEY:
        raise HTTPException(status_code=400, detail="Invalid token query parameter")
