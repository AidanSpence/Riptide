from flask import Flask, jsonify, request
from _Recommendation_System_.Frontend import chatbot

# App Configuration
app = Flask(__name__)
bot = chatbot.Chatbot()

# ==========================================
# Routes
# ==========================================

@app.route("/")
def hello_world():
    """Test route to see if the program is responding correctly"""
    return "<p>Hello, World!</p>"


@app.route('/api/playlist', methods=['GET'])
def send_playlist():
    """Passes playlist info as a list of json, with the values: title and duration"""
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


@app.route('/api/chat', methods=['POST'])
def get_response():
    """
    Receives incoming message from the website,
    processes them via the chatbot, and returns the response.
    """
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    recieved = request.get_json()
    user_input = recieved.get('user_txt')

    # Verify Message
    if not user_input:
        return jsonify({"error": "user_txt missing"}), 400
    
    # Process input through chatbot
    bot_output = bot.chat(user_input)
    
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
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )