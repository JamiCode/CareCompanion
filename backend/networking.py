#This file is used for managing websockets


from typing import List, Dict
from fastapi.websockets import WebSocket
import models

class ChatHistoryConnectionManager:
    """ Tracks the websocket connection to chat history"""
    def __init__(self):
        self.connections = set()

    async def connect(self, websocket:WebSocket, user_id):
        await websocket.accept()
        self.connections.add((user_id, websocket))

    def disconnect(self, websocket:WebSocket, user_id):
        self.connections.remove((user_id,websocket))





class ClientConnectionManager:
    """ Tracks overall websocket connection"""
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, user_id:int, websocket:WebSocket):
        if user_id in self.active_connections:
            print("User is already connected")
            await websocket.accept()
        else:
            print("Connected to the server", user_id)
            self.active_connections[user_id] = websocket
    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections.pop(user_id)


