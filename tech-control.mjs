import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SKIP = new Set(['.git', 'node_modules', '.unlighthouse', 'playwright-report', 'test-results', 'visual-qa', '.openai']);
const IMAGE_EXT = new Set(['.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif']);
const WARN_IMAGE_BYTES = 400 * 1024;
const FORM_ENDPOINT = 'https://formspree.io/f/mvkpbvnb';
const SITE_ORIGIN = 'https://ohrana.tech';

function walk(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out;
}

const files = walk(ROOT);
const htmlFiles = files.filter(f => f.endsWith('.html'));
const jsFiles = files.filter(f => f.endsWith('.js') || f.endsWith('.mjs'));
const imageFiles = files.filter(f => IMAGE_EXT.has(path.extname(f).toLowerCase()));
const warnings = [];
const errors = [];
let leadForms = 0;
let correctLeadForms = 0;
let formspreeRefs = 0;

function rel(file) {
  return path.relative(ROOT, file).replaceAll(path.sep, '/');
}

function warn(file, msg) {
  warnings.push(`${rel(file)}: ${msg}`);
}

function error(file, msg) {
  errors.push(`${rel(file)}: ${msg}`);
}

function stripUrl(raw) {
  return raw.trim().split('#')[0].split('?')[0];
}

function isIgnoredUrl(u) {
  return !u || u.startsWith('#') || /^(https?:|mailto:|tel:|data:|javascript:|blob:|\/\/)/i.test(u);
}

function resolveLocal(fromFile, raw) {
  let clean = stripUrl(raw);
  if (/^https?:/i.test(clean)) {
    try { const url = new URL(clean); if (url.origin !== SITE_ORIGIN) return null; clean = url.pathname; }
    catch { return null; }
  }
  if (isIgnoredUrl(clean)) return null;
  let decoded = clean;
  try { decoded = decodeURIComponent(clean); } catch {}
  let candidate = decoded.startsWith('/')
    ? path.join(ROOT, decoded.replace(/^\/+/, ''))
    : path.resolve(path.dirname(fromFile), decoded);

  if (decoded.endsWith('/')) candidate = path.join(candidate, 'index.html');
  if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) candidate = path.join(candidate, 'index.html');
  return candidate;
}

function resolveSiteUrl(raw) {
  try {
    const u = new URL(raw);
    if (u.origin !== SITE_ORIGIN) return null;
    let pathname = u.pathname;
    try { pathname = decodeURIComponent(pathname); } catch {}

    if (pathname === '/') return path.join(ROOT, 'index.html');

    let candidate = path.join(ROOT, pathname.replace(/^\/+/, ''));
    if (pathname.endsWith('/')) candidate = path.join(candidate, 'index.html');
    if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) candidate = path.join(candidate, 'index.html');
    return candidate;
  } catch {
    return null;
  }
}

function attrValue(attrs, name) {
  const m = attrs.match(new RegExp(`\\b${name}\\s*=\\s*["']([^"']*)["']`, 'i'));
  return m ? m[1].trim() : '';
}

function tagValue(xml, tag) {
  const m = xml.match(new RegExp(`<${tag}(?:\\s[^>]*)?>\\s*([\\s\\S]*?)\\s*</${tag}>`, 'i'));
  return m ? m[1].trim() : '';
}

