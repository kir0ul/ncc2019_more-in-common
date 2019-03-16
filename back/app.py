from flask import Flask
import json
from flask.json import jsonify

app = Flask(__name__)


@app.route("/")
def api_root():
    """API root"""
    return "<h2>Welcome to the API</h2>"


@app.route("/hashtag/<hashtag>")
def get_hashtag(hashtag):
    """Hashtag route"""

    # Mocked JSON
    mocked_json_path = "../data/api_out.json"
    with open(mocked_json_path, "r") as fh:
        data = fh.readlines()
        data = "".join(data)
    response = json.loads(data)
    response = jsonify(response)

    return response
