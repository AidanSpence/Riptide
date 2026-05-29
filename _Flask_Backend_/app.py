from flask import Flask, jsonify, request
# This is required for correct custom port routing 
from flask_cors import CORS

# Variables
id = 0
app = Flask(__name__)
CORS(app, origins=["http://localhost:5500"]) 


# Routes
"""Test route to see if the program is responding correctly"""
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# ROUTES FOR INTERNAL CALLS (E.G HTML AND AI BACKEND)
"""This returns chat content as chatbot_txt:text, and 
returns msg_id as 0 or 1.
0 = justification left and 1 = right"""
@app.route('/api/chat', methods=['GET'])
def send_chatbot():
    global id
    id = (id + 1 ) % 2 # ID for text justification (0=left)
    items={'chatbot_txt': "This is text that is coming from flask", 'msg_id': f"{id}"}
    return jsonify(items), 200


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



#ROUTES FOR EXTERNAL API (E.G SPOTIFY AND SENSTIVE DATA)


# @app.route('spotifyWebsiteVar{id}', methods=['GET'])
# def get_playlists():




# Program run
if __name__ == "__main__":
    app.run(debug=True)
