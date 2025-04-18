# 🎬 Uscite Film & Serie TV – Gist Automagico

**Benvenuto!** 👋  
Questo piccolo progetto si prende cura di una grande missione:  
📆 Ogni giorno controlla **quali film e serie TV vengono rilasciati**  
🍿 Raccoglie titolo, descrizione, locandina e (se disponibile) anche il trailer  
📤 E aggiorna un Gist GitHub con tutte le uscite del giorno in formato JSON!

> Per i veri appassionati che vogliono essere sempre aggiornati, senza dover cercare ovunque! ❤️

---

## 🚀 Come funziona

1. ⏰ Una GitHub Action si attiva ogni giorno alle **06:00 UTC**
2. 🤖 Lo script interroga l’[API di TMDb (The Movie Database)](https://www.themoviedb.org/documentation/api)
3. 🧠 Filtra **solo le uscite del giorno corrente** (film e serie TV)
4. 📎 Estrae:
   - Titolo
   - Descrizione
   - Locandina
   - Trailer (se disponibile)
   - Tipo (Film o Serie TV)
5. ✨ E aggiorna un **Gist GitHub pubblico o privato** con tutte queste informazioni, in un file JSON pulito e leggibile.

---

## 📦 Esempio di Output JSON

```json
[
  {
    "titolo": "Inside Out 2",
    "descrizione": "Riley è cresciuta, ma nella sua mente c'è ancora tanto da scoprire...",
    "locandina": "https://image.tmdb.org/t/p/w500/poster.jpg",
    "trailer": "https://www.youtube.com/watch?v=abc123",
    "tipo": "Film"
  },
  {
    "titolo": "Stranger Things - Stagione 5",
    "descrizione": "Tornano gli anni ’80 più spaventosi della TV...",
    "locandina": "https://image.tmdb.org/t/p/w500/stranger.jpg",
    "trailer": null,
    "tipo": "Serie TV"
  }
]
```

## 🧪 Tecnologie usate
- 🐍 Python 3.10

- 🌍 TMDb API per ottenere dati precisi e affidabili

- ⚙️ GitHub Actions per l’automazione giornaliera

- 💾 GitHub Gist per pubblicare i risultati

- 🛠️ Come personalizzarlo

## Se vuoi usarlo con il tuo Gist:

- Crea un Gist su GitHub (pubblico o privato)

- Ottieni il suo ID (presente nell’URL)

- Vai nella tua repo su GitHub

- Aggiungi i seguenti segreti:

1 GIST_ID | L'ID del tuo Gist
2 PERSONAL_GIST_TOKEN | Un GitHub token con accesso ai tuoi Gist
3 TMDB_API_KEY | La tua chiave API da TMDb

## ❤️ Idee per il futuro
 
 - Esportare anche in formato Markdown/HTML

 - Aggiungere le piattaforme di streaming

 - Creare un sito web con tutte le uscite giornaliere in bella vista

 Mandare notifiche Telegram?
