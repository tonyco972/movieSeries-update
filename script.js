const fs = require('fs');
const { chromium } = require('playwright');

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
      await page.waitForTimeout(2000);
    } catch (e) {
      break;
    }
  }

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

  // Controlla il formato dei dati
  console.log(games);

  // Scrivi i dati nel file JSON
  try {
    fs.writeFileSync('games.json', JSON.stringify(games, null, 2));
    console.log(`✅ Salvati ${games.length} giochi in games.json`);
  } catch (error) {
    console.error('Errore nella scrittura del file JSON:', error);
  }

  await browser.close();
})();
