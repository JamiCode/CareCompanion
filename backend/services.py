from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
import models
import schemas
import database
import passlib.hash as _hash
import sqlalchemy.orm as _orm
import jwt
import secrets
import fastapi
import fastapi.security as security


oauth2schema = security.OAuth2PasswordBearer(tokenUrl='/api/token')


JWT_SECRET = secrets.token_urlsafe(32) 

def create_database():
    return database.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
async def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


async def create_user(db:Session,user: schemas.UserCreate):
    user_obj = models.User(
        email=user.email, 
        hashed_password=_hash.bcrypt.hash(user.hashed_password),
        first_name=user.first_name,
        last_name = user.last_name,
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user

async def create_token(user: models.User):
    user_obj = schemas.User.model_validate(user)

    token = jwt.encode(user_obj.model_dump(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")

async def get_current_user(
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),  # Assuming you have previously defined oauth2_scheme
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload['id'])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Invalid email or password")
    return schemas.User.model_validate(user)

if __name__ == "__main__":
    create_database()