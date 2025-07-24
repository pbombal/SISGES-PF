
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from pathlib import Path

BASE_URL = "https://sistemas.sence.cl/sipfor/Planes/Catalogo.aspx"
OUTPUT_DIR = Path("data/planes_formativos")
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def ensure_output_folder():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_soup(url):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def descargar_planes():
    print("🔍 Accediendo al catálogo...")
    soup = get_soup(BASE_URL)

    links = soup.find_all("a")
    pdf_links = [a for a in links if "href" in a.attrs and a["href"].lower().endswith(".pdf")]

    print(f"📄 Se encontraron {len(pdf_links)} archivos PDF.")

    for i, link in enumerate(pdf_links, 1):
        href = link["href"]
        nombre = link.text.strip() or f"plan_{i}.pdf"
        url_pdf = urljoin(BASE_URL, href)
        nombre_archivo = OUTPUT_DIR / f"{nombre.replace('/', '_').replace(' ', '_')}.pdf"

        try:
            r = requests.get(url_pdf, headers=HEADERS)
            r.raise_for_status()
            with open(nombre_archivo, "wb") as f:
                f.write(r.content)
            print(f"✅ ({i}) Descargado: {nombre_archivo.name}")
        except Exception as e:
            print(f"❌ ({i}) Error al descargar {url_pdf}: {e}")

if __name__ == "__main__":
    ensure_output_folder()
    descargar_planes()
