import sqlite3
import os
import subprocess
from fingerprint import check_vulnerability
import requests

# Configuración de base de datos
DB_PATH = "database/inventory.db"

def init_db():
    # Esta línea es la que falta para evitar el error en GitHub
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) 
    
    conn = sqlite3.connect(DB_PATH)
    curr = conn.cursor()
    curr.execute('''CREATE TABLE IF NOT EXISTS findings 
                    (domain TEXT PRIMARY KEY, service TEXT, status TEXT)''')
    conn.commit()
    conn.close()

def send_telegram(message):
    token = os.getenv("TG_TOKEN")
    chat_id = os.getenv("TG_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=Markdown"
    requests.get(url)

def run_scanner():
    init_db()
    # Leemos los subdominios encontrados por subfinder (generado en el workflow)
    if not os.path.exists("live_subs.txt"):
        return

    conn = sqlite3.connect(DB_PATH)
    curr = conn.cursor()

    with open("live_subs.txt", "r") as f:
        for line in f:
            domain = line.strip()
            if not domain: continue
            
            # Verificar si ya lo procesamos
            curr.execute("SELECT domain FROM findings WHERE domain=?", (domain,))
            if curr.fetchone(): continue

            print(f"[*] Analizando: {domain}")
            status = check_vulnerability(domain)
            
            if status["vulnerable"]:
                msg = f"💎 *¡NUEVO TAKEOVER DETECTADO!*\n\n" \
                      f"🌐 *Dominio:* `{domain}`\n" \
                      f"🛠️ *Servicio:* {status['service']}\n" \
                      f"🔗 *CNAME:* `{status['cname']}`\n\n" \
                      f"👉 _Acción: Reclama este dominio en el proveedor indicado._"
                send_telegram(msg)
                curr.execute("INSERT INTO findings VALUES (?, ?, ?)", (domain, status["service"], "VULNERABLE"))
                conn.commit()
    
    conn.close()

if __name__ == "__main__":
    run_scanner()