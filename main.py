import json
import re
import requests
from playwright.sync_api import sync_playwright
import os

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GIST_ID = os.getenv("GIST_ID")
GIST_FILENAME = "xbox_offerte.json"

def estrai_sconto(testo):
    prezzi = re.findall(r'\d{1,3},\d{2}', testo)
    if len(prezzi) >= 2:
        originale = float(prezzi[0].replace(",", "."))
        scontato = float(prezzi[-1].replace(",", "."))
        if scontato < originale:
            return originale, scontato
    return None, None

def scrape_xbox_deals():
    with sync_playwright() as p:
        # Avvia il browser
        browser = p.chromium.launch(headless=True)  # Usa headless=False se vuoi vedere il browser
        page = browser.new_page()

        # Carica la pagina
        page.goto("https://www.xbox.com/it-IT/games/browse/DynamicChannel.GameDeals")

        # Aspetta che il DOM sia completamente caricato
        page.wait_for_load_state('domcontentloaded')  # Aspetta che la pagina si carichi completamente
        
        # Aspetta che l'elemento di interesse sia presente, aumenta il timeout se necessario
        try:
            print("🔍 Attesa dell'elemento .gameDiv...")
            page.wait_for_selector(".gameDiv", timeout=60000)  # Timeout aumentato a 60 secondi
            print("✅ Elemento .gameDiv trovato!")
        except Exception as e:
            print(f"❌ Errore: {str(e)}")
            browser.close()
            return []

        items = []
        game_cards = page.query_selector_all(".gameDiv")

        print(f"📦 Trovati {len(game_cards)} schede di gioco.")

        for card in game_cards:
            title_el = card.query_selector(".gameTitle") or card.query_selector("h3")
            image_el = card.query_selector("img")
            price_el = card.query_selector(".Price")

            title = title_el.inner_text().strip() if title_el else "N/A"
            image = image_el.get_attribute("src") if image_el else "N/A"
            price_text = price_el.inner_text().strip() if price_el else ""

            # Escludi giochi gratuiti
            if "gratuito" in price_text.lower() or "free" in price_text.lower():
                continue

            originale, scontato = estrai_sconto(price_text)

            if originale is not None:
                items.append({
                    "title": title,
                    "image": image,
                    "price_originale": originale,
                    "prezzo_scontato": scontato,
                    "sconto_percentuale": round(100 * (originale - scontato) / originale, 1)
                })

        browser.close()
        return items

def update_gist(data):
    url = f"https://api.github
