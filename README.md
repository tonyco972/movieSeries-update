🎬 Uscite Film & Serie TV – Gist Automagico
Benvenuto! 👋
Questo piccolo progetto si prende cura di una grande missione:
📆 Ogni giorno controlla quali film e serie TV vengono rilasciati
🍿 Raccoglie titolo, descrizione, locandina e (se disponibile) anche il trailer
📤 E aggiorna un Gist GitHub con tutte le uscite del giorno in formato JSON!

Per i veri appassionati che vogliono essere sempre aggiornati, senza dover cercare ovunque! ❤️

🚀 Come funziona
⏰ Una GitHub Action si attiva ogni giorno alle 06:00 UTC

🤖 Lo script interroga l’API di TMDb (The Movie Database)

🧠 Filtra solo le uscite del giorno corrente (film e serie TV)

📎 Estrae:

Titolo

Descrizione

Locandina

Trailer (se disponibile)

Tipo (Film o Serie TV)

✨ E aggiorna un Gist GitHub pubblico o privato con tutte queste informazioni, in un file JSON pulito e leggibile.

📦 Esempio di Output JSON
json
Copy
Edit
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
🧪 Tecnologie usate
🐍 Python 3.10

🌍 TMDb API per ottenere dati precisi e affidabili

⚙️ GitHub Actions per l’automazione giornaliera

💾 GitHub Gist per pubblicare i risultati

🛠️ Personalizzabile per il tuo Gist e le tue preferenze

🧑‍💻 Come personalizzarlo
Se vuoi usarlo con il tuo Gist:
Crea un Gist su GitHub (pubblico o privato).

Ottieni il suo ID (presente nell’URL).

Vai nella tua repo su GitHub.

Aggiungi i seguenti segreti nella sezione GitHub Secrets:

GIST_ID: L'ID del tuo Gist.

PERSONAL_GIST_TOKEN: Un GitHub token con accesso ai tuoi Gist.

TMDB_API_KEY: La tua chiave API da TMDb.

🚀 Come avviare l'azione:
Configura il tuo progetto:
Dopo aver configurato i segreti, l’azione GitHub si attiverà automaticamente ogni giorno alle 06:00 UTC.

Automazione:
L'azione eseguirà lo script Python per raccogliere i dati di TMDb, filtrarli per il giorno corrente, e infine aggiornerà il Gist con i nuovi film e serie TV.

Gist aggiornato:
Il file JSON generato sarà disponibile nel tuo Gist, pronto per essere utilizzato.

📱 Idee per il futuro
Esportare anche in formato Markdown/HTML per avere una vista più bella e accessibile dei risultati.

Aggiungere le piattaforme di streaming per mostrare dove è disponibile ogni film/serie TV.

Creare un sito web con tutte le uscite giornaliere in bella vista.

Mandare notifiche Telegram per avvisarti ogni volta che un nuovo aggiornamento viene caricato nel Gist.

Con questo sistema, sarai sempre aggiornato sulle nuove uscite cinematografiche e televisive senza fare fatica. Buona visione! 🎥🍿
