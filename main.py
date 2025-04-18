import json
import re
import requests
from playwright.sync_api import sync_playwright
import os
import time  # Per aggiungere una pausa (opzionale)

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
        # Avvia il browser in modalità visibile per il debug (facoltativo)
        browser = p.chromium.launch(headless=True)  # Usa headless=False se vuoi vedere il browser
        page = browser.new_page()

        # Carica la pagina
        page.goto("https://www.xbox.com/it-IT/games/browse/DynamicChannel.GameDeals")
        
        # Aggiungi attesa per caricare il DOM (opzionale)
        page.wait_for_load_state('domcontentloaded')  # Aspetta che il DOM sia completamente caricato

        # Aumenta il timeout a 30 secondi per aspettare l'elemento
        try:
            print("🔍 Attesa dell'elemento .gameDiv...")
            page.wait_for_selector(".gameDiv", timeout=30000)  # Aumento il timeout a 30 secondi
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
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "files": {
            GIST_FILENAME: {
                "content": json.dumps(data, indent=2, ensure_ascii=False)
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ Gist aggiornato con successo!")
    else:
        print("❌ Errore durante l'aggiornamento del Gist:")
        print(response.text)

if __name__ == "__main__":
    print("🔍 Raccolta dati in corso...")
    giochi = scrape_xbox_deals()
    if giochi:
        print(f"📦 Trovati {len(giochi)} giochi in offerta.")
        update_gist(giochi)
    else:
        print("❌ Nessun gioco trovato. Controlla l'errore.")
