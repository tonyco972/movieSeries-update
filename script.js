const fs = require('fs');
const { chromium } = require('playwright');
const axios = require('axios');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto('https://www.xbox.com/it-IT/games/browse/DynamicChannel.GameDeals', {
    waitUntil: 'networkidle',
    timeout: 60000,
  });

  // Scrolla e clicca "Carica altro" fino a che è visibile
  while (true) {
    try {
      await page.waitForSelector('button:has-text("Carica altro")', { timeout: 5000 });
      await page.click('button:has-text("Carica altro")');
      await page.waitForTimeout(2000); // attende il caricamento dei nuovi giochi
    } catch (e) {
      break; // esce dal ciclo quando il bottone non c'è più
    }
  }

  // Ora raccogliamo i giochi
  await page.waitForSelector('.ProductCard-module__cardWrapper___6Ls86');

  const games = await page.$$eval('.ProductCard-module__cardWrapper___6Ls86', cards => {
    return cards.map(card => {
      const title = card.querySelector('.ProductCard-module__title___nHGIp')?.innerText.trim() || null;
      const price = card.querySelector('.Price-module__boldText___1i2Li')?.innerText.trim() || null;
      const originalPrice = card.querySelector('.Price-module__originalPrice___XNCxs')?.innerText.trim() || null;
      const image = card.querySelector('img')?.src || null;
      const discount = card.querySelector('.ProductCard-module__discountTag___OjGFy')?.innerText.trim() || null;

      return {
        title,
        price,
        originalPrice,
        image,
        discount
      };
    });
  });

  // Scrive i dati su un file JSON
  const gamesFilePath = 'games.json';
  fs.writeFileSync(gamesFilePath, JSON.stringify(games, null, 2));
  console.log(`✅ Salvati ${games.length} giochi in games.json`);

  await browser.close();

  // Ora aggiorniamo il Gist con il file JSON generato
  const gistId = process.env.GIST_ID;
  const githubToken = process.env.GITHUB_TOKEN;
  const gistUrl = `https://api.github.com/gists/${gistId}`;

  // Carica il file JSON su Gist
  const gistContent = fs.readFileSync(gamesFilePath, 'utf8');

  await axios({
    method: 'PATCH',
    url: gistUrl,
    headers: {
      'Authorization': `token ${githubToken}`,
      'Accept': 'application/vnd.github.v3+json',
    },
    data: {
      files: {
        'games.json': {
          content: gistContent,
        }
      }
    }
  });

  console.log('✅ Gist aggiornato con successo!');
})();
