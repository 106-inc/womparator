from flask import Flask, jsonify
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)


@app.route("/upload", methods=["POST"])
def upload():
    print(request.data)
    response = "Whatever you wish too return"
    return response


@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Pixies Team Production"})


if __name__ == "__main__":
    app.run(port=8080)
