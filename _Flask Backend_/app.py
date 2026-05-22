from flask import Flask, jsonify, request
from flask_cors import CORS





app = Flask(__name__)
CORS(app, origins=["http://localhost:5500"])
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/chat', methods=['GET'])
def send_chatbot():
    items={'chatbot_txt': "This is text that is coming from flask"}
    return jsonify(items), 200



if __name__ == "__main__":
    app.run(debug=True)
