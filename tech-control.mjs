import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const SKIP = new Set(['.git', 'node_modules', '.unlighthouse', 'playwright-report', 'test-results']);
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
  const clean = stripUrl(raw);
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

const feedFile = path.join(ROOT, 'yandex-services.yml');
if (fs.existsSync(feedFile)) {
  const xml = fs.readFileSync(feedFile, 'utf8');
  if (!/^\s*<\?xml\b/i.test(xml)) error(feedFile, 'нет XML-декларации');
  if (!/<services_feed\b[^>]*>[\s\S]*<\/services_feed>/i.test(xml)) error(feedFile, 'нет корневого services_feed');

  const source = xml.match(/<source>\s*([\s\S]*?)\s*<\/source>/i)?.[1] || '';
  if (!source) error(feedFile, 'нет обязательного блока source');
  else {
    for (const tag of ['name', 'url', 'favicon', 'locale']) {
      if (!tagValue(source, tag)) error(feedFile, `source/${tag} обязателен`);
    }
    if (tagValue(source, 'locale') && tagValue(source, 'locale') !== 'ru') {
      error(feedFile, `source/locale должен быть ru, сейчас: ${tagValue(source, 'locale')}`);
    }
    for (const tag of ['url', 'favicon']) {
      const raw = tagValue(source, tag);
      if (!raw) continue;
      const target = resolveSiteUrl(raw);
      if (target && !fs.existsSync(target)) warn(feedFile, `source/${tag} ведёт на отсутствующий локальный файл: ${raw}`);
    }
  }

  const executors = [...xml.matchAll(/<executor>\s*([\s\S]*?)\s*<\/executor>/gi)].map(m => m[1]);
  if (executors.length === 0) error(feedFile, 'нет ни одного executor');
  const executorIds = new Set();

  for (const [i, executor] of executors.entries()) {
    const n = i + 1;
    for (const tag of ['url', 'is_organization', 'name']) {
      if (!tagValue(executor, tag)) error(feedFile, `executor #${n}: отсутствует ${tag}`);
    }
    const executorId = tagValue(executor, 'persistent_id');
    if (executorId) {
      if (executorIds.has(executorId)) error(feedFile, `дублирующий persistent_id исполнителя: ${executorId}`);
      executorIds.add(executorId);
    }

    const servicesBlock = executor.match(/<services>\s*([\s\S]*?)\s*<\/services>/i)?.[1] || '';
    const services = [...servicesBlock.matchAll(/<service>\s*([\s\S]*?)\s*<\/service>/gi)].map(m => m[1]);
    if (services.length === 0) error(feedFile, `executor #${n}: нет ни одной service`);

    const serviceIds = new Set();
    const serviceNames = new Set();
    for (const [j, service] of services.entries()) {
      const sn = `${n}.${j + 1}`;
      const name = tagValue(service, 'name');
      if (!name) error(feedFile, `service #${sn}: отсутствует name`);
      else if (serviceNames.has(name)) error(feedFile, `executor #${n}: повтор названия услуги "${name}"`);
      else serviceNames.add(name);

      const id = tagValue(service, 'persistent_id');
      if (id) {
        if (serviceIds.has(id)) error(feedFile, `executor #${n}: повтор persistent_id услуги ${id}`);
        serviceIds.add(id);
      }

      const where = tagValue(service, 'where');
      if (where && !new Set(['at_customer', 'at_executor', 'online', 'both']).has(where)) {
        warn(feedFile, `service #${sn}: неизвестный where=${where}`);
      }

      const price = service.match(/<price>\s*([\s\S]*?)\s*<\/price>/i)?.[1] || '';
      if (price) {
        const priceTypes = ['is_negotiable', 'is_free', 'exact', 'from'].filter(tag => new RegExp(`<${tag}(?:\\s|>)`, 'i').test(price));
        if (priceTypes.length > 1) warn(feedFile, `service #${sn}: одновременно несколько типов цены: ${priceTypes.join(', ')}`);
      }

      const serviceUrl = tagValue(service, 'url');
      if (serviceUrl) {
        const target = resolveSiteUrl(serviceUrl);
        if (target && !fs.existsSync(target)) warn(feedFile, `service #${sn}: URL не имеет локальной страницы: ${serviceUrl}`);
        if (sitemapUrls.size && !sitemapUrls.has(serviceUrl)) warn(feedFile, `service #${sn}: URL отсутствует в sitemap: ${serviceUrl}`);
      }
    }
  }
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

const missingCore = ['index.html', 'stati/index.html', 'sitemap.xml', 'robots.txt', 'yandex-services.yml']
  .some(f => !fs.existsSync(path.join(ROOT, f)));
if (missingCore) process.exit(1);
