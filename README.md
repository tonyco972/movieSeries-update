# 🎮 Xbox Game Deals Scraper

Script automatizzato che raccoglie le offerte giornaliere dei giochi Xbox direttamente dal sito ufficiale e aggiorna un Gist con la lista dei titoli in offerta.

---

## 📊 Stato aggiornamento Gist

![Aggiorna Gist con uscite giornaliere](https://github.com/tonyco972/xbox-game-deals/actions/workflows/update-gist.yml/badge.svg)

---

## 📦 Installazione

Clona la repository e installa le dipendenze:

```bash
git clone https://github.com/tonyco972/xbox-game-deals.git
cd xbox-game-deals
npm install
```

🚀 Avvio in locale
Per eseguire lo scraper in locale:

bash
Copy
Edit
npm start
Il risultato sarà salvato in games.json (che è escluso dal repository tramite .gitignore).

🤖 Automazione
Una GitHub Action esegue automaticamente questo scraper ogni giorno alle 6:00 UTC e aggiorna il Gist collegato.

📁 File generati
games.json — elenco aggiornato dei giochi in offerta con:

🎮 Titolo

💶 Prezzo scontato

💸 Prezzo originale

🖼️ Immagine di copertina

🏷️ Percentuale di sconto

📋 Dipendenze
Playwright

Axios

📜 Licenza
MIT
