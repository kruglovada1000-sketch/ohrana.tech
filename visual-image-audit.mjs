import { chromium } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const BASE = process.env.VISUAL_QA_BASE || 'http://127.0.0.1:4173';
const OUT = path.join(ROOT, 'visual-qa');
const SHOTS = path.join(OUT, 'cropped-images');
const SKIP_DIRS = new Set(['.git', 'node_modules', 'visual-qa', 'playwright-report', 'test-results']);
const MAX_SHOTS = 50;
const CROP_WARN = 0.12;

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(SHOTS, { recursive: true });

function walk(dir, acc = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory() && SKIP_DIRS.has(entry.name)) continue;
    const abs = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(abs, acc);
    else if (entry.isFile() && entry.name.toLowerCase().endsWith('.html')) acc.push(abs);
  }
  return acc;
}

function fileToUrl(file) {
  const rel = path.relative(ROOT, file).split(path.sep).join('/');
  if (rel === 'index.html') return '/';
  if (rel.endsWith('/index.html')) return '/' + rel.slice(0, -'index.html'.length);
  return '/' + rel;
}

function safeName(value) {
  return value.replace(/^\/+/, '').replace(/[^a-zA-Z0-9а-яА-ЯёЁ._-]+/g, '_').slice(0, 120) || 'home';
}

const files = walk(ROOT).sort();
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });

// Для геометрии локального сайта нам не нужны метрика, шрифты и прочие внешние запросы.
await context.route('**/*', async route => {
  try {
    const u = new URL(route.request().url());
    if (u.hostname === '127.0.0.1' || u.hostname === 'localhost') return route.continue();
    return route.abort();
  } catch {
    return route.continue();
  }
});

const findings = [];
const pageErrors = [];
let shotCount = 0;

for (const file of files) {
  const route = fileToUrl(file);
  const page = await context.newPage();
  try {
    const response = await page.goto(BASE + route, { waitUntil: 'domcontentloaded', timeout: 15000 });
    if (!response || !response.ok()) {
      pageErrors.push({ route, error: `HTTP ${response ? response.status() : 'no response'}` });
      await page.close();
      continue;
    }
    await page.waitForTimeout(180);

    const images = await page.locator('img').evaluateAll(nodes => nodes.map((img, index) => {
      const s = getComputedStyle(img);
      const r = img.getBoundingClientRect();
      const nw = img.naturalWidth || 0;
      const nh = img.naturalHeight || 0;
      const renderedW = r.width || 0;
      const renderedH = r.height || 0;
      const naturalAspect = nw && nh ? nw / nh : 0;
      const frameAspect = renderedW && renderedH ? renderedW / renderedH : 0;
      let crop = 0;
      if (s.objectFit === 'cover' && naturalAspect && frameAspect) {
        crop = naturalAspect > frameAspect
          ? 1 - (frameAspect / naturalAspect)
          : 1 - (naturalAspect / frameAspect);
      }
      const parent = img.parentElement ? getComputedStyle(img.parentElement) : null;
      return {
        index,
        src: img.currentSrc || img.getAttribute('src') || '',
        alt: img.getAttribute('alt') || '',
        id: img.id || '',
        className: typeof img.className === 'string' ? img.className : '',
        objectFit: s.objectFit,
        objectPosition: s.objectPosition,
        naturalWidth: nw,
        naturalHeight: nh,
        renderedWidth: Math.round(renderedW),
        renderedHeight: Math.round(renderedH),
        crop,
        parentClass: img.parentElement && typeof img.parentElement.className === 'string' ? img.parentElement.className : '',
        parentOverflow: parent ? `${parent.overflowX}/${parent.overflowY}` : '',
        visible: renderedW > 24 && renderedH > 24 && s.display !== 'none' && s.visibility !== 'hidden'
      };
    }));

    for (const img of images) {
      if (!img.visible || img.naturalWidth < 2 || img.naturalHeight < 2) continue;
      if (img.objectFit !== 'cover' || img.crop < CROP_WARN) continue;

      const finding = { route, file: path.relative(ROOT, file).split(path.sep).join('/'), ...img };
      findings.push(finding);

      if (shotCount < MAX_SHOTS) {
        const locator = page.locator('img').nth(img.index);
        if (await locator.isVisible().catch(() => false)) {
          const name = `${String(shotCount + 1).padStart(2, '0')}-${safeName(route)}-img${img.index}.png`;
          try {
            await locator.screenshot({ path: path.join(SHOTS, name), animations: 'disabled' });
            finding.screenshot = `cropped-images/${name}`;
            shotCount++;
          } catch {}
        }
      }
    }
  } catch (error) {
    pageErrors.push({ route, error: String(error && error.message ? error.message : error) });
  } finally {
    await page.close();
  }
}

await browser.close();

findings.sort((a, b) => b.crop - a.crop);
const json = { generatedAt: new Date().toISOString(), pagesScanned: files.length, threshold: CROP_WARN, findings, pageErrors };
fs.writeFileSync(path.join(OUT, 'image-crop-report.json'), JSON.stringify(json, null, 2));

const md = [];
md.push('# Visual image crop audit');
md.push('');
md.push(`Проверено HTML-страниц: **${files.length}**.`);
md.push(`Подозрительно обрезанных изображений (object-fit: cover, потеря > ${Math.round(CROP_WARN * 100)}%): **${findings.length}**.`);
md.push('');
md.push('Это диагностический отчёт: он ничего автоматически не ломает и не меняет на сайте.');
md.push('');

if (!findings.length) {
  md.push('✅ Подозрительных обрезок не найдено.');
} else {
  md.push('| Обрезка | Страница | Картинка | Блок | Натуральный → показанный размер | Скрин |');
  md.push('|---:|---|---|---|---|---|');
  for (const f of findings) {
    const block = [f.id ? `#${f.id}` : '', f.className ? `.${f.className.trim().replace(/\s+/g, '.')}` : '', f.parentClass ? `parent:${String(f.parentClass).trim().replace(/\s+/g, '.')}` : ''].filter(Boolean).join(' ');
    md.push(`| ${Math.round(f.crop * 100)}% | \`${f.route}\` | \`${String(f.src).replace(/\|/g, '%7C')}\` | \`${block || 'img'}\` | ${f.naturalWidth}×${f.naturalHeight} → ${f.renderedWidth}×${f.renderedHeight} | ${f.screenshot ? `[png](${f.screenshot})` : '—'} |`);
  }
}

if (pageErrors.length) {
  md.push('');
  md.push('## Страницы, которые не удалось проверить');
  for (const e of pageErrors) md.push(`- \`${e.route}\` — ${e.error}`);
}

fs.writeFileSync(path.join(OUT, 'image-crop-report.md'), md.join('\n') + '\n');
console.log(`Visual QA: ${files.length} pages, ${findings.length} suspicious cropped images, ${pageErrors.length} page errors.`);
