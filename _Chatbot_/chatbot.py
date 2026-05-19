import random
import re


class Chatbot():
    def __init__(self):
        self.talk = {
            'help': r'help',
            'recommend': r'create|make|playlist',
            'improve': r'improve|better',
            'new_song': r'new song|song'
            #album finder
        }

    def start(self):
        print("Welcome To Riptide.")
        self.chat()

    def reply(self, message):
        for key,value in self.talk.items():
            intent = key
            pattern = value
            found_match = re.match(pattern, message)

            if found_match and intent =='recommend':
                return self.recommend()
            elif found_match and intent =='help':
                return self.help()
            elif found_match and intent =='new_song':
                return self.new_song()
            # elif found_match and intent =='':
            #     return self.()
        return self.confused()

    def chat(self):
        message = input().lower()
        self.reply(message)

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
        response = "Try do this..." # MAKE A BETTER VERSION OF THIS
        print(response)
        self.chat()



bot = Chatbot()
bot.start()