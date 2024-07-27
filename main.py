import requests, json, os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn.workers import UvicornWorker
from redis import Redis
from tasks import process_data
from dotenv import load_dotenv

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

load_dotenv()
REDIS_HOST: str = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT: int = 6379

if REDIS_HOST:
    r = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    r.ping()

cv_url = (
    "https://gist.githubusercontent.com/anttus/d1285d208ef1cb4d54e27561251e38cd/raw/"
)


def load_data():
    try:
        r = requests.get(cv_url)
        return json.loads(r.content)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


@app.get("/")
async def root(request: Request):
    page_view_count = r.get("page_view_count") or 0
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"page_view_count": page_view_count},
    )


@app.get("/cv")
async def cv(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="cv.html",
        context={"data": load_data()},
    )


@app.post("/collect-data")
async def collect_data(request: Request):
    data = await request.json()
    process_data(data)
    return {"message": "Data received"}


class MyUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "log_config": "logging.yaml",
    }
