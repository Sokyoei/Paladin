import asyncio
import threading
from typing import Set

import websockets
from loguru import logger
from websockets import ServerProtocol


class WebSocketServer(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server = None
        self.clients: Set[ServerProtocol] = set()
        self.stop_event = asyncio.Event()

    async def handle(self, websocket):
        logger.info("Client connected")
        self.clients.add(websocket)
        try:
            async for message in websocket:
                logger.info(f"Received message from client: {message}")
        except websockets.exceptions.ConnectionClosed as e:
            logger.error(f"Connection closed: {e}")
        finally:
            self.clients.remove(websocket)

    async def start_server(self):
        self.server = await websockets.serve(self.handle, self.host, self.port)
        logger.info(f"WebSocket server started on ws://{self.host}:{self.port}")
        await self.stop_event.wait()

    async def stop_server(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            logger.info("WebSocket server stopped")

    async def send_message_to_clients(self, message):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.start_server())
        self.loop.run_forever()
        self.loop.run_until_complete(self.stop_server())

    def send_frame(self, message):
        asyncio.run_coroutine_threadsafe(self.send_message_to_clients(message), self.loop)

    async def _set_stop_event(self):
        self.stop_event.set()

    def stop(self):
        asyncio.run_coroutine_threadsafe(self._set_stop_event(), self.loop).result()
        self.loop.call_soon_threadsafe(self.loop.stop)  # 停止事件循环
