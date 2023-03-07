import json
import websockets
import asyncio
import os
import signal

from database import Answer, TriviaDatabase
from gamestate import Game


class Server:
    def __init__(self) -> None:
        asyncio.run(self.main())
    
    async def send_error(self, websocket, message):
        event = {
            "type": "error",
            "message": message,
        }
        await websocket.send(json.dumps(event))


    async def host(self, host_socket, game):
        async for message in host_socket:
            event = json.loads(message)
            if event["type"] == "next":
                game.increment_question_index()
                await self.broadcast_new_question(game)
            elif event["type"] == "prev":
                game.decrement_question_index()
                await self.broadcast_new_question(game)
            elif event["type"] == "updateScore":
                await self.update_score(game, event["teamName"], event["score"])
            else:
                await self.send_error(host_socket, "Unknown host request type")

    async def update_score(self, game, teamName, score):
        game.update_score(teamName, score)
        # broadcast to score view

    async def broadcast_new_question(self, game):
        await self.update_player_question_index(game)
        await self.update_host_question(game)

    async def update_host_question(self, game):
        answers = game.get_answers()
        event = {
            "type": "newQuestion",
            "questionIndex": game.question_index,
            "answers": answers
        }
        await game.host_socket.send(json.dumps(event))
    
    async def update_player_question_index(self, game):
        # TODO: include info about whether each team needs to provide an answer for this question or not.
        event = {
            "type": "updatePlayerQuestionIndex",
            "questionIndex": game.question_index
        }
        for player in game.players:
            await player.send(json.dumps(event))

    async def relay_answers(self, player_socket, game):
        async for message in player_socket:
            host_ws = game.host_socket
            if host_ws.close_code is not None:
                print("WebSocket connection is closed.")
                break
            # TODO: Should validate here that the question index passed actually matches the server's index
            event = json.loads(message)
            answer = Answer(game.game_code, event["teamName"], event["answer"], int(event["questionIndex"]))
            game.add_answer(answer)
            answer_received_event = {
                "type": "answerReceived",
                "questionIndex": game.question_index
            }
            await player_socket.send(json.dumps(answer_received_event))
            await host_ws.send(message)
            

    async def create(self, websocket, game_code):
        game = Game(game_code, websocket)
        self.games[game_code] = game
        print("Created a new game with game code", game_code)
        try:
            event = {
                "type": "success",
                "message": "Successfully created a new game",
                "gameCode": game_code,
                "questionIndex": game.question_index
            }
            await websocket.send(json.dumps(event))
            await self.host(websocket, self.games[game_code])
        finally:
            # del JOIN[game_code]
            pass

    async def join(self, player_socket, game_code):
        if game_code not in self.games:
            await self.send_error(player_socket, "Invalid game code")
            print("invalid game code")
            return
        game = self.games[game_code]
        print("Joined the game with game code", game_code)
        game.players.append(player_socket)
        try:
            event = {
                "type": "success",
                "message": "Successfully joined the game",
                "gameCode": game_code,
                "questionIndex": game.question_index
            }
            await player_socket.send(json.dumps(event))
            await self.relay_answers(player_socket, game)
        finally:
            # del HOST[game_code]
            # TODO: figure out what we need to delete
            pass


    async def handler(self, websocket):
        message = await websocket.recv()
        event = json.loads(message)
        assert event["type"] == "init"

        if "create" in event:
            await self.create(websocket, event['gameCode'])
        else:
            await self.join(websocket, event['gameCode'])

    async def main(self):
        self.db = TriviaDatabase()
        self.games = {}
        loop = asyncio.get_running_loop()
        stop = loop.create_future()
        loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
        port = int(os.environ.get("PORT", "8001"))
        async with websockets.serve(self.handler, "", port):
            await stop

if __name__ == "__main__":
    Server()
    