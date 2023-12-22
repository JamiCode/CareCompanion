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
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, conversation_id:int, websocket):
        if not conversation_id in self.active_connections.keys():
            self.active_connections[conversation_id] = websocket
            

    def disconnect(self, conversation_id: int):
        if conversation_id in self.active_connections:
            self.active_connections.pop(conversation_id)


