import random
import re


class Chatbot():
    def __init__(self):
        self.intent = {
            'help': r'help|assist|support|how (do|to)|what can you do|commands|options',
            'recommend': r'recommend|suggest|find|give me',
            'improve': r'improve|better|refine|adjust|tune',
            'new_song': r'new song|song| something new',
            'similar_songs': r'similar|like this|more like|same vibe',
        }
        self.goal = {
            'playlist': r'create|make|build|generate.*playlist|new playlist'
        }
        self.moods = (r'happy|sad|chill|relax|energetic|party|focus')
        self.genres = (r'rock|pop|rap|hip hop|jazz|edm|classical')

    def start(self):
        print("Welcome To Riptide.")
        self.chat()

    def detect_intent(self, message):
        for key,value in self.intent.items():
            intent = key
            pattern = value
            found_match = re.match(pattern, message)
            if found_match and intent =='help':
                return self.help()
            elif found_match and intent =='recommend':
                return self.recommend()
            elif found_match and intent =='improve':
                return self.improve()
            elif found_match and intent == 'new_song':
                return self.new_song()
            elif found_match and intent == 'similar_songs':
                return self.similar_songs()
        return self.confused()
    
    def detect_goal(self, message):
        for key,value in self.goal.items:
            goal = key
            pattern = value
            found_match = re.match(pattern, message)
            if found_match and goal =='playlist':
                return 0
            elif found_match and goal =='':
                return 1
            elif found_match and goal =='':
                return 2

    def detect_mood(self, message):
        mood = re.match(self.moods, message)

    def detect_genre(self):
        pass

    def chat(self):
        message = input().lower()
        self.detect_intent(message)

    def help(self):
        response = "Ask me to 'Create a _____ playlist'" # MAKE A BETTER VERSION OF THIS
        print(response)
        self.chat()

    def recommend(self):
        responses = ("Working on it", "Nah")
        # add some way to talk to recommender system while sending message through
        print(random.choice(responses))
        self.chat()

    def new_song(self):
        pass # recommend system makes new song
        print('song')
        self.chat()

    def confused(self):
        response = "Sorry I don't understand, Type 'Help' for more options."
        print(response)
        self.chat()



bot = Chatbot()
bot.start()