
from database import TriviaDatabase


class Game:
    def __init__(self, game_code, host_socket):
        self.game_code = game_code
        self.question_index = 1
        self.host_socket = host_socket
        self.players = {}
        self.watch_sockets = []
        self.db = TriviaDatabase()
        self.accepting_answers = False

    def add_player(self, player_socket, team_name):
        self.players[team_name] = player_socket

    def get_player_sockets(self):
        return self.players.values()

    def get_player_socket(self, team_name):
        return self.players[team_name]

    def get_players_no_answer(self):
        player_names = self.db.get_players_no_answer(
            self.game_code, self.question_index, self.players.keys())
        return [self.players[team_name] for team_name in self.players if team_name in player_names]

    def increment_question_index(self):
        self.question_index += 1
        return self.question_index

    def decrement_question_index(self):
        if (self.question_index > 1):
            self.question_index -= 1
        return self.question_index

    def get_answers(self):
        answers = self.db.get_answers(self.game_code, self.question_index)
        if answers is None:
            answers = []
        return answers

    def add_answer(self, answer):
        self.db.insert_answer(answer)

    def update_score(self, teamName, score):
        print(f"Updating team {teamName}'s score to {score}")
        self.db.update_score(self.game_code, teamName, score)

    def get_scores(self):
        return self.db.get_scores(self.game_code)

    def get_team_score(self, team_name):
        return self.db.get_team_score(self.game_code, team_name)

    def update_points_given(self, team_name, points_given):
        # at the current question index for the given team name, find the answer and update the score
        self.db.update_points_given(
            self.game_code, team_name, self.question_index, points_given)

    def remove_player(self, team_name):
        del self.players[team_name]

    def remove_watch_socket(self, watch_socket):
        self.watch_sockets.remove(watch_socket)
