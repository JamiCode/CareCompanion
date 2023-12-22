from typing import Union
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from fastapi.exceptions import WebSocketException
import fastapi as _fastapi
import fastapi.security as _security
import services as _services
import schemas as _schemas
import sqlalchemy.orm as _orm
import models
import passlib.hash as _hash



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

@app.get("/api/create_bot_user/")
def create_bot_user(
    db: _orm.Session = _fastapi.Depends(_services.get_db)
    ):
    """Creates bot user"""
    bot_user = db.query(models.User).filter(models.User.email == "bot@example.com").first()

    if bot_user is None:
    # Bot user doesn't exist, create a new one
        bot_user = models.User(
        email="bot@example.com",
        first_name="MediCare",
        last_name="Bot",
        hashed_password=_hash.bcrypt.hash("medicarebot1234"),
        is_bot=True,
        )

        # Add the bot user to the session and commit the changes
        db.add(bot_user)
        db.commit()
        db.add(bot_user)
        db.commit()
        db.refresh(bot_user)  # Refresh to get the updated user object

        return {"message": "Bot user created successfully"}

    return {"message": "Bot user already exists"}



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

# Endpoint to create a conversation
@app.post("/api/create_convo/", response_model=dict)
async def create_conversation(
    conversation: _schemas.ConversationCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    token: str = _fastapi.Depends(_services.authenticate_token),
    ):
    """Endpoint used to create a conversation """
    user = await _services.get_current_user(db, token)
    print(user,2)
    convo = await _services.create_conversation_service(user,conversation, db)
    return {
        "conversation_id":convo.id, 
        'conversation_date_created':convo.date_created ,
        "message": "Conversation created successfully"
        }


@app.websocket("/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            # Receive JSON data containing the message payload
            data = await websocket.receive_json()
            message_payload = _schemas.MessagePayload(**data)

            # Pass the received message text to the AI function (mocked for now)
            ai_response = await get_ai_response(message_payload.text_content)
            
            # Prepare the AI's response payload
            response_payload = {
                "conversation_id": message_payload.conversation_id,
                "text_content": ai_response,
                "author_id": 123  #x Replace with the actual author ID or logic to identify the author
            }

            # Send the AI's response back to the client via WebSocket
            await websocket.send_text(response_payload)
        except WebSocketDisconnect:
            break  # Break the loop if WebSocket is disconnected