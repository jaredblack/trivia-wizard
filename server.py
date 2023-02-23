import itertools
import json
import secrets
import requests
import websockets
import asyncio
import os
import signal

from database import Answer, TriviaDatabase

HOST = {}
PLAYERS = []
GAME_CODE_LENGTH = 5

class Server:
    def __init__(self) -> None:
        asyncio.run(self.main())
    
    async def send_error(self, websocket, message):
        event = {
            "type": "error",
            "message": message,
        }
        await websocket.send(json.dumps(event))


    async def host(self, websocket):
        async for message in websocket:
            event = json.loads(message)
            if event["type"] == "next":
                await self.return_next_question(websocket)
            elif event["type"] == "prev":
                await self.return_prev_question(websocket)
            else:
                await self.send_error(websocket, "Unknown host request type")

    def generate_game_code(self):
        r = requests.get(f'https://random-word-api.herokuapp.com/word?length={GAME_CODE_LENGTH}')
        code = r.json()[0].upper()
        if self.db.game_code_exists(code):
            return self.generate_game_code()
        return code


    async def return_next_question(self, websocket):
        self.question_index += 1
        answers = self.db.get_answers(self.game_code, self.question_index)
        if answers == None:
            answers = []
        event = {
            "type": "newQuestion",
            "questionIndex": self.question_index,
            "answers": answers
        }
        await self.update_player_question_index()
        await websocket.send(json.dumps(event))

    async def return_prev_question(self, websocket):
        if (self.question_index > 1):
            self.question_index -= 1
        answers = self.db.get_answers(self.game_code, self.question_index)
        if answers == None:
            answers = []
        event = {
            "type": "newQuestion",
            "questionIndex": self.question_index,
            "answers": answers
        }
        await self.update_player_question_index()
        await websocket.send(json.dumps(event))
    
    async def update_player_question_index(self):
        event = {
            "type": "updateQuestionIndex",
            "questionIndex": self.question_index
        }
        for player in PLAYERS:
            await player.send(json.dumps(event))

    async def relay_answers(self, websocket, game_code):
        async for message in websocket:
            host_ws = HOST[game_code]
            if host_ws.close_code is not None:
                print("WebSocket connection is closed.")
                break
            event = json.loads(message)
            answer = Answer(game_code, event["teamName"], event["answer"], int(event["questionIndex"]))
            self.db.insert_answer(answer)
            await host_ws.send(message)
            

    async def create(self, websocket):
        game_code = event['gameCode'] if 'gameCode' in event else self.generate_game_code()

        HOST[game_code] = websocket
        self.game_code = game_code
        print("Created a new game with game code", game_code)
        try:
            event = {
                "type": "success",
                "message": "Successfully created a new game",
                "gameCode": game_code
            }
            await websocket.send(json.dumps(event))
            await self.host(websocket)
        finally:
            # del JOIN[game_code]
            pass

    async def join(self, websocket, game_code):
        if game_code not in HOST:
            await self.send_error(websocket, "Invalid game code")
            print("invalid game code")
            await websocket.send(json.dumps(event))
            return
        print("Joined the game with game code", game_code)
        PLAYERS.append(websocket)
        try:
            event = {
                "type": "info",
                "message": "Successfully joined the game",
            }
            # await websocket.send(json.dumps(event))
            await self.relay_answers(websocket, game_code)
        finally:
            del HOST[game_code]


    async def handler(self, websocket):
        message = await websocket.recv()
        event = json.loads(message)
        assert event["type"] == "init"

        if "create" in event:
            await self.create(websocket, event)
        else:
            await self.join(websocket, event['gameCode'])

    async def main(self):
        self.db = TriviaDatabase()
        self.question_index = 1
        loop = asyncio.get_running_loop()
        stop = loop.create_future()
        loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
        port = int(os.environ.get("PORT", "8001"))
        async with websockets.serve(self.handler, "", port):
            await stop

if __name__ == "__main__":
    Server()
    