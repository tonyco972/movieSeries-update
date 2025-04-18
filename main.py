import os
import requests
import json
from datetime import datetime, timedelta

# Configurazioni
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GIST_ID = os.getenv("GIST_ID")
GIST_FILENAME = "uscite_giornaliere.json"

BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"Authorization": f"Bearer {TMDB_API_KEY}"}
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Calcola il periodo (oggi + 6 giorni)
oggi = datetime.utcnow().date()
fine = oggi + timedelta(days=6)
oggi_str = oggi.strftime("%Y-%m-%d")
fine_str = fine.strftime("%Y-%m-%d")
periodo_testuale = f"dal {oggi.strftime('%d %B %Y')} al {fine.strftime('%d %B %Y')}"

def get_genres_map():
    """
    Restituisce un dizionario con gli ID dei generi e i loro nomi
    """
    genres = {}
    for tipo in ["movie", "tv"]:
        url = f"{BASE_URL}/genre/{tipo}/list?language=it-IT"
        response = requests.get(url, headers=HEADERS)
        if response.ok:
            for genre in response.json().get("genres", []):
                genres[genre["id"]] = genre["name"]
    return genres

def get_trailer(item_id, tipo):
    """
    Restituisce l'URL del trailer YouTube se disponibile
    """
    url = f"{BASE_URL}/{tipo}/{item_id}/videos?language=it-IT"
    response = requests.get(url, headers=HEADERS)
    if response.ok:
        for video in response.json().get("results", []):
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                return f"https://www.youtube.com/watch?v={video['key']}"
    return None

def fetch_releases(tipo, genres_map):
    """
    Recupera i film o le serie TV in uscita nel periodo specificato
    """
    endpoint = "movie/upcoming" if tipo == "movie" else "tv/airing_today"
    url = f"{BASE_URL}/discover/{tipo}?primary_release_date.gte={oggi_str}&primary_release_date.lte={fine_str}&language=it-IT&region=IT&sort_by=primary_release_date.asc"
    response = requests.get(url, headers=HEADERS)
    results = []

    if response.ok:
        for item in response.json().get("results", []):
            genres_ids = item.get("genre_ids", [])
            genere = genres_map.get(genres_ids[0], "Sconosciuto") if genres_ids else "N/A"
            results.append({
                "titolo": item.get("title") or item.get("name"),
                "titolo_originale": item.get("original_title") or item.get("original_name"),
                "descrizione": item.get("overview"),
                "genere": genere,
                "lingua_originale": item.get("original_language"),
                "data_uscita": item.get("release_date") or item.get("first_air_date"),
                "media_voto": item.get("vote_average"),
                "numero_voti": item.get("vote_count"),
                "tipo": "Film" if tipo == "movie" else "Serie TV",
                "stato": None,  # Può essere esteso con /tv/{id} se vuoi
                "trailer": get_trailer(item["id"], tipo),
                "locandina": f"{IMAGE_BASE}{item['poster_path']}" if item.get("poster_path") else None,
                "tmdb_url": f"https://www.themoviedb.org/{tipo}/{item['id']}"
            })

    return results

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

    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ Gist aggiornato con successo!")
    else:
        print("❌ Errore durante l'aggiornamento del Gist:")
        print(response.text)

def main():
    print(f"🎬 Raccolta delle uscite in programma {periodo_testuale}...")
    genres_map = get_genres_map()
    film = fetch_releases("movie", genres_map)
    serie = fetch_releases("tv", genres_map)

    dati = {
        "periodo": periodo_testuale,
        "film": film,
        "serie_tv": serie
    }

    aggiorna_gist(dati)

if __name__ == "__main__":
    main()
