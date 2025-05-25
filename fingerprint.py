from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import hashlib

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class FingerprintPayload(BaseModel):
    resolution: str
    platform: str
    language: str
    timezone: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/device-fingerprint")
async def generate_fingerprint(request: Request, data: FingerprintPayload):
    # nepoužíváme IP ani user-agent, pro vyšší stabilitu mezi prohlížeči/sítěmi
    raw = f"{data.resolution}|{data.platform}|{data.language}|{data.timezone}"
    print("Fingerprint data:", raw)
    fingerprint = hashlib.sha256(raw.encode()).hexdigest()
    return JSONResponse(content={"fingerprint": fingerprint})


@app.post("/device-fingerprint-details")
async def fingerprint_details(request: Request, data: FingerprintPayload):
    raw = f"{data.resolution}|{data.platform}|{data.language}|{data.timezone}"
    fingerprint = hashlib.sha256(raw.encode()).hexdigest()
    return {
        "fingerprint": fingerprint,
        "resolution": data.resolution,
        "platform": data.platform,
        "language": data.language,
        "timezone": data.timezone
    }
