from flask import Flask, jsonify, request
from flask_cors import CORS
from _Recommendation_System_.Frontend import chatbot
import os
import logging
import sys
import requests
import base64

# App Configuration
application = Flask(__name__)
app = application
CORS(app)
bot = chatbot.Chatbot()
logger = logging.getLogger(__name__)

# Spotify Codes
CLIENT_ID = '3eed8ec7a7a8454393d3e118574bdd05'
CLIENT_SECRET = '53cc431ea67c40ccbc5dbc9fd288f6e2'
REDIRECT_URI = 'https://d11r265tlaxh0o.cloudfront.net/'
#REDIRECT_URI = 'http://127.0.0.1:5500/_Website_/main.html'



# SECRET = os.environ.get("ORIGIN_VERIFY_SECRET")

# if not SECRET:
#     logger.warning("ORIGIN_VERIFY_SECRET not found in environment. Falling back to default secret for local development only.")
#     print("WARNING: ORIGIN_VERIFY_SECRET not found in environment.", file=sys.stderr)
#     SECRET = "localhost"

# @app.before_request
# def verify_origin():
#     token = request.headers.get("X-Origin-Verify")
#     if token != SECRET:
#         return {"error": "Forbidden"}, 403

# ==========================================
# Routes
# ==========================================

@app.route("/")
def hello_world():
    """Test route to see if the program is responding correctly"""
    return "<p>Hello, World!</p>"


# @app.route('/api/playlist', methods=['GET'])
# def send_playlist():
#     """Passes playlist info as a list of json, with the values: title and duration"""
#     items = {
#         "playlist_data": [
#             {
#                 "title": "Generic playlist 1 flask",
#                 "duration": "1H 30M"
#             },
#             {
#                 "title": "Genericplaylistflaskbutthenameisreally long and will overflow really badly",
#                 "duration": "1H 45M"
#             }
#         ]
#     }
#     return jsonify(items), 200


@app.route('/api/chat', methods=['POST'])
def get_response():
    """
    Receives incoming message from the website,
    processes them via the chatbot, and returns the response.
    """
    print("JSON Message: ", request.get_json())
    recieved = request.get_json()
    
    if not recieved:
        return jsonify({"Error": "No JSON received"}), 400

    user_input = recieved.get('user_txt')

    # Verify Message
    if not user_input:
        return jsonify({"Error": "user_txt missing"}), 400
    
    # Process input through chatbot
    bot_output = bot.chat(user_input)
    
    response_data = {
        'chatbot_txt': f"{bot_output}", 
        'msg_id': "0"
    }

    return jsonify(response_data), 200


# ==========================================
# Routes for Spotify
# ==========================================


@app.route("/api/spotify-token")
def spotify_token():
    """"""
    code = request.args.get("code")

    if not code:
        return jsonify({"error": "missing code"}), 400

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        headers={
            "Authorization": "Basic " + base64.b64encode(
                f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
            ).decode()
        }
    )

    return jsonify(response.json())


# Program run
if __name__ == "__main__":
    application.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )