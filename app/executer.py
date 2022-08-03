import traceback
from http import HTTPStatus
from typing import Tuple

from flask import Flask, jsonify, request, wrappers
from werkzeug.exceptions import BadRequest

from helpers import *


def execute_request(func: str, *args) -> Tuple[wrappers.Request, HTTPStatus]:
    """Execute the request by calling the helper functions and handle common errors."""

    template = {"Type": "", "Arguments": "", "Message": ""}

    try:
        if func == "list_algs":
            return jsonify(list_algorithms()), HTTPStatus.OK

        elif func == "get_alg_help":
            return jsonify(get_alg_help(*args)), HTTPStatus.OK

        elif func == "process_alg":
            return jsonify(process_alg(*args)), HTTPStatus.OK
    except Exception as e:
        template["Type"] = e.__class__.__name__
        template["Arguments"] = [*args]
        template["Message"] = str(e)

        if template["Type"] == "BadRequest":
            http_status = HTTPStatus.BAD_REQUEST
        else:
            http_status = HTTPStatus.INTERNAL_SERVER_ERROR
            template["StackTrace"] = traceback.format_exc()

        return jsonify(template), http_status
