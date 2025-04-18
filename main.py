import json
import os
import requests
from bs4 import BeautifulSoup

# Configurazione
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GIST_ID = os.getenv("GIST_ID")
GIST_FILENAME = "xbox_offerte.json"
XBOX_STORE_URL = "https://www.microsoft.com/it-it/store/deals/xbox"

def recupera_offerte():
    """
    Recupera i giochi in offerta dal Microsoft Store.
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(XBOX_STORE_URL, headers=headers)
    if response.status_code != 200:
        print("❌ Errore nel recupero dei dati.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    giochi = []

    # Esempio di parsing: adattare in base alla struttura attuale del sito
    for item in soup.select(".m-channel-placement-item"):
        titolo = item.select_one(".c-subheading-6").get_text(strip=True)
        prezzo_attuale = item.select_one(".c-price").get_text(strip=True)
        prezzo_originale = item.select_one(".c-price-previous").get_text(strip=True) if item.select_one(".c-price-previous") else None
        immagine = item.select_one("img")["src"] if item.select_one("img") else None

        giochi.append({
            "titolo": titolo,
            "prezzo_attuale": prezzo_attuale,
            "prezzo_originale": prezzo_originale,
            "immagine": immagine
        })

    return giochi

def aggiorna_gist(dati):
    """
    Aggiorna il Gist su GitHub con i dati forniti.
    """
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "files": {
            GIST_FILENAME: {
                "content": json.dumps(dati, indent=2, ensure_ascii=False)
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ Gist aggiornato con successo!")
    else:
        print("❌ Errore durante l'aggiornamento del Gist:")
        print(response.text)

def main():
    """
    Funzione principale che gestisce il flusso.
    """
    print("🔍 Raccolta dati in corso...")
    giochi = recupera_offerte()
    if giochi:
        print(f"📦 Trovati {len(giochi)} giochi in offerta.")
        aggiorna_gist(giochi)
    else:
        print("❌ Nessun gioco trovato. Controlla l'errore.")

if __name__ == "__main__":
    main()
