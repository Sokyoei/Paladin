from typing import Dict, Optional

from fastapi import WebSocket
from loguru import logger


class WebSocketManager(object):

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected, current active connections: {len(self.active_connections)}")

    def disconnect(self, client_id: str):
        del self.active_connections[client_id]
        logger.info(f"Client {client_id} disconnected, current active connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, sender_id: Optional[str] = None):
        for client_id, client in self.active_connections.items():
            if sender_id and sender_id == client_id:
                continue
            await client.send_text(message)


websocket_manager = WebSocketManager()
