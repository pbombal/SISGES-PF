
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
from pathlib import Path
import requests

BASE_URL = "https://sistemas.sence.cl/sipfor/Planes/Catalogo.aspx"
DOWNLOAD_DIR = Path("data/planes_formativos")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(options=chrome_options)

def descargar_pdf(url_pdf, nombre_archivo):
    try:
        r = requests.get(url_pdf, timeout=10)
        r.raise_for_status()
        with open(nombre_archivo, "wb") as f:
            f.write(r.content)
        print(f"✅ Descargado: {nombre_archivo.name}")
    except Exception as e:
        print(f"❌ Error al descargar {url_pdf}: {e}")

def main():
    print("🌐 Iniciando navegador...")
    driver = setup_driver()
    driver.get(BASE_URL)
    time.sleep(5)

    print("🔍 Buscando enlaces a PDF...")
    links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
    print(f"📄 Se encontraron {len(links)} enlaces a PDF.")

    for i, link in enumerate(links, 1):
        url = link.get_attribute("href")
        texto = link.text.strip() or f"plan_{i}"
        nombre_archivo = DOWNLOAD_DIR / f"{texto.replace('/', '_').replace(' ', '_')}.pdf"
        descargar_pdf(url, nombre_archivo)

    driver.quit()

if __name__ == "__main__":
    main()
