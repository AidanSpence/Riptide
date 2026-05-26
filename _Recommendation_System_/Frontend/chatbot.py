import random
import re
import joblib

from recommender import SongRecommender


class Chatbot():
    def __init__(self):
        self.X =joblib.load("_Recommendation_System_/models/final_df_scaled.jb")
        self.recommender = SongRecommender(input_dim=self.X.shape[1], device="cpu")

        self.intent = {
            'help': r'help|assist|support|how (do|to)|what can you do|commands|options',
            'recommend': r'recommend|suggest|find|give me|make|create|build',
            'improve': r'improve|better|refine|adjust|tune',
        }
        self.goal = {
            'playlist': r'playlist|new playlist',
            'new_song': r'new song|song| something new',
        }
        self.style = (r'car|run|workout|sleep|dance|sport|party|study')
        self.moods = (r'happy|sad|chill|relax|energetic|party|focus')
        self.genres = (r'rock|pop|rap|hip hop|jazz|edm|classical')
        self.number = (r'(\d+)\s*song')

    def start(self):
        print("Welcome To Riptide.")
        self.chat()

    def detect_intent(self, message):
        for key,value in self.intent.items():
            intent = key
            pattern = value
            found_match = re.search(pattern, message)
            if found_match and intent =='help':
                return self.help()
            elif found_match and intent =='recommend':
                return self.recommend(message)
            #elif found_match and intent =='improve':
                #return self.improve()
        return self.confused()
    
    def detect_goal(self, message):
        for key,value in self.goal.items():
            goal = key
            pattern = value
            found_match = re.search(pattern, message)
            if found_match and goal =='playlist':
                return 0
            elif found_match and goal =='new_song':
                return 1
            
    def detect_style(self, message):
        style = re.search(self.style, message)
        return style
            
    def detect_mood(self, message):
        mood = re.search(self.moods, message)
        return mood

    def detect_genre(self, message):
        genre = re.search(self.genres, message)
        return genre
    
    def extract_number(self, message):
        number = re.search(self.number, message)
    
        if number:
            return number.group(1)  # Returns only the number portion
        return None
    
    def dialog_manager(self, message, filters):
        pass

    def chat(self):
        message = input().lower()
        self.detect_intent(message)

    def help(self):
        response = "Ask me to 'Create a _____ playlist'" # MAKE A BETTER VERSION OF THIS
        print(response)
        self.chat()

    def recommend(self, message):
        goal = self.detect_goal(message)
        style = self.detect_style(message)
        mood = self.detect_mood(message)
        genre = self.detect_genre(message)
   

        filters = [style, mood, genre]
        query_vector = self.dialog_manager(message, filters)

        if goal == 0:
            length = self.extract_number(message)
            if length != None:
                results = self.recommender.recommend(query_vector, k=int(length))
            else:
                results = self.recommender.recommend(query_vector, k=10)
        elif goal == 1:
            results = self.recommender.recommend(query_vector, k=1)
        else:
            results = self.recommender.recommend(query_vector, k=10)
        self.chat()

    def confused(self):
        response = "Sorry I don't understand, Type 'Help' for more options."
        print(response)
        self.chat()


bot = Chatbot()
bot.start()