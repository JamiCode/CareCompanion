from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import WebSocketException
from fastapi import WebSocket
import models
import schemas
import database
import passlib.hash as _hash
import sqlalchemy.orm as _orm
import jwt
import secrets
import fastapi
import fastapi.security as security







JWT_SECRET = "jackal"
oauth2schema = security.OAuth2PasswordBearer(tokenUrl='/api/token')


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
    token: str = fastapi.Depends(oauth2schema), 
):
    try:
    
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload['id'])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Invalid  credentials")
    return schemas.User.model_validate(user)


# A custom dependency that checks for token
async def authenticate_token(
        db: _orm.Session = fastapi.Depends(get_db),
        token:str= Depends(oauth2schema),
        ):
    try:
        decoded_payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(decoded_payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Invalid credentials")

    return token

#creates conversation
async def create_conversation_service(
        user:models.User,
        conversation:schemas.ConversationCreate,
        db:_orm.Session,
    ):

        new_conversation = models.Conversation(
            title=conversation.title,
            user_id=user.id
        )

        db.add(new_conversation)
        db.commit()
        db.refresh(new_conversation)
        return new_conversation

async def get_token(websocket:WebSocket):
    token_1 = websocket.headers.get("Authorization")
    if token_1 is None:
        #if token is None
        raise WebSocketException(code=fastapi.status.WS_1008_POLICY_VIOLATION, reason="Token not found in header")
    token = token = token_1.split("Bearer ")[-1]
  
    return token

async def verify_socket_connection(
        token,
        db: _orm.Session = fastapi.Depends(get_db),
        ):
    #getting informatino from token
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms="HS256")
        user = db.query(models.User).get(payload['id'])
        print(user, 0)
    
        if user:
            return user
        else:
            raise WebSocketException(code=fastapi.status.WS_1008_POLICY_VIOLATION, reason="Token information not found")

    except:
        raise WebSocketException(code=fastapi.status.WS_1008_POLICY_VIOLATION, reason="Invalid token")

async def check_conversation_exists(db: Session, conversation_id: str) -> bool:
    """
    Function to check if a conversation with a specific conversation_id exists in the database.
    """
    conversation_exists = db.query(models.Conversation.id).filter_by(id=conversation_id).scalar() is not None
    return conversation_exists

await def get_user_conversations(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None  # Or handle the case when the user doesn't exist

    user_conversations = db.query(models.Conversation).filter(models.Conversation.user_id == user_id).all()
    return user_conversations

async def get_conversation_by_id(db: Session, conversation_id: int):
    # Retrieve the conversation by its ID
    conversation = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

    if not conversation:
        return None  # Or handle the case when the conversation doesn't exist

    return conversation


async def get_all_messages_from_conversation(db: Session, conversation_id: str):
    # Retrieve the conversation by its ID
    conversation = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

    if not conversation:
        return None  # Or handle the case when the conversation doesn't exist

    # Get all messages related to the conversation
    messages = db.query(models.Message).filter(models.Message.conversation_id == conversation_id).all()
    return messages
if __name__ == "__main__":

    create_database()
