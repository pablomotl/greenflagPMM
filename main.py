import os
import json
import time
from datetime import datetime
from flask import Flask, request
import gspread
from google.oauth2 import service_account
import requests

# === CONFIGURACIÓN ===

# Variables de entorno
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")
sheet_url = os.getenv("SHEET_URL")

# Credenciales de Google desde variable de entorno
google_credentials_json = json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))

# Autenticación con Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
credentials = service_account.Credentials.from_service_account_info(google_credentials_json, scopes=scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_url(sheet_url).sheet1

# === SERVIDOR FLASK ===

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot activo ✅"

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()

    mensaje = data.get("mensaje", "Sin mensaje")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Escribir en Google Sheet
    sheet.append_row([now, mensaje])

    # Enviar mensaje a Telegram
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"🟢 Notificación:\n\n{mensaje}"
    }
    requests.post(url, json=payload)

    return "Notificado", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
