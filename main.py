import json
import requests
import os

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GIST_ID = os.getenv("GIST_ID")
GIST_FILENAME = "xbox_offerte.json"
API_URL = "https://www.xbox-now.com/en/deal-list"  # URL per l'estrazione delle offerte

def aggiorna_gist(dati):
    """
    Funzione per aggiornare il Gist su GitHub
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

def recupera_offerte():
    """
    Funzione per recuperare i giochi in offerta da Xbox Now
    """
    response = requests.get(API_URL)
    if response.status_code == 200:
        offerte = response.json()
        return offerte
    else:
        print("❌ Errore nel recupero dei dati dalle offerte.")
        return []

def main():
    """
    Funzione principale che gestisce il flusso
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
