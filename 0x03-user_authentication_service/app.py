#!/usr/bin/env python3
"""Flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from flask.helpers import make_response
from typing import Dict
from os import getenv

app = Flask(__name__)

AUTH = Auth()


def index() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
