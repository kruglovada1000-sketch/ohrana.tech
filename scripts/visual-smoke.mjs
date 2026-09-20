import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const BASE = process.env.VISUAL_BASE_URL || 'http://127.0.0.1:4173';
const OUT = path.join(ROOT, 'visual-qa');
fs.mkdirSync(OUT, { recursive: true });

function readJson(rel, fallback) {
  const p = path.join(ROOT, rel);
  if (!fs.existsSync(p)) return fallback;
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

const objects = readJson('site-src/object-pages.json', []);
const shared = readJson('site-src/shared-pages.json', []);
const custom = readJson('site-src/custom-pages.json', []);
const documents = readJson('site-src/document-pages.json', []);
const articles = readJson('site-src/article-pages.generated.json', { regular: [], custom: [] });

const urls = new Set(['/']);
urls.add('/ohrana-skladov/');
urls.add('/ceny/');
for (const row of [...objects, ...shared, ...custom]) urls.add(`/${row.slug}/`);
for (const row of documents) {
  const rel = String(row.path || '').replace(/index\.html$/i, '');
  urls.add('/' + rel.replace(/^\/+/, ''));
}
urls.add('/stati/');
for (const row of [...(articles.regular || []), ...(articles.custom || [])]) {
  urls.add(`/stati/${row.file}`);
}

const viewports = [
  { name: 'desktop', width: 1440, height: 1000 },
  { name: 'mobile', width: 390, height: 844 },
];

const screenshotUrls = new Set([
  '/',
  '/ceny/',
  '/ohrana-ofisov/',
  '/fizicheskaya-ohrana/',
  '/ohrana-fizicheskih-lic/',
  '/ohrana-stroitelnyh-obektov/',
  '/ohrana-moskovskaya-oblast/',
  '/dogovor/',
  '/kontakty/',
  '/stati/',
  '/stati/pultovaya-ohrana-kak-rabotaet.html',
  '/stati/stoimost-bezopasnosti.html',
  '/kommercheskoe-predlozhenie/',
]);

function safeName(url) {
  if (url === '/') return 'home';
  return url.replace(/^\//, '').replace(/\/$/, '').replace(/[^a-zA-Z0-9._-]+/g, '-');
}

const browser = await chromium.launch({ headless: true });
const report = [];
const failures = [];

for (const vp of viewports) {
  const context = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    deviceScaleFactor: 1,
    reducedMotion: 'reduce',
  });

  for (const url of [...urls].sort()) {
    const page = await context.newPage();
    const pageErrors = [];
    const localHttpErrors = [];
    const consoleErrors = [];

    page.on('pageerror', err => pageErrors.push(String(err?.message || err)));
    page.on('console', msg => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });
    page.on('response', response => {
      const responseUrl = response.url();
      if (responseUrl.startsWith(BASE) && response.status() >= 400) {
        localHttpErrors.push(`${response.status()} ${responseUrl}`);
      }
    });

    let gotoError = null;
    try {
      await page.goto(BASE + url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(250);
    } catch (err) {
      gotoError = String(err?.message || err);
    }

    const metrics = gotoError ? null : await page.evaluate(() => {
      const doc = document.documentElement;
      const body = document.body;
      const scrollWidth = Math.max(doc.scrollWidth, body?.scrollWidth || 0);
      const clientWidth = doc.clientWidth;
      const h1s = [...document.querySelectorAll('h1')].filter(el => {
        const s = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
      });
      const main = document.querySelector('main');
      const brokenLocalImages = [...document.images]
        .filter(img => {
          try { return new URL(img.currentSrc || img.src, location.href).origin === location.origin; }
          catch { return false; }
        })
        .filter(img => img.complete && img.naturalWidth === 0)
        .map(img => img.getAttribute('src') || img.currentSrc || '(unknown)');
      const canvases = [...document.querySelectorAll('canvas')].map(c => ({
        id: c.id || null,
        width: c.width,
        height: c.height,
        clientWidth: c.clientWidth,
        clientHeight: c.clientHeight,
      }));
      return {
        title: document.title,
        scrollWidth,
        clientWidth,
        overflowPx: scrollWidth - clientWidth,
        h1Visible: h1s.length,
        mainHeight: main ? Math.round(main.getBoundingClientRect().height) : null,
        brokenLocalImages,
        canvases,
      };
    });

    let burgerOk = true;
    if (!gotoError && vp.name === 'mobile') {
      const burger = page.locator('.burger').first();
      if (await burger.count() && await burger.isVisible().catch(() => false)) {
        await burger.click().catch(() => { burgerOk = false; });
        await page.waitForTimeout(60);
        const opened = await burger.evaluate(el => el.classList.contains('open')).catch(() => false);
        if (!opened) burgerOk = false;
        if (opened) await burger.click().catch(() => {});
      }
    }

    const problems = [];
    if (gotoError) problems.push(`navigation: ${gotoError}`);
    if (metrics?.overflowPx > 6) problems.push(`horizontal overflow ${metrics.overflowPx}px`);
    if (metrics?.brokenLocalImages?.length) problems.push(`broken local images: ${metrics.brokenLocalImages.join(', ')}`);
    if (pageErrors.length) problems.push(`page errors: ${pageErrors.join(' | ')}`);
    if (localHttpErrors.length) problems.push(`local HTTP errors: ${localHttpErrors.join(' | ')}`);
    if (!burgerOk) problems.push('mobile burger did not open correctly');

    if (screenshotUrls.has(url) && !gotoError) {
      const file = path.join(OUT, `${vp.name}-${safeName(url)}.png`);
      await page.screenshot({ path: file, fullPage: true });
    }

    const entry = {
      viewport: vp.name,
      url,
      metrics,
      pageErrors,
      localHttpErrors,
      consoleErrors: consoleErrors.slice(0, 20),
      burgerOk,
      problems,
    };
    report.push(entry);
    if (problems.length) failures.push(entry);
    await page.close();
  }
  await context.close();
}

await browser.close();
fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify({ base: BASE, pages: urls.size, report, failures }, null, 2));
fs.writeFileSync(
  path.join(OUT, 'summary.txt'),
  `Visual QA pages: ${urls.size}\nViewports: ${viewports.length}\nChecks: ${report.length}\nFailures: ${failures.length}\n` +
    failures.map(f => `${f.viewport} ${f.url}: ${f.problems.join('; ')}`).join('\n') + '\n'
);

console.log(`Visual QA complete: ${urls.size} pages x ${viewports.length} viewports = ${report.length} checks`);
console.log(`Screenshots: ${[...screenshotUrls].length} representative pages x ${viewports.length}`);
if (failures.length) {
  console.error(`Visual QA failures: ${failures.length}`);
  for (const failure of failures) console.error(`${failure.viewport} ${failure.url}: ${failure.problems.join('; ')}`);
  process.exit(1);
}
console.log('Visual QA GREEN: no horizontal overflow, local 4xx/5xx, browser exceptions, broken local images, or mobile burger failures.');
