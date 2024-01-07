from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

clients: List[WebSocket] = []

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                await client.send_text(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        clients.remove(websocket)
        
