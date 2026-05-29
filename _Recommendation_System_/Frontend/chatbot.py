import random
import re
import numpy as np
import joblib
from pathlib import Path

from _Recommendation_System_.Frontend.recommender import SongRecommender

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_PATH = PROJECT_ROOT / "models"


class Dialog_Manager:
    def __init__(self, style, mood, genre, message):
        self.style = style.group(0) if style else None
        self.mood = mood.group(0) if mood else None
        self.genre = genre.group(0) if genre else None
        self.text = message

    def dialog_manager(self):
        enriched_text = self.text

        if self.mood:
            enriched_text += f" {self.mood}"
        if self.genre:
            enriched_text += f" {self.genre}"
        if self.style:
            enriched_text += f" {self.style}"

        return enriched_text


class Chatbot:
    def __init__(self):
        self.X =joblib.load(MODELS_PATH / "X_final.jb")
        self.recommender = SongRecommender(input_dim=self.X.shape[1], device="cpu")
        self.vectorizer = joblib.load(MODELS_PATH / "vectorizer.jb")
        self.message = " "
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

    def detect_intent(self):
        if re.search(self.intent["help"], self.message):
            return self.help()

        if re.search(self.intent["recommend"], self.message):
            return self.recommend()
        
        return self.confused()
    
    def detect_goal(self):
        for key,value in self.goal.items():
            goal = key
            pattern = value
            found_match = re.search(pattern, self.message)
            if found_match and goal =='playlist':
                return 0
            elif found_match and goal =='new_song':
                return 1
            
    def detect_style(self):
        style = re.search(self.style, self.message)
        return style
            
    def detect_mood(self):
        mood = re.search(self.moods, self.message)
        return mood

    def detect_genre(self):
        genre = re.search(self.genres, self.message)
        return genre
    
    def extract_number(self):
        number = re.search(self.number, self.message)
    
        if number:
            return number.group(1)  # Returns only the number portion
        return None

    def chat(self):
        while True:
            self.message = input().lower()
            self.detect_intent()

    def help(self):
        response = "Ask me to 'Create a _____ playlist'" # MAKE A BETTER VERSION OF THIS
        print(response)
        self.chat()

    def recommend(self):
        goal = self.detect_goal()
        style = self.detect_style()
        mood = self.detect_mood()
        genre = self.detect_genre()

        manager = Dialog_Manager(style, mood, genre, self.message)
        query_text = manager.dialog_manager()
        query_vector = self.vectorizer.transform([query_text]).toarray()[0]

        if goal == 0:
            length = self.extract_number()
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


if __name__ == "__main__":
    bot = Chatbot()
    try:
        bot.start()
    except Exception as e:
        print(e)