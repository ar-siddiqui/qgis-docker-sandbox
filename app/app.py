from http import HTTPStatus
from flask import Flask, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def ping():
    return jsonify({"message": "Hello World!"}), HTTPStatus.OK
