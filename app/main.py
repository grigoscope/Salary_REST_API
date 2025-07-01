import os
import json
import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.utils import generate_token, get_salary_and_next_raise, refresh_all_tokens

# Path to the JSON data file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(os.path.dirname(BASE_DIR), 'employee.json')

app = FastAPI(title="💼 Salary REST API", version="0.1.0")


class Credentials(BaseModel):
    login: str
    password: str


@app.on_event("startup")
async def schedule_token_refresh():
    """
    Spawn a background task that refreshes all tokens every hour.
    """
    async def refresher():
        while True:
            refresh_all_tokens(DATA_FILE)
            await asyncio.sleep(3600)  # sleep for 1 hour

    asyncio.create_task(refresher())


@app.post("/token", summary="Obtain authentication token")
async def login_for_token(creds: Credentials):
    token = generate_token(creds.login, creds.password, DATA_FILE)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid login or password")
    return {"token": token}


@app.get("/salary", summary="Retrieve salary info by token")
async def read_salary(token: str):
    result = get_salary_and_next_raise(token, DATA_FILE)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    current_salary, next_raise_date = result
    return {
        "current_salary": current_salary,
        "next_raise_date": next_raise_date
    }
