from flask import Flask, jsonify
from flask_cors import CORS
from flask import request

womparator = Flask(__name__)
CORS(womparator)


@womparator.route("/upload", methods=["POST"])
def upload():
    print(request.data)
    response = "Whatever you wish too return"
    return response


if __name__ == "__main__":
    womparator.run(port=8080, host="0.0.0.0")
