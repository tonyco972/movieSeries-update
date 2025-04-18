import requests
import json
import os
from datetime import datetime

# ENV
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GIST_ID = os.getenv("GIST_ID")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GIST_FILENAME = "uscite_giornaliere.json"

def ottieni_uscite(tipo):
    """
    tipo: 'movie' o 'tv'
    """
    oggi = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.themoviedb.org/3/discover/{tipo}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "it-IT",
        "sort_by": "popularity.desc",
        "primary_release_date.gte": oggi,
        "primary_release_date.lte": oggi,
        "region": "IT",
        "with_original_language": "en|it"
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r.json().get("results", [])
    else:
        print(f"Errore TMDb ({tipo}):", r.text)
        return []

def arricchisci_con_trailer(media, tipo):
    """
    Recupera il trailer se disponibile
    """
    trailer_url = f"https://api.themoviedb.org/3/{tipo}/{media['id']}/videos"
    params = {"api_key": TMDB_API_KEY}
    r = requests.get(trailer_url, params=params)
    if r.status_code == 200:
        for video in r.json().get("results", []):
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                media["trailer"] = f"https://www.youtube.com/watch?v={video['key']}"
                return media
    media["trailer"] = None
    return media

def prepara_json():
    film = ottieni_uscite("movie")
    serie = ottieni_uscite("tv")
    dati = []

    for item in film + serie:
        tipo = "movie" if "title" in item else "tv"
        titolo = item.get("title") or item.get("name")
        descrizione = item.get("overview", "")
        locandina = f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get("poster_path") else None

        item = arricchisci_con_trailer(item, tipo)

        dati.append({
            "titolo": titolo,
            "descrizione": descrizione,
            "locandina": locandina,
            "trailer": item.get("trailer"),
            "tipo": "Film" if tipo == "movie" else "Serie TV"
        })

    return dati

def aggiorna_gist(dati):
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
    r = requests.patch(url, headers=headers, json=payload)
    if r.status_code == 200:
        print("✅ Gist aggiornato con successo.")
    else:
        print("❌ Errore aggiornamento gist:", r.text)

def main():
    print("🎬 Recupero delle uscite del giorno...")
    dati = prepara_json()
    if dati:
        print(f"Trovati {len(dati)} elementi.")
        aggiorna_gist(dati)
    else:
        print("Nessuna uscita trovata.")

if __name__ == "__main__":
    main()
