import itertools
import json
import secrets
import websockets
import asyncio
import os
import signal

JOIN = {}

async def host(websocket):
    async for message in websocket:
        event = json.loads(message)
        print(event)

async def relay_answers(websocket, join_id):
    async for message in websocket:
        host_ws = JOIN[join_id]
        if host_ws.close_code is not None:
            print("WebSocket connection is closed.")
            break
        await host_ws.send(message)
        

async def create(websocket, join_id):
    JOIN[join_id] = websocket
    print("Created a new game with join id", join_id)
    try:
        event = {
            "type": "info",
            "message": "Successfully created a new game",
        }
        await websocket.send(json.dumps(event))
        await host(websocket)
    finally:
        # del JOIN[join_id]
        pass

async def join(websocket, join_id):
    if join_id not in JOIN:
        event = {
            "type": "error",
            "message": "Invalid join id",
        }
        print("invalid join id")
        await websocket.send(json.dumps(event))
        return
    print("Joined the game with join id", join_id)
    try:
        event = {
            "type": "info",
            "message": "Successfully joined the game",
        }
        # await websocket.send(json.dumps(event))
        await relay_answers(websocket, join_id)
    finally:
        del JOIN[join_id]


async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "create" in event:
        await create(websocket, event['joinId'])
    else:
        await join(websocket, event['joinId'])

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    port = int(os.environ.get("PORT", "8001"))
    async with websockets.serve(handler, "", port):
        await stop

if __name__ == "__main__":
    asyncio.run(main())