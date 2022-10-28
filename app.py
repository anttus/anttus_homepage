import json
from flask import Flask
from flask import render_template
import requests


app = Flask(__name__)
app.static_folder = "static"
cv_url = "https://gist.github.com/anttus/d1285d208ef1cb4d54e27561251e38cd/raw/4a6dd9e1006670718e8e6710e2cd0d1c6b94f9de/cv.json"


@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", data=data)


def load_data():
    data = requests.get(cv_url)
    print(data.content)
    return json.loads(data.content)
