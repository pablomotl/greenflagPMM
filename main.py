# ==============================
# GreenFlag Master Script – Pablo Motl
# Alertas + Google Sheets + Telegram + Performance
# Ejecuta automáticamente cada hora con cron
# ==============================

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time
from datetime import datetime
from flask import Flask

# === CONFIGURACIÓN ===

bot_token = "8126039848:AAG3Mkr4jbe5KJYoHrfQ4HlyIricgp8ZQYM"
chat_id = "-1002341211105"
sheet_url = "https://docs.google.com/spreadsheets/d/1GhtF77BkhUXNW-LdRE9DGIBTwcIRhNIX2Yb3pdGIM1w/edit"

# === AUTENTICACIÓN CON GOOGLE SHEETS ===

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credenciales.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(sheet_url).sheet1

# === DATOS DE EJEMPLO PARA PRUEBA INICIAL ===

activo = "ETH"
tipo = "Cripto"
fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
monto_usd = 150.0
precio_entrada = 2500
precio_actual = 2900
resultado = round(precio_actual - precio_entrada, 2)
rendimiento_pct = round((resultado / precio_entrada) * 100, 2)
ytd = rendimiento_pct  # simplificado
mtm = 3.1  # ejemplo estático

# === PUBLICACIÓN EN TELEGRAM ===

mensaje_telegram = f"""
📊 [CIERRE AUTOMÁTICO – {fecha}]

- Activo: {activo}
- Tipo: {tipo}
- Inversión: ${precio_entrada} MXN → Valor actual: ${precio_actual} MXN
- Resultado: {f"{resultado:+.0f}"} MXN ({rendimiento_pct}%)
- YTD: {ytd}%
- MTM: {mtm}%

#GreenFlag #PMAbundancia
"""

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
print("➡️ Intentando enviar mensaje a Telegram...")
print("Mensaje:", mensaje_telegram)
response = requests.post(url,
                         data={
                             "chat_id": chat_id,
                             "text": mensaje_telegram
                         })
print("🧾 Respuesta de Telegram:", response.text)

print("➡️ Intentando enviar mensaje a Telegram...")
print("Mensaje:", mensaje_telegram)

# === REGISTRO EN GOOGLE SHEETS ===

sheet.append_row([
    fecha, activo, tipo, monto_usd, precio_entrada, precio_actual, resultado,
    f"{rendimiento_pct}%", f"{ytd}%", f"{mtm}%", "Abierta"
])

# === ACTIVACIÓN DEL SERVIDOR PARA UPTIMEROBOT ===

app = Flask('')


@app.route('/')
def home():
    return "Sistema activo."


app.run(host='0.0.0.0', port=8080)
from flask import request


@app.route('/', methods=['GET', 'HEAD'])
def home():
    if request.method == 'HEAD':
        return '', 200
    return "Sistema activo."
