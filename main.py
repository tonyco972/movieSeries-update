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

def ottieni_trailer(tipo, id_):
    url = f"https://api.themoviedb.org/3/{tipo}/{id_}/videos"
    params = {"api_key": TMDB_API_KEY}
    r = requests.get(url, params=params)
    if r.ok:
        for v in r.json().get("results", []):
            if v["site"] == "YouTube" and v["type"] == "Trailer":
                return f"https://www.youtube.com/watch?v={v['key']}"
    return None

def ottieni_cast(tipo, id_):
    url = f"https://api.themoviedb.org/3/{tipo}/{id_}/credits"
    params = {"api_key": TMDB_API_KEY}
    r = requests.get(url, params=params)
    if r.ok:
        return [att["name"] for att in r.json().get("cast", [])[:5]]
    return []

def dettagli_serie(tv_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_id}?language=it-IT&api_key={TMDB_API_KEY}"
    r = requests.get(url)
    if r.ok:
        data = r.json()
        return {
            "stato": data.get("status"),
            "durata_minuti": data.get("episode_run_time", [None])[0],
            "stagioni_totali": data.get("number_of_seasons"),
            "network": data["networks"][0]["name"] if data.get("networks") else None
        }
    return {}

def episodio_del_giorno(tv_id):
    oggi = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.themoviedb.org/3/tv/{tv_id}/season/1?language=it-IT&api_key={TMDB_API_KEY}"
    r = requests.get(url)
    if r.ok:
        for season in range(1, 100):  # limite massimo stagioni
            url_season = f"https://api.themoviedb.org/3/tv/{tv_id}/season/{season}?language=it-IT&api_key={TMDB_API_KEY}"
            rs = requests.get(url_season)
            if not rs.ok:
                break
            for ep in rs.json().get("episodes", []):
                if ep.get("air_date") == oggi:
                    return {
                        "titolo_episodio": ep.get("name"),
                        "descrizione_episodio": ep.get("overview"),
                        "numero_stagione": ep.get("season_number"),
                        "numero_episodio": ep.get("episode_number")
                    }
    return {}

def prepara_json():
    film = ottieni_uscite("movie")
    serie = ottieni_uscite("tv")
    dati = []

    for item in film + serie:
        tipo = "movie" if "title" in item else "tv"
        titolo = item.get("title") or item.get("name")
        descrizione = item.get("overview", "")
        locandina = f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get("poster_path") else None
        trailer = ottieni_trailer(tipo, item["id"])
        cast = ottieni_cast(tipo, item["id"])
        dettaglio = dettagli_serie(item["id"]) if tipo == "tv" else {}
        episodio = episodio_del_giorno(item["id"]) if tipo == "tv" else {}

        dati.append({
            "titolo": titolo,
            "descrizione": descrizione,
            "locandina": locandina,
            "trailer": trailer,
            "tipo": "Film" if tipo == "movie" else "Serie TV",
            "cast_principale": cast,
            **dettaglio,
            **episodio
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
