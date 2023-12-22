from typing import Union
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from fastapi.exceptions import WebSocketException
from fastapi import WebSocket, WebSocketDisconnect
from networking import ClientConnectionManager
import fastapi as _fastapi
import fastapi.security as _security
import services as _services
import schemas as _schemas
import sqlalchemy.orm as _orm
import models
import passlib.hash as _hash
import websockets
import json



app = FastAPI()
websocket_manager = ClientConnectionManager()


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

# Endpoint to create a conversation
@app.post("/api/create_convo/", response_model=dict)
async def create_conversation(
    conversation: _schemas.ConversationCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    token: str = _fastapi.Depends(_services.authenticate_token),
    ):
    """Endpoint used to create a conversation """
    user = await _services.get_current_user(db, token)
    convo = await _services.create_conversation_service(user,conversation, db)
    return {
        "conversation_id":convo.id, 
        'conversation_date_created':convo.date_created ,
        "message": "Conversation created successfully"
        }


@app.websocket("/chat/{room_id}/{token}")
async def chat_endpoint(
    room_id:int,
    token:str,
    websocket:WebSocket,
    db:_orm.Session = _fastapi.Depends(_services.get_db)
    ):
    print('hello')
    await websocket.accept()
    user = await _services.verify_socket_connection(token, db=db)
    conversation = _services.check_conversation_exists(db, room_id)
    print(conversation)

    await websocket.accept()
    await websocket_manager.connect(conversation.id, websocket)

    while True:
        try:
            # Receive JSON data containing the message payload
            data = await websocket.receive_json()
            message_payload = _schemas.MessagePayload(**data)
            websocket_conn  = websocket_manager.active_connections[conversation.id]

            await websocket_conn.send_json()

        
            new_message = models.Message(
                text_content=message_payload.text_content,
                author_id=user.id,
                conversation_id=conversation.id
            )
            db.add(new_message)
            db.commit()

            # Mock bot response
            bot_response = {
                "conversation_id": conversation.id,
                "text_content": "This is a response from the bot.",
            }

            # add the message as well
            bot_message = models.Message(
                text_content=bot_response["text_content"],
                conversation_id=bot_response["conversation_id"],
                is_bot_message=True,
                
                )
            db.add(bot_message)
            db.commit()
            
        

            # Send the AI's response back to the client via WebSocket
            await websocket_conn.send_json(bot_response)
        except websockets.exceptions.ConnectionClosedOK as e:
            websocket_manager.disconnect(user.id)
         
        except websockets.exceptions.ConnectionClosedError as error:
            websocket_manager.disconnect(user.id)
        except json.decoder.JSONDecodeError:
            # if user does not put in the format of json
            websocket_manager.disconnect(user.id)
            raise WebSocketException(code=_fastapi.status.WS_1008_POLICY_VIOLATION, reason="Unable to parse JSON")
        except WebSocketDisconnect:
            websocket_manager.disconnect(user.id)
        
        except Exception as e:
            print(e)
            websocket_manager.disconnect(user.id)
        finally:
            break



           