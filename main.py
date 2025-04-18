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
    Recupera le uscite di film o serie TV per oggi
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

def dettagli_serie(serie_id):
    """
    Ottiene dettagli aggiuntivi di una serie TV: stato, numero stagioni, durata, network, cast
    """
    url = f"https://api.themoviedb.org/3/tv/{serie_id}"
    params = {"api_key": TMDB_API_KEY, "language": "it-IT"}
    r = requests.get(url, params=params)
    if not r.ok:
        print(f"❌ Errore nel recupero dettagli serie {serie_id}")
        return {}

    data = r.json()

    # Recupera il cast
    credits_url = f"https://api.themoviedb.org/3/tv/{serie_id}/credits"
    credits_resp = requests.get(credits_url, params={"api_key": TMDB_API_KEY})
    cast = []
    if credits_resp.ok:
        credits_data = credits_resp.json()
        cast = [m.get("name") for m in credits_data.get("cast", [])[:5]]  # primi 5 attori

    return {
        "stato": data.get("status"),
        "stagioni_totali": data.get("number_of_seasons"),
        "durata_minuti": data.get("episode_run_time")[0] if data.get("episode_run_time") else None,
        "network": data.get("networks", [{}])[0].get("name") if data.get("networks") else None,
        "cast": cast
    }

def prepara_json():
    """
    Prepara i dati delle uscite di film e serie TV
    """
    film = ottieni_uscite("movie")
    serie = ottieni_uscite("tv")
    dati = []

    for item in film + serie:
        tipo = "movie" if "title" in item else "tv"
        titolo = item.get("title") or item.get("name")
        descrizione = item.get("overview", "")
        locandina = f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get("poster_path") else None

        item = arricchisci_con_trailer(item, tipo)

        # Dettagli aggiuntivi per le serie TV
        if tipo == "tv":
            dettaglio = dettagli_serie(item["id"])
            item.update(dettaglio)

        dati.append({
            "titolo": titolo,
            "descrizione": descrizione,
            "locandina": locandina,
            "trailer": item.get("trailer"),
            "tipo": "Film" if tipo == "movie" else "Serie TV",
            "stato": item.get("stato"),
            "stagioni_totali": item.get("stagioni_totali"),
            "durata_minuti": item.get("durata_minuti"),
            "network": item.get("network"),
            "cast": item.get("cast")
        })

    return dati

def aggiorna_gist(dati):
    """
    Aggiorna il Gist con i dati JSON
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
