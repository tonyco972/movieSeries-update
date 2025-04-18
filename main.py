import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Configurazione
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GIST_ID = os.getenv("GIST_ID")
GIST_FILENAME = "uscite_giornaliere.json"
DATA_ODIERNA = datetime.now().strftime("%d %B %Y")

def recupera_uscite():
    """
    Recupera i film e le serie TV in uscita oggi.
    """
    # Esempio: utilizziamo Movieplayer per le serie TV
    url = "https://movieplayer.it/streaming/ultime-uscite/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ Errore nel recupero dei dati.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    uscite = []

    # Parsing degli elementi (adattare in base alla struttura attuale del sito)
    for item in soup.select("div.scheda"):
        titolo_elem = item.select_one("h2")
        descrizione_elem = item.select_one("p")
        immagine_elem = item.select_one("img")
        trailer_elem = item.select_one("a[href*='trailer']")

        titolo = titolo_elem.get_text(strip=True) if titolo_elem else "Titolo non disponibile"
        descrizione = descrizione_elem.get_text(strip=True) if descrizione_elem else "Descrizione non disponibile"
        immagine = immagine_elem["src"] if immagine_elem else None
        trailer = trailer_elem["href"] if trailer_elem else None

        uscite.append({
            "titolo": titolo,
            "descrizione": descrizione,
            "immagine": immagine,
            "trailer": trailer
        })

    return uscite

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
    print(f"🔍 Raccolta dati in corso per il {DATA_ODIERNA}...")
    uscite = recupera_uscite()
    if uscite:
        print(f"📦 Trovati {len(uscite)} titoli in uscita.")
        aggiorna_gist(uscite)
    else:
        print("❌ Nessun titolo trovato. Controlla l'errore.")

if __name__ == "__main__":
    main()
