from fastapi import FastAPI
import requests, hashlib

app = FastAPI()

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
    return {"status": "API running on Vercel 🚀"}

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

@app.post("/verify-otp")
def verify_otp(access_token: str, email: str, otp: str):
    url = f"{BASE_URL}/game/account_security/bind:verify_otp"
    data = {"app_id": APP_ID, "access_token": access_token, "email": email, "otp": otp}
    return requests.post(url, headers=HEADERS, data=data).json()

@app.post("/verify-identity-otp")
def verify_identity_otp(access_token: str, email: str, otp: str):
    url = f"{BASE_URL}/game/account_security/bind:verify_identity"
    data = {"app_id": APP_ID, "access_token": access_token, "email": email, "otp": otp}
    return requests.post(url, headers=HEADERS, data=data).json()

@app.post("/verify-identity-sec")
def verify_identity_sec(access_token: str, code: str):
    url = f"{BASE_URL}/game/account_security/bind:verify_identity"
    data = {
        "app_id": APP_ID,
        "access_token": access_token,
        "secondary_password": sha256_hash(code)
    }
    return requests.post(url, headers=HEADERS, data=data).json()

@app.post("/change-bind")
def change_bind(access_token: str, identity_token: str, verifier_token: str, new_email: str):
    url = f"{BASE_URL}/game/account_security/bind:create_rebind_request"
    data = {
        "app_id": APP_ID,
        "access_token": access_token,
        "identity_token": identity_token,
        "verifier_token": verifier_token,
        "email": new_email
    }
    return requests.post(url, headers=HEADERS, data=data).json()

@app.post("/unbind")
def unbind(access_token: str, identity_token: str):
    url = f"{BASE_URL}/game/account_security/bind:unbind_identity"
    data = {
        "app_id": APP_ID,
        "access_token": access_token,
        "identity_token": identity_token
    }
    return requests.post(url, headers=HEADERS, data=data).json()

@app.post("/cancel")
def cancel(access_token: str):
    url = f"{BASE_URL}/game/account_security/bind:cancel_request"
    data = {"app_id": APP_ID, "access_token": access_token}
    return requests.post(url, headers=HEADERS, data=data).json()
