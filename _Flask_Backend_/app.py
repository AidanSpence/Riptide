from flask import Flask, jsonify, request
from flask_cors import CORS





app = Flask(__name__)
CORS(app, origins=["http://localhost:5500"])
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# ROUTES FOR INTERNAL CALLS (E.G HTML AND AI BACKEND)
@app.route('/api/chat', methods=['GET'])
def send_chatbot():
    items={'chatbot_txt': "This is text that is coming from flask"}
    return jsonify(items), 200

@app.route('/api/playlist', methods=['GET'])
def send_playlist():
    items = {
        "playlist_data": [
            {
                "title": "This is a \"playlist\" and its name is so incredibly long that its completely insane",
                "duration": "1H 30M"
            },
            {
                "title": "Another playlist from flask",
                "duration": "45M"
            }
        ]
    }
    return jsonify(items), 200

#ROUTES FOR EXTERNAL API (E.G SPOTIFY AND SENSTIVE DATA)







# run
if __name__ == "__main__":
    app.run(debug=True)
