from pymongo import MongoClient


def get_database():  
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://jaredblack:WeirdFISHES88@trivia-wizard-db.r1kpwn5.mongodb.net/?retryWrites=true&w=majority"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['user_shopping_list']



# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
    # Get the database
    db = get_database()
    col = db["games"]
    testgame = {
        "gameCode":"TEST1",
    }
    col.insert_one(testgame)
    
    # store questions separately so that we can query easily by game code and question index
    col = db["questions"]
    testquestion = {
        "gameCode":"TEST1",
        "index":1,
        "question":"What is the largest country in the world by land area?",
        "answers":[
            {
                "team":"team1", 
                "answer":"Russia",
                "pointsGiven":50
            }
        ]
    }
    col.insert_one(testquestion)
