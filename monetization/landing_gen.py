import json

def build_bridge(niche, affiliate_url):
    # Carga la plantilla base
    with open("templates/ultra_fast_bridge.html", "r") as f:
        html_content = f.read()

    # Inyección de URL y metadatos de ofuscación
    final_html = html_content.replace("{{OFFER_LINK}}", affiliate_url)
    
    with open("dist/index.html", "w") as f:
        f.write(final_html)
    print("✅ Landing generada en /dist/index.html lista para despliegue.")

# Ejemplo de uso interno
if __name__ == "__main__":
    # Carga de links desde offers.json
    with open("monetization/offers.json", "r") as f:
        offers = json.load(f)
    # Genera una landing para nicho tecnológico
    build_bridge("tech", offers["tech"])