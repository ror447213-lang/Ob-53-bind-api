from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import hashlib

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- CONFIG ----------------
BASE_URL = "https://100067.connect.garena.com"
APP_ID = "100067"

HEADERS = {
    "User-Agent": "GarenaMSDK/4.0.39",
    "Content-Type": "application/x-www-form-urlencoded"
}

# ---------------- HASH ----------------
def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

# ---------------- SAFE REQUEST ----------------
def safe_post(url, data):
    try:
        return requests.post(url, headers=HEADERS, data=data, timeout=10).json()
    except Exception as e:
        return {"error": str(e)}

def safe_get(url, params):
    try:
        return requests.get(url, headers=HEADERS, params=params, timeout=10).json()
    except Exception as e:
        return {"error": str(e)}

# =========================================================
# ROOT
# =========================================================
@app.get("/")
def home():
    return {"status": "Garena Bind API Running 🚀"}

# =========================================================
# 1️⃣ BIND INFO
# =========================================================
@app.get("/bind-info")
def bind_info(access_token: str):
    url = f"{BASE_URL}/game/account_security/bind:get_bind_info"
    params = {"app_id": APP_ID, "access_token": access_token}
    return safe_get(url, params)

# =========================================================
# 2️⃣ SEND OTP (GET + POST)
# =========================================================
@app.post("/send-otp")
def send_otp_post(access_token: str, email: str):
    url = f"{BASE_URL}/game/account_security/bind:send_otp"
    data = {
        "app_id": APP_ID,
        "access_token": access_token,
        "email": email,
        "locale": "en_PK",
        "region": "PK"
    }
    return safe_post(url, data)

@app.get("/send-otp")
def send_otp_get(access_token: str, email: str):
    return send_otp_post(access_token, email)

# =========================================================
# 3️⃣ VERIFY OTP
# =========================================================
@app.post("/verify-otp")
def verify_otp(access_token: str, email: str, otp: str):
    url = f"{BASE_URL}/game/account_security/bind:verify_otp"
    data = {
        "app_id": APP_ID,
        "access_token": access_token,
        "email": email,
        "otp": otp
    }
    return safe_post(url, data)

# =========================================================
# 4️⃣ VERIFY IDENTITY (OTP)
# =========================================================
@app.post("/verify-identity-otp")
def verify_identity_otp(access_token: str, email: str, otp: str):
    url = f"{BASE_URL}/game/account_security/bind:verify_identity"
    data = {
        "app_id": APP_ID,
        "access_token": access_token,
        "email": email,
        "otp": otp
    }
    return safe_post(url, data)

# =========================================================
# 5️⃣ VERIFY IDENTITY (SECURITY CODE)
# =========================================================
@app.post("/verify-identity-sec")
def verify_identity_sec(access_token: str, code: str):
    url = f"{BASE_URL}/game/account_security/bind:verify_identity"
    data = {
        "app_id": APP_ID,
        "access_token": access_token,
        "secondary_password": sha256_hash(code)
    }
    return safe_post(url, data)

# =========================================================
# 6️⃣ CHANGE BIND
# =========================================================
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
    return safe_post(url, data)

# =========================================================
# 7️⃣ UNBIND EMAIL
# =========================================================
@app.post("/unbind")
def unbind(access_token: str, identity_token: str):
    url = f"{BASE_URL}/game/account_security/bind:unbind_identity"
    data = {
        "app_id": APP_ID,
        "access_token": access_token,
        "identity_token": identity_token
    }
    return safe_post(url, data)

# =========================================================
# 8️⃣ CANCEL BIND
# =========================================================
@app.post("/cancel")
def cancel(access_token: str):
    url = f"{BASE_URL}/game/account_security/bind:cancel_request"
    data = {
        "app_id": APP_ID,
        "access_token": access_token
    }
    return safe_post(url, data)
