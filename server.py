import json
import websockets
import asyncio
import os
import signal
import sys

from database import Answer, TriviaDatabase
from gamestate import Game

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

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
                await self.update_score(game, event["teamName"], event["score"], event["pointsGiven"])
            elif event["type"] == "updateAcceptingAnswers":
                await self.update_accepting_answers(game, event["acceptingAnswers"], event["questionIndex"], event["timeRemaining"])
            else:
                await self.send_error(host_socket, "Unknown host request type")

    # this is synonymous with timer updates
    async def update_accepting_answers(self, game, accepting_answers, question_index, time_remaining):
        if question_index != game.question_index:
            eprint("WARNING: ignoring updateAcceptingAnswers because question index doesn't match")
            return
        game.accepting_answers = accepting_answers
        await self.update_score_view_timer(game, accepting_answers, time_remaining)
        await self.update_player_accepting_answers(game, accepting_answers, time_remaining)

    async def update_score_view_timer(self, game, timer_running, time_remaining):
        event = {
            "type": "updateTimer",
            "timerRunning": timer_running,
            "timeRemaining": time_remaining
        }
        for watch_socket in game.watch_sockets:
            await watch_socket.send(json.dumps(event))

    async def update_player_accepting_answers(self, game, accepting_answers, time_remaining):
        event = {
            "type": "updateAcceptingAnswers",
            "acceptingAnswers": accepting_answers,
            "timeRemaining": time_remaining,
        }
        players = game.get_players_no_answer() if event["acceptingAnswers"] else game.get_player_sockets()
        for player in players:
            await player.send(json.dumps(event))

    async def update_score(self, game, team_name, score, points_given):
        game.update_score(team_name, score)
        game.update_points_given(team_name, points_given)
        await self.update_score_view(game)

    async def broadcast_new_question(self, game):
        await self.update_player_question_index(game)
        await self.update_host_question(game)

    async def update_host_question(self, game):
        answers = game.get_answers()
        self.inject_answers_with_scores(answers, game)
        event = {
            "type": "newQuestion",
            "questionIndex": game.question_index,
            "answers": answers
        }
        await game.host_socket.send(json.dumps(event))
    
    def inject_answers_with_scores(self, answers, game):
        for answer in answers:
            answer["teamScore"] = game.get_team_score(answer["teamName"])
        return answers
    
    async def update_player_question_index(self, game):
        event = {
            "type": "updatePlayerQuestionIndex",
            "questionIndex": game.question_index
        }
        players = game.get_players_no_answer() if game.accepting_answers else game.get_player_sockets()
        for player in players:
            await player.send(json.dumps(event))

    async def relay_answers(self, player_socket, game):
        async for message in player_socket:
            host_ws = game.host_socket
            if host_ws.close_code is not None:
                eprint("ERROR: Host WebSocket connection is closed.")
                break
            answer_event = json.loads(message)
            if answer_event["questionIndex"] != game.question_index:
                print("WARNING: ignoring answer because question index doesn't match")
                return
            answer = Answer(game.game_code, answer_event["teamName"], answer_event["answer"], int(answer_event["questionIndex"]))
            game.add_answer(answer)
            answer_received_event = {
                "type": "answerReceived",
                "questionIndex": game.question_index
            }
            answer_event["teamScore"] = game.get_team_score(answer_event["teamName"])
            await player_socket.send(json.dumps(answer_received_event))
            await host_ws.send(json.dumps(answer_event))
            
    async def update_score_view(self, game):
        event = {
            "type": "teamScores",
            "gameCode": game.game_code,
            "teamScores": game.get_scores()
        }

        for socket in game.watch_sockets:
            if socket.close_code is not None:
                print("ERROR: Watch socket connection is closed.")
                return
            await socket.send(json.dumps(event))

    async def create(self, websocket, game_code):
        game = Game(game_code, websocket)
        if game_code in self.games:
            await self.send_error(websocket, "Game code already exists")
            print("INFO: Tried to create a game with an existing game code")
            return
        self.games[game_code] = game
        print("INFO: Created a new game with game code", game_code)
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
            del self.games[game_code]

    async def join(self, player_socket, game_code, team_name):
        team_name = team_name.strip()
        if game_code not in self.games:
            await self.send_error(player_socket, "Invalid game code")
            print("INFO: Tried to join invalid game code")
            return
        game = self.games[game_code]
        print("INFO: Joined the game with game code", game_code)
        game.add_player(player_socket, team_name)
        try:
            event = {
                "type": "success",
                "message": "Successfully joined the game",
                "gameCode": game_code,
                "questionIndex": game.question_index,
                "acceptingAnswers": game.accepting_answers
            }
            await player_socket.send(json.dumps(event))
            await self.relay_answers(player_socket, game)
        finally:
            game.remove_player(team_name)

    async def watch(self, websocket, game_code):
        if game_code not in self.games:
            await self.send_error(websocket, "Invalid game code")
            print("INFO: invalid game code for watch")
            return
        game = self.games[game_code]
        print("INFO: Watching the game with game code", game_code)
        try:
            game.watch_sockets.append(websocket)
            await self.update_score_view(game)
            async for message in websocket:
                print(f"INFO: got message from a Watch view {message}")
        finally:
            game.remove_watch_socket(websocket)

    async def handler(self, websocket):
        message = await websocket.recv()
        event = json.loads(message)
        assert event["type"] == "init"

        match event["initType"]:
            case "host":
                await self.create(websocket, event['gameCode'])
            case "player":
                await self.join(websocket, event['gameCode'], event['teamName'])
            case "watch":
                await self.watch(websocket, event['gameCode'])

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
    