for (const file of htmlFiles) {
  const src = fs.readFileSync(file, 'utf8');

  for (const match of src.matchAll(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)) {
    try { JSON.parse(match[1]); } catch (err) { error(file, `некорректный JSON-LD: ${err.message}`); }
  }

  const ids = [...src.matchAll(/\bid\s*=\s*["']([^"']+)["']/gi)].map(m => m[1]);
  const seen = new Set();
  for (const id of ids) {
    if (seen.has(id)) error(file, `повторяющийся id="${id}"`);
    seen.add(id);
  }

  for (const m of src.matchAll(/<img\b([^>]*)>/gi)) {
    const attrs = m[1];
    if (!/\balt\s*=\s*["'][^"']*["']/i.test(attrs)) warn(file, 'у изображения нет alt');
  }

  for (const m of src.matchAll(/\b(?:src|href)\s*=\s*["']([^"']+)["']/gi)) {
    const raw = m[1];
    const target = resolveLocal(file, raw);
    if (!target) continue;
    if (!fs.existsSync(target)) {
      const clean = stripUrl(raw);
      const looksLikeAsset = /\.(?:html?|css|js|mjs|jpg|jpeg|png|webp|gif|avif|svg|ico|json|xml|pdf|mp4|webm|woff2?|ttf)$/i.test(clean);
      if (looksLikeAsset) error(file, `не найден локальный файл: ${raw}`);
      else warn(file, `маршрут не найден в репозитории: ${raw}`);
    }
  }

  for (const m of src.matchAll(/<form\b([^>]*)>([\s\S]*?)<\/form>/gi)) {
    const attrs = m[1];
    const body = m[2];
    const action = attrValue(attrs, 'action');
    const method = attrValue(attrs, 'method').toLowerCase();
    const looksLikeLead = method === 'post'
      || /formspree\.io/i.test(action)
      || /type\s*=\s*["']tel["']/i.test(body)
      || /name\s*=\s*["'](?:phone|tel|telephone)["']/i.test(body);

    if (!looksLikeLead) continue;
    leadForms++;
    if (action === FORM_ENDPOINT) {
      correctLeadForms++;
    } else {
      error(file, `форма заявки отправляет на "${action || '(action отсутствует)'}", нужно ${FORM_ENDPOINT}`);
    }
  }
}

for (const file of jsFiles) {
  const src = fs.readFileSync(file, 'utf8');
  for (const m of src.matchAll(/https:\/\/formspree\.io\/f\/[A-Za-z0-9_-]+/gi)) {
    formspreeRefs++;
    if (m[0] !== FORM_ENDPOINT) error(file, `старый/чужой Formspree endpoint: ${m[0]}`);
  }
}

const heavy = imageFiles
  .map(file => ({ file, size: fs.statSync(file).size }))
  .filter(x => x.size > WARN_IMAGE_BYTES)
  .sort((a, b) => b.size - a.size);

for (const { file, size } of heavy.slice(0, 40)) {
  warn(file, `картинка ${(size / 1024).toFixed(0)} КБ (ориентир сайта — до 400 КБ)`);
}
if (heavy.length > 40) warnings.push(`...и ещё ${heavy.length - 40} изображений тяжелее 400 КБ`);

for (const required of ['index.html', 'stati/index.html', 'sitemap.xml', 'robots.txt', 'yandex-services.yml']) {
  if (!fs.existsSync(path.join(ROOT, required))) errors.push(`${required}: обязательный файл отсутствует`);
}

const sitemapFile = path.join(ROOT, 'sitemap.xml');
const sitemapUrls = new Set();
if (fs.existsSync(sitemapFile)) {
  const xml = fs.readFileSync(sitemapFile, 'utf8');
  if (!/<urlset\b[^>]*>[\s\S]*<\/urlset>/i.test(xml)) error(sitemapFile, 'некорректный корневой элемент urlset');
  for (const m of xml.matchAll(/<loc>\s*([^<]+?)\s*<\/loc>/gi)) {
    const url = m[1].trim();
    if (sitemapUrls.has(url)) warn(sitemapFile, `дубликат URL: ${url}`);
    sitemapUrls.add(url);
    if (/[?#]/.test(url)) warn(sitemapFile, `URL содержит query/hash: ${url}`);
    const target = resolveSiteUrl(url);
    if (!target) {
      warn(sitemapFile, `внешний или некорректный URL: ${url}`);
    } else if (!fs.existsSync(target)) {
      warn(sitemapFile, `URL не имеет локальной страницы: ${url}`);
    }
  }
  if (sitemapUrls.size === 0) error(sitemapFile, 'не найдено ни одного <loc>');
}

// Yandex YML services/provider feed: shop, categories, sets and offers.
// Official format: https://yandex.ru/support/webmaster/ru/search-appearance/services
const feedFile = path.join(ROOT, 'yandex-services.yml');
if (fs.existsSync(feedFile)) {
  const xml = fs.readFileSync(feedFile, 'utf8');
  if (!/^\s*<\?xml\b/i.test(xml)) error(feedFile, 'нет XML-декларации');
  if (!/<yml_catalog\b[^>]*>[\s\S]*<\/yml_catalog>/i.test(xml)) error(feedFile, 'нет корневого yml_catalog');
  const shop = xml.match(/<shop>\s*([\s\S]*?)\s*<\/shop>/i)?.[1] || '';
  if (!shop) error(feedFile, 'нет обязательного shop');
  for (const tag of ['name', 'company', 'url']) if (!tagValue(shop, tag)) error(feedFile, `shop/${tag} обязателен`);
  const currencies = new Set([...shop.matchAll(/<currency\b([^>]*)\/?\s*>/gi)].map(m => attrValue(m[1], 'id')));
  const categories = new Set([...shop.matchAll(/<category\b([^>]*)>[\s\S]*?<\/category>/gi)].map(m => attrValue(m[1], 'id')));
  if (!currencies.size) error(feedFile, 'нет currencies/currency');
  if (!categories.size) error(feedFile, 'нет categories/category');
  const sets = new Set();
  function checkFeedUrl(raw, label) {
    const target = resolveSiteUrl(raw);
    if (!target || !fs.existsSync(target)) error(feedFile, `${label}: URL не имеет локальной страницы/файла: ${raw}`);
  }
  for (const match of shop.matchAll(/<set\b([^>]*)>([\s\S]*?)<\/set>/gi)) {
    const id = attrValue(match[1], 'id');
    if (!id || sets.has(id)) error(feedFile, `пустой или повторяющийся set id=${id}`);
    sets.add(id);
    if (!tagValue(match[2], 'name')) error(feedFile, `set ${id}: отсутствует name`);
    checkFeedUrl(tagValue(match[2], 'url'), `set ${id}`);
  }
  if (!sets.size) error(feedFile, 'нет sets/set');
  const offerIds = new Set();
  for (const match of shop.matchAll(/<offer\b([^>]*)>([\s\S]*?)<\/offer>/gi)) {
    const id = attrValue(match[1], 'id'), offer = match[2];
    if (!id || offerIds.has(id)) error(feedFile, `пустой или повторяющийся offer id=${id}`);
    offerIds.add(id);
    if (!tagValue(offer, 'name')) error(feedFile, `offer ${id}: отсутствует name`);
    const price = Number(tagValue(offer, 'price'));
    if (!Number.isFinite(price) || price <= 0) error(feedFile, `offer ${id}: некорректная price`);
    if (!currencies.has(tagValue(offer, 'currencyId'))) error(feedFile, `offer ${id}: неизвестная currencyId`);
    if (!categories.has(tagValue(offer, 'categoryId'))) error(feedFile, `offer ${id}: неизвестная categoryId`);
    const ids = tagValue(offer, 'set-ids').split(',').map(v => v.trim());
    for (const setId of ids) if (!sets.has(setId)) error(feedFile, `offer ${id}: неизвестный set-ids=${setId}`);
    checkFeedUrl(tagValue(offer, 'url'), `offer ${id}`);
    for (const picture of offer.matchAll(/<picture>\s*([^<]+)\s*<\/picture>/gi)) checkFeedUrl(picture[1].trim(), `offer ${id}/picture`);
  }
  if (!offerIds.size) error(feedFile, 'нет offers/offer');
}

for (const name of ['manifest.json', 'site.webmanifest']) {
  const file = path.join(ROOT, name);
  try {
    const manifest = JSON.parse(fs.readFileSync(file, 'utf8'));
    for (const icon of manifest.icons || []) {
      const target = resolveLocal(file, icon.src);
      if (!target || !fs.existsSync(target)) error(file, `не найден значок: ${icon.src}`);
    }
  } catch (err) { error(file, `некорректный UTF-8 JSON: ${err.message}`); }
}

console.log(`\n=== ТЕХКОНТРОЛЬ ohrana.tech ===`);
console.log(`HTML-файлов: ${htmlFiles.length}`);
console.log(`Изображений: ${imageFiles.length}`);
console.log(`Форм заявок: ${leadForms}`);
console.log(`Форм на правильном Formspree: ${correctLeadForms}/${leadForms}`);
console.log(`Formspree-ссылок в JS: ${formspreeRefs}`);
console.log(`URL в sitemap: ${sitemapUrls.size}`);
console.log(`Предупреждений: ${warnings.length}`);
console.log(`Критических замечаний: ${errors.length}\n`);

for (const msg of warnings) console.log(`::warning::${msg}`);
for (const msg of errors) console.log(`::error::${msg}`);

if (errors.length) process.exitCode = 1;
