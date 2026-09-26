import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const SKIP = new Set(['.git', 'node_modules', '.unlighthouse', 'playwright-report', 'test-results']);
const IMAGE_EXT = new Set(['.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif']);
const WARN_IMAGE_BYTES = 400 * 1024;
const FORM_ENDPOINT = 'https://formspree.io/f/mvkpbvnb';

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

function attrValue(attrs, name) {
  const m = attrs.match(new RegExp(`\\b${name}\\s*=\\s*["']([^"']*)["']`, 'i'));
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
      // Не считаем серверные/виртуальные маршруты критической ошибкой, если это href без расширения.
      const clean = stripUrl(raw);
      const looksLikeAsset = /\.(?:html?|css|js|mjs|jpg|jpeg|png|webp|gif|avif|svg|ico|json|xml|pdf|mp4|webm|woff2?|ttf)$/i.test(clean);
      if (looksLikeAsset) error(file, `не найден локальный файл: ${raw}`);
      else warn(file, `маршрут не найден в репозитории: ${raw}`);
    }
  }

  // Проверка всех лид-форм. Формой заявки считаем POST/Formspree-форму
  // либо форму с телефонным полем. Она обязана отправлять на единый endpoint.
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

// Отдельно ловим старые Formspree-ID в JavaScript, даже если код пока не используется.
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

for (const required of ['index.html', 'stati/index.html', 'sitemap.xml', 'robots.txt']) {
  if (!fs.existsSync(path.join(ROOT, required))) errors.push(`${required}: обязательный файл отсутствует`);
}

console.log(`\n=== ТЕХКОНТРОЛЬ ohrana.tech ===`);
console.log(`HTML-файлов: ${htmlFiles.length}`);
console.log(`Изображений: ${imageFiles.length}`);
console.log(`Форм заявок: ${leadForms}`);
console.log(`Форм на правильном Formspree: ${correctLeadForms}/${leadForms}`);
console.log(`Formspree-ссылок в JS: ${formspreeRefs}`);
console.log(`Предупреждений: ${warnings.length}`);
console.log(`Критических замечаний: ${errors.length}\n`);

for (const msg of warnings) console.log(`::warning::${msg}`);
for (const msg of errors) console.log(`::error::${msg}`);

// На первом этапе аудит информирует, а не блокирует публикацию из-за старого техдолга.
// Блокируем только если потеряны базовые файлы сайта.
const missingCore = ['index.html', 'stati/index.html', 'sitemap.xml', 'robots.txt']
  .some(f => !fs.existsSync(path.join(ROOT, f)));
if (missingCore) process.exit(1);
