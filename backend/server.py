from typing import Union
from fastapi import FastAPI
import fastapi as _fastapi
import fastapi.security as _security
import services as _services
import schemas as _schemas
import sqlalchemy.orm as _orm


app = FastAPI()


# User authentication endpoints

@app.post("/api/users")
async def create_user(
    user:_schemas.UserCreate, 
    db:_orm.Session = _fastapi.Depends(_services.get_db)
    ):
    """ Endpoint responsible for creating users"""
    db_user = await _services.get_user_by_email(db, user.email)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")
    return await _services.create_user(db, user)

@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    """ Endpoint responsible for generating token """
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user)


@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(
    user:_schemas.User = _fastapi.Depends(_services.get_current_user),
    ):
    """ Endpoint responsible to get the user"""
    return user






