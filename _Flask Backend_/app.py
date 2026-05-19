from flask import Flask, jsonify, request





app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/items', methods=['GET'])
def GetItems():
    return jsonify(list(items.values())), 200



if __name__ == "__main__":
    app.run(debug=True)
