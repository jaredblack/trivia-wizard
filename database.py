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
        
    def get_database(self):  
        username = os.environ.get("TRIVIA_MONGO_USERNAME")
        password = os.environ.get("TRIVIA_MONGO_PASSWORD")
        CONNECTION_STRING = f"mongodb+srv://{username}:{password}@trivia-wizard-db.r1kpwn5.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(CONNECTION_STRING)
        return client['user_shopping_list']
    
    def get_game(self, game_code):
        return self.games.find_one({"gameCode": game_code})
    
    def get_answers(self, gameCode, questionIndex):
        answers = self.answers.find({"gameCode": gameCode, "questionIndex": questionIndex})
        print("answers")
        l = []
        for answer in answers:
            print(answer)
            answer.pop("_id")
            l.append(answer)
        return l
    
    def insert_answer(self, answer: Answer):
        self.answers.insert_one(asdict(answer))

    def update_answer(self, answer: Answer):
        self.answers.update_one({"gameCode": answer.gameCode, "questionIndex": answer.questionIndex, "team": answer.team}, {"$set": asdict(answer)})

if __name__ == "__main__":
    db = TriviaDatabase()
    print(db.get_answers("TEST1", 5))