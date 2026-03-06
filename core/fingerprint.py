import requests
import dns.resolver
import urllib3

# Deshabilitar advertencias de SSL para escaneos masivos
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Diccionario Maestro de Vulnerabilidades validado
# Firma: Lo que el servicio devuelve cuando el subdominio está libre
FINGERPRINTS = {
    "GitHub Pages": {
        "sig": "There isn't a GitHub Pages site here",
        "cname": ["github.io"],
        "nxdomain": False
    },
    "AWS S3": {
        "sig": "NoSuchBucket",
        "cname": ["amazonaws.com"],
        "nxdomain": False
    },
    "Heroku": {
        "sig": "no-such-app.html",
        "cname": ["herokudns.com", "herokupp.com"],
        "nxdomain": False
    },
    "Shopify": {
        "sig": "Sorry, this shop is currently unavailable",
        "cname": ["myshopify.com"],
        "nxdomain": False
    },
    "Azure": {
        "sig": "The specified bucket does not exist",
        "cname": ["blob.core.windows.net", "azureedge.net"],
        "nxdomain": False
    }
}

def check_vulnerability(domain):
    results = {"vulnerable": False, "service": None, "cname": None}
    
    # Paso 1: Resolución DNS (Validación de CNAME)
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 5
        answers = resolver.resolve(domain, 'CNAME')
        cname_record = str(answers[0].target).lower()
        results["cname"] = cname_record
    except Exception:
        return results # Si no hay CNAME, no hay Takeover simplificado

    # Paso 2: Análisis de Respuesta HTTP
    try:
        # Usamos un User-Agent de navegador real para evitar bloqueos
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(f"http://{domain}", headers=headers, timeout=8, verify=False, allow_redirects=True)
        
        for service, data in FINGERPRINTS.items():
            # Si la firma está en el texto de la página y el CNAME coincide
            if data["sig"] in response.text:
                if any(ext in cname_record for ext in data["cname"]):
                    results["vulnerable"] = True
                    results["service"] = service
                    return results
    except:
        pass
        
    return results