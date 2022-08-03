from http import HTTPStatus

from flask import Flask, jsonify, request, wrappers

from executer import execute_request

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def ping():
    return jsonify("I am a QGIS Processor!"), HTTPStatus.OK


@app.route("/list")
def list_algs():
    return execute_request("list_algs")


@app.route("/help/<provider_id>/<algorithm_id>")
def get_alg_help(provider_id, algorithm_id):
    return execute_request("get_alg_help", provider_id, algorithm_id)


@app.route("/process/<provider_id>/<algorithm_id>", methods=["POST"])
def process_alg(provider_id, algorithm_id):
    data = request.json
    return execute_request("process_alg", provider_id, algorithm_id, data)
