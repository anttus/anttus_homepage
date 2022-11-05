import json
from flask import Flask
from flask import render_template
import requests
from waitress import serve


app = Flask(__name__)
app.static_folder = "static"
cv_url = "https://gist.github.com/anttus/d1285d208ef1cb4d54e27561251e38cd/raw/4a6dd9e1006670718e8e6710e2cd0d1c6b94f9de/cv.json"


@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", data=data)


def load_data():
    try:
        r = requests.get(cv_url)
        print("Successfully loaded content")
        return json.loads(r.content)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5050, url_scheme='https')
