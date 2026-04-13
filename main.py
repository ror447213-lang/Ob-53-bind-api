from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, hashlib

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://100067.connect.garena.com"
APP_ID = "100067"

HEADERS = {
    "User-Agent": "GarenaMSDK/4.0.39",
    "Content-Type": "application/x-www-form-urlencoded"
}

def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

@app.get("/")
def home():
    return {"status": "Railway API Running 🚀"}

@app.get("/bind-info")
def bind_info(access_token: str):
    url = f"{BASE_URL}/game/account_security/bind:get_bind_info"
    params = {"app_id": APP_ID, "access_token": access_token}
    return requests.get(url, headers=HEADERS, params=params).json()

@app.post("/send-otp")
def send_otp(access_token: str, email: str):
    url = f"{BASE_URL}/game/account_security/bind:send_otp"
    data = {"app_id": APP_ID, "access_token": access_token, "email": email}
    return requests.post(url, headers=HEADERS, data=data).json()
