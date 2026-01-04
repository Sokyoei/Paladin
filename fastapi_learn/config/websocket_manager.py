import asyncio
from typing import Awaitable, Callable

from fastapi import WebSocket
from fastapi.websockets import WebSocketState
from loguru import logger

MessageType = str | bytes | dict


class WebSocketManager(object):

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.__lock = asyncio.Lock()
        self.__send_funcs: dict[type, Callable[[WebSocket, MessageType], Awaitable[None]]] = {
            str: lambda ws, msg: ws.send_text(msg),
            bytes: lambda ws, msg: ws.send_bytes(msg),
            dict: lambda ws, msg: ws.send_json(msg),
        }
        self.__disconnecting: set[str] = set()
        self.__disconnect_lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        async with self.__lock:
            # if client_id already exists, close the old connection
            if client_id in self.active_connections:
                old_ws = self.active_connections[client_id]
                try:
                    if old_ws.client_state == WebSocketState.CONNECTED:
                        await old_ws.close(code=1001, reason="Duplicate connection")
                    logger.debug(f"Client {client_id} duplicate connection, closed old WebSocket")
                except Exception as e:
                    logger.error(f"Failed to close old connection for {client_id}: {e}")
            # add new connection
            self.active_connections[client_id] = websocket
            logger.info(f"Client {client_id} connected, current active connections: {len(self.active_connections)}")

    async def disconnect(self, client_id: str):
        async with self.__disconnect_lock:
            if client_id in self.__disconnecting:
                logger.debug(f"Client {client_id} is already disconnecting, skip")
                return
            self.__disconnecting.add(client_id)

        try:
            async with self.__lock:
                client = self.active_connections.get(client_id)
                if not client:
                    logger.debug(f"Client {client_id} not found in active connections")
                    return
                del self.active_connections[client_id]
                logger.info(
                    f"Client {client_id} disconnected, current active connections: {len(self.active_connections)}"
                )

            if client.client_state == WebSocketState.CONNECTED:
                try:
                    await client.close(code=1000, reason="Normal closure")
                except Exception as e:
                    logger.error(f"Failed to close WebSocket for {client_id}: {e}")
        finally:
            async with self.__disconnect_lock:
                self.__disconnecting.discard(client_id)

    async def send_message(self, message: MessageType, client_id: str):
        async with self.__lock:
            if client_id not in self.active_connections:
                logger.warning(f"Client {client_id} not connected, cannot send message")
                return
            client = self.active_connections[client_id]

        if not self.__check_message_type(message):
            return

        logger.info(f"Send `{message}` to client `{client_id}`")
        await self.__try_send_message(message, client, client_id)

    async def broadcast(self, message: MessageType, sender_id: str | None = None):
        if not self.__check_message_type(message):
            return

        async with self.__lock:
            if not self.active_connections:
                logger.debug("No active connections")
                return
            active_connections = self.active_connections.copy()

        for client_id, client in active_connections.items():
            if sender_id and sender_id == client_id:
                continue
            logger.info(f"Broadcast `{message}` to client `{client_id}`")
            await self.__try_send_message(message, client, client_id)

    def __check_message_type(self, message: MessageType) -> bool:
        for msg_type in self.__send_funcs.keys():
            if isinstance(message, msg_type):
                return True
        logger.error(f"Unsupported message type: {type(message)}, only support str/bytes/dict")
        return False

    async def __try_send_message(self, message: MessageType, client: WebSocket, client_id: str):
        try:
            if client.client_state == WebSocketState.CONNECTED:
                await self.__send_funcs[type(message)](client, message)
        except Exception as e:
            logger.error(f"Error sending message to client {client_id}: {e}")
            await self.disconnect(client_id)


websocket_manager = WebSocketManager()
