from flask import Flask, jsonify, request
import os
import logging
import sys
from _Recommendation_System_.Frontend import chatbot

# Variables
application = Flask(__name__)
app = application
bot = chatbot.Chatbot()
logger = logging.getLogger(__name__)


SECRET = os.environ.get("ORIGIN_VERIFY_SECRET")

if not SECRET:
    logger.warning("ORIGIN_VERIFY_SECRET not found in environment. Falling back to default secret for local development only.")
    print("WARNING: ORIGIN_VERIFY_SECRET not found in environment.", file=sys.stderr)
    SECRET = "localhost"

@app.before_request
def verify_origin():
    token = request.headers.get("X-Origin-Verify")
    if token != SECRET:
        return {"error": "Forbidden"}, 403


# Routes
"""Test route to see if the program is responding correctly"""
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"






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
                "title": "Genericplaylistflaskbutthenameisreally long and will overflow really badly",
                "duration": "1H 45M"
            }
        ]
    }
    return jsonify(items), 200




"""
This route will recieve data from the website as user_input, 
which will then be passed into the chatbot
"""
@app.route('/api/chat', methods=['POST'])
def get_response():
    print("anything at all?")
    print("Raw JSON:", request.get_json())

    recieved = request.get_json()

    if not recieved:
        return jsonify({"error": "No JSON received"}), 400

    user_input = recieved.get('user_txt')
    print("user_input:", user_input)

    if not user_input:
        print("ahhhh no user_txt")
        return jsonify({"error": "user_txt missing"}), 400

    print("found it", user_input)
    
    bot_output = bot.chat(user_input)
    print(bot_output)
    
    response_data = {
        'chatbot_txt': f"{bot_output}", 
        'msg_id': "0"
    }

    
    return jsonify(response_data), 200
    

#ROUTES FOR EXTERNAL API (E.G SPOTIFY AND SENSTIVE DATA)


# @app.route('spotifyWebsiteVar{id}', methods=['GET'])
# def get_playlists():




# Program run
if __name__ == "__main__":
    application.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )