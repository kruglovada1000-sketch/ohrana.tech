import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

// Public services remain mocked during tests, including all form submissions.
test.beforeEach(async ({ page }) => {
  await page.route('**/*', route => {
    const host = new URL(route.request().url()).hostname;
    return host === '127.0.0.1' || host === 'localhost' ? route.continue() : route.abort();
  });
});

const urls = [...fs.readFileSync('sitemap.xml', 'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)]
  .map(match => new URL(match[1]).pathname);

for (const url of urls) {
  test(`страница ${url}: обе темы, мобильная ширина, изображения и JavaScript`, async ({ page }, testInfo) => {
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const response = await page.goto(url, { waitUntil: 'load' });
    expect(response?.ok()).toBeTruthy();
    await expect(page.locator('h1')).toHaveCount(1);
    await page.locator('img').evaluateAll(images => images.forEach(image => image.loading = 'eager'));
    await page.waitForLoadState('networkidle');
    const broken = await page.locator('img').evaluateAll(images => images
      .filter(image => !image.complete || !image.naturalWidth)
      .map(image => image.getAttribute('src')));
    expect(broken).toEqual([]);

    for (const width of [1440, 390]) {
      await page.setViewportSize({ width, height: 1000 });
      for (let i = 0; i < 2; i++) {
        const theme = await page.locator('html').getAttribute('data-theme');
        await expect(page.locator('#themeToggle')).toBeVisible();
        await page.locator('#themeToggle').click();
        const changed = await page.locator('html').getAttribute('data-theme');
        expect(changed).not.toBe(theme);
        expect(['light', 'dark']).toContain(changed);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
        expect(overflow, `${url}, ширина ${width}, тема ${changed}`).toBeLessThanOrEqual(2);
      }
      if (['/', '/kontakty/', '/ceny/', '/ohrana-moskovskaya-oblast/', '/uslugi/ohrana-lombardov/'].includes(url)) {
        await testInfo.attach(`page-${width}`, { body: await page.screenshot(), contentType: 'image/png' });
      }
    }
    expect(errors).toEqual([]);
  });
}

test('раздел 01 сохраняет согласованную квадратную картинку', async ({ page }) => {
  await page.goto('/');
  const image = page.locator('#about .about-visual img');
  await expect(image).toHaveAttribute('src', '/images/chop-company.png');
  await page.waitForLoadState('networkidle');
  await expect(image).toHaveAttribute('src', '/images/chop-company.png');
});

test('Услуги закрываются Escape при фокусе внутри раскрытого меню', async ({ page }) => {
  await page.goto('/');
  const trigger = page.locator('.services-nav-link');
  const toggle = page.locator('.services-nav-toggle');
  const panel = page.locator('.services-panel');
  await trigger.focus();
  await trigger.press('ArrowDown');
  await expect(panel).toBeVisible();
  await panel.locator('a').first().press('Escape');
  await expect(panel).toBeHidden();
  await expect(toggle).toBeFocused();
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');
});

for (const url of ['/', '/kontakty/', '/ohrana-moskovskaya-oblast/', '/uslugi/ohrana-lombardov/']) {
  test(`мобильное меню ${url}: Escape и клик вне меню`, async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(url);
    const burger = page.locator('#burger'), nav = page.locator('#siteNav');
    await burger.click();
    await expect(nav).toHaveClass(/open/);
    await page.keyboard.press('Escape');
    await expect(nav).not.toHaveClass(/open/);
    await expect(burger).toBeFocused();
    await burger.click();
    await page.locator('.hd-in').click({ position: { x: 5, y: 5 } });
    await expect(nav).not.toHaveClass(/open/);
  });
}

for (const url of ['/', '/kontakty/', '/ohrana-moskovskaya-oblast/']) {
  test(`FAQ ${url}: открытый ответ сохраняется после изменения ширины`, async ({ page }) => {
    await page.goto(url);
    const question = page.locator('.faq-q').nth(1);
    const answer = question.locator('..').locator('.faq-a');
    await question.click();
    await expect(question).toHaveAttribute('aria-expanded', 'true');
    await expect(answer).toHaveAttribute('aria-hidden', 'false');
    await page.setViewportSize({ width: 390, height: 844 });
    await expect.poll(() => answer.evaluate(el => parseFloat(el.style.maxHeight) >= el.scrollHeight)).toBe(true);
    await question.click();
    await expect(question).toHaveAttribute('aria-expanded', 'false');
    await expect(answer).toHaveAttribute('aria-hidden', 'true');
  });
}

async function fillLeadForm(page, url) {
  await page.goto(url);
  const form = page.locator('form[action*="formspree.io"]').first();
  await form.locator('[name="name"]').fill('Тест проверки сайта');
  await form.locator('[name="phone"]').fill('+7 (900) 000-00-00');
  for (const checkbox of await form.locator('input[type="checkbox"][required]').all()) await checkbox.check();
  for (const select of await form.locator('select[required]').all()) {
    const value = await select.locator('option').evaluateAll(options => options.find(option => option.value && !option.disabled)?.value);
    if (value) await select.selectOption(value);
  }
  return form;
}

for (const url of ['/', '/kontakty/', '/ohrana-moskovskaya-oblast/', '/uslugi/ohrana-lombardov/']) {
  test(`форма ${url}: ошибка не уводит со страницы, данные сохраняются, повтор успешен`, async ({ page }) => {
    let requests = 0;
    await page.route('https://formspree.io/f/mvkpbvnb', async route => {
      requests++;
      await route.fulfill({ status: requests === 1 ? 503 : 200, contentType: 'application/json', body: requests === 1 ? '{"error":"unavailable"}' : '{"ok":true}', headers: { 'access-control-allow-origin': '*' } });
    });
    const form = await fillLeadForm(page, url);
    const button = form.locator('[type="submit"]');
    await button.click();
    await expect(form.locator('[data-form-error]')).toBeVisible();
    await expect(form.locator('[name="name"]')).toHaveValue('Тест проверки сайта');
    await expect(form.locator('[name="phone"]')).toHaveValue('+7 (900) 000-00-00');
    await expect(button).toBeEnabled();
    expect(new URL(page.url()).pathname).toBe(url);
    expect(requests).toBe(1);
    await button.click();
    await expect(page.locator('.form-ok,.form-success,[data-form-success]').filter({ visible: true }).first()).toBeVisible();
    expect(requests).toBe(2);
  });

  test(`форма ${url}: при обрыве сети не отправляет заявку второй раз`, async ({ page }) => {
    let requests = 0;
    await page.route('https://formspree.io/f/mvkpbvnb', route => { requests++; return route.abort(); });
    const form = await fillLeadForm(page, url);
    await form.locator('[type="submit"]').click();
    await expect(form.locator('[data-form-error]')).toBeVisible();
    await expect(form.locator('[type="submit"]')).toBeEnabled();
    expect(requests).toBe(1);
    expect(new URL(page.url()).pathname).toBe(url);
  });
}

test('светлая тема сохраняется при переходах между страницами', async ({ page }) => {
  await page.goto('/');
  if (await page.locator('html').getAttribute('data-theme') !== 'light') await page.locator('#themeToggle').click();
  for (const url of ['/kontakty/', '/ohrana-moskovskaya-oblast/', '/uslugi/ohrana-lombardov/', '/']) {
    await page.goto(url);
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
    await expect(page.locator('#themeToggle')).toHaveAttribute('aria-pressed', 'true');
  }
});

test('переходы к заявке и аргументам сопровождения попадают в существующие блоки', async ({ page }) => {
  await page.goto('/ohrana-tehniki/');
  await page.locator('a[href="#order"]').first().click();
  await expect(page.locator('#order')).toBeInViewport();
  await page.goto('/stati/soprovozhdenie-gruzov.html');
  await page.locator('a[href="#why"]').click();
  await expect(page.locator('#why')).toBeInViewport();
});

test('манифесты читаются в UTF-8 и все иконки доступны', async ({ request }) => {
  for (const file of ['/manifest.json', '/site.webmanifest']) {
    const response = await request.get(file);
    expect(response.ok()).toBeTruthy();
    const manifest = await response.json();
    expect(manifest.name).toContain('Рускорпорация');
    for (const icon of manifest.icons) expect((await request.get(icon.src)).ok()).toBeTruthy();
  }
});


test('узкая шапка статьи: телефон и переключатель темы остаются доступными', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 844 });
  await page.goto('/stati/srok-zapuska-ohrany-novogo-obekta.html');
  for (const selector of ['.hd-right > .hd-phone', '#themeToggle']) {
    const rect = await page.locator(selector).boundingBox();
    expect(rect).not.toBeNull();
    expect(rect.x).toBeGreaterThanOrEqual(0);
    expect(rect.x + rect.width).toBeLessThanOrEqual(320);
  }
  const before = await page.locator('html').getAttribute('data-theme');
  await page.locator('#themeToggle').click();
  expect(await page.locator('html').getAttribute('data-theme')).not.toBe(before);
});
