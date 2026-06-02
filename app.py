from flask import Flask, jsonify, request
# This is required for correct custom port routing 
from flask_cors import CORS

from _Recommendation_System_.Frontend import chatbot

# Variables
app = Flask(__name__)
CORS(app, origins=["*"]) 
bot = chatbot.Chatbot()

# Routes
"""Test route to see if the program is responding correctly"""
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# ROUTES FOR INTERNAL CALLS (E.G HTML AND AI BACKEND)
# """This returns chat content as chatbot_txt:text, and 
# returns msg_id as 0 or 1.
# 0 = justification left and 1 = right"""
# @app.route('/api/chat', methods=['GET'])
# def send_chatbot(user_input: str):
#     bot_output = bot.chat(user_input)
#     items={'chatbot_txt': f"{bot_output}", 'msg_id': "0"}
#     return jsonify(items), 200


"""Passes playlist info as a list of json, with the values:
title and duration """
@app.route('/api/playlist', methods=['GET'])
def send_playlist():
    items = {
        "playlist_data": [
            {
                "title": "Generic playlist 1 flask",
                "duration": "1H 30M"
            },
            {
                "title": "Generic playlist 2 flask",
                "duration": "45M"
            }
        ]
    }
    return jsonify(items), 200




"""
This route will recieve data from the website as user_input, 
which will then be passed into the chatbot
"""
@app.route('api/chat/input', methods=['POST'])
def get_response():
    recieved = request.get_json()
    user_input = recieved.get('user_txt')
    if not user_input:
        print("ahhhh i cant find it")
        pass
        #return "sdfghjkl" - find some way to return
    #Find some way to return
    print("found it", user_input)
    pass



#ROUTES FOR EXTERNAL API (E.G SPOTIFY AND SENSTIVE DATA)


# @app.route('spotifyWebsiteVar{id}', methods=['GET'])
# def get_playlists():




# Program run
if __name__ == "__main__":
    app.run(debug=True)
