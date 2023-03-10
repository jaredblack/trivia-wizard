from dataclasses import asdict, dataclass
from pymongo import MongoClient
import os


@dataclass
class Answer:
    gameCode: str
    teamName: str
    answer: str
    questionIndex: int
    pointsGiven: int = 0
    question: str = ""


class TriviaDatabase:
    def __init__(self) -> None:
        self.db = self.get_database()
        self.games = self.db["games"]
        self.answers = self.db["answers"]
        self.scores = self.db["scores"]

    def get_database(self):
        username = os.environ.get("TRIVIA_MONGO_USERNAME")
        password = os.environ.get("TRIVIA_MONGO_PASSWORD")
        CONNECTION_STRING = f"mongodb+srv://{username}:{password}@trivia-wizard-db.r1kpwn5.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(CONNECTION_STRING)
        return client['user_shopping_list']

    def get_game(self, game_code):
        return self.games.find_one({"gameCode": game_code})

    def get_answers(self, gameCode, questionIndex):
        answers = self.answers.find(
            {"gameCode": gameCode, "questionIndex": questionIndex})
        l = []
        for answer in answers:
            answer.pop("_id")
            l.append(answer)
        print(f"got {len(l)} answers from db")
        return l

    def insert_answer(self, answer: Answer):
        self.answers.insert_one(asdict(answer))

    def update_answer(self, answer: Answer):
        self.answers.update_one({"gameCode": answer.gameCode, "questionIndex": answer.questionIndex, "team": answer.team}, {
                                "$set": asdict(answer)})

    def game_code_exists(self, game_code):
        return self.get_game(game_code) != None

    def update_score(self, gameCode, teamName, score):
        self.scores.update_one({"gameCode": gameCode, "teamName": teamName}, {
                               "$set": {"score": score}}, upsert=True)

    def get_scores(self, gameCode):
        scores = self.scores.find({"gameCode": gameCode})
        l = []
        for score in scores:
            score.pop("_id")
            l.append(score)
        return l

    def get_team_score(self, game_code, team_name):
        score_obj = self.scores.find_one(
            {"gameCode": game_code, "teamName": team_name})
        if score_obj is None:
            return 0
        return score_obj["score"]

    def update_points_given(self, gameCode, teamName, questionIndex, pointsGiven):
        self.answers.update_one({"gameCode": gameCode, "teamName": teamName, "questionIndex": questionIndex}, {
                                "$set": {"pointsGiven": pointsGiven}})

    def get_players_no_answer(self, gameCode, questionIndex, teamNames):
        answers = self.get_answers(gameCode, questionIndex)
        teamNamesWithAnswer = [answer["teamName"] for answer in answers]
        return [teamName for teamName in teamNames if teamName not in teamNamesWithAnswer]


if __name__ == "__main__":
    db = TriviaDatabase()
    print(db.get_answers("TEST1", 5))
