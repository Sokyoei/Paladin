from typing import Dict

from fastapi import WebSocket
from loguru import logger


class WebSocketManager(object):

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected, current active connections: {len(self.active_connections)}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected, current active connections: {len(self.active_connections)}")

    async def send_message(self, message: str, websocket: WebSocket):
        if websocket in self.active_connections.values():
            logger.info(f"Send `{message}` to client `{websocket}`")
            await websocket.send_text(message)

    async def broadcast(self, message: str, sender_id: str | None = None):
        active_connections = self.active_connections.copy()
        for client_id, client in active_connections.items():
            if sender_id and sender_id == client_id:
                continue
            await client.send_text(message)


websocket_manager = WebSocketManager()
