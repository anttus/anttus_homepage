import json
from flask import Flask
from flask import render_template
import requests
from waitress import serve
import logging

logger = logging.getLogger("waitress")
logger.setLevel(logging.INFO)
app = Flask(__name__)
app.static_folder = "static"
cv_url = (
    "https://gist.githubusercontent.com/anttus/d1285d208ef1cb4d54e27561251e38cd/raw/"
)


@app.route("/")
def index():
    data = load_data()
    logger.info("Data loaded from GitHub")
    return render_template("index.html", data=data)


def load_data():
    try:
        r = requests.get(cv_url)
        logger.info("Successfully loaded content")
        return json.loads(r.content)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5050, url_scheme="https")
