import requests
import os

def track_revenue():
    # Ejemplo con API de CPALead (debes obtener tu API Key en el dashboard)
    api_key = os.getenv("CPA_API_KEY")
    url = f"https://www.cpalead.com/dashboard/reports/campaign_stats_api.php?api_key={api_key}&format=json"
    
    try:
        r = requests.get(url)
        data = r.json()
        unpaid_balance = data.get("unpaid_balance", 0)
        
        if float(unpaid_balance) >= 50.0:
            msg = f"💰 *LIQUIDACIÓN DISPONIBLE*\nSaldo: `${unpaid_balance}`\nYa puedes solicitar el retiro a tu Wallet."
            # send_telegram(msg)
    except:
        print("Error consultando balance.")