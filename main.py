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

def ottieni_generi():
    generi = {}
    for tipo in ["movie", "tv"]:
        url = f"https://api.themoviedb.org/3/genre/{tipo}/list?language=it-IT&api_key={TMDB_API_KEY}"
        r = requests.get(url)
        if r.ok:
            for g in r.json().get("genres", []):
                generi[g["id"]] = g["name"]
    return generi

def arricchisci_con_trailer(media, tipo):
    url = f"https://api.themoviedb.org/3/{tipo}/{media['id']}/videos?api_key={TMDB_API_KEY}"
    r = requests.get(url)
    if r.ok:
        for v in r.json().get("results", []):
            if v["site"] == "YouTube" and v["type"] == "Trailer":
                media["trailer"] = f"https://www.youtube.com/watch?v={v['key']}"
                return media
    media["trailer"] = None
    return media

def prepara_json():
    film = ottieni_uscite("movie")
    serie = ottieni_uscite("tv")
    generi = ottieni_generi()
    dati = []

    for item in film + serie:
        tipo = "movie" if "title" in item else "tv"
        titolo = item.get("title") or item.get("name")
        descrizione = item.get("overview", "")
        locandina = f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get("poster_path") else None
        data_uscita = item.get("release_date") or item.get("first_air_date")
        lingua = item.get("original_language", "")
        voto = item.get("vote_average")
        voti = item.get("vote_count")
        id_tmdb = item.get("id")
        genere = generi.get(item["genre_ids"][0], "Sconosciuto") if item.get("genre_ids") else "N/A"

        item = arricchisci_con_trailer(item, tipo)

        dati.append({
            "titolo": titolo,
            "descrizione": descrizione,
            "locandina": locandina,
            "trailer": item.get("trailer"),
            "genere": genere,
            "lingua_originale": lingua,
            "media_voto": voto,
            "numero_voti": voti,
            "data_uscita": data_uscita,
            "tipo": "Film" if tipo == "movie" else "Serie TV",
            "tmdb_url": f"https://www.themoviedb.org/{tipo}/{id_tmdb}"
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
