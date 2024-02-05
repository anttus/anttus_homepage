from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests, json
from uvicorn.workers import UvicornWorker

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

cv_url = (
    "https://gist.githubusercontent.com/anttus/d1285d208ef1cb4d54e27561251e38cd/raw/"
)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"data": load_data()}
    )


def load_data():
    try:
        r = requests.get(cv_url)
        return json.loads(r.content)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

class MyUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "log_config": "logging.yaml",
    }
