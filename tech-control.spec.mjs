import { test, expect } from '@playwright/test';

test('главная открывается и ключевые элементы на месте', async ({ page }) => {
  const response = await page.goto('/', { waitUntil: 'domcontentloaded' });
  expect(response?.ok()).toBeTruthy();
  await expect(page.locator('h1').first()).toBeVisible();
  await expect(page.locator('#siteNav')).toBeAttached();
  await expect(page.locator('#themeToggle')).toBeAttached();
});

test('Услуги: меню раскрывается и не исчезает при переходе курсора внутрь', async ({ page }) => {
  await page.goto('/', { waitUntil: 'networkidle' });
  const services = page.locator('.services-nav').first();
  const trigger = services.locator('.services-nav-link').first();
  const panel = services.locator('.services-panel').first();

  await expect(trigger).toBeVisible();
  await trigger.hover();
  await expect(panel).toBeVisible();

  await panel.hover();
  await page.waitForTimeout(850);
  await expect(panel).toBeVisible();
});

test('Статьи: раскрытие работает и обложка не мерцает', async ({ page }) => {
  const response = await page.goto('/stati/', { waitUntil: 'networkidle' });
  expect(response?.ok()).toBeTruthy();
  await page.waitForTimeout(600);

  const item = page.locator('.accordion-item').filter({ has: page.locator('.accordion-featured img') }).first();
  const header = item.locator('.accordion-header');
  const content = item.locator('.accordion-content');
  const image = item.locator('.accordion-featured img');

  await expect(header).toBeVisible();
  const before = await image.getAttribute('src');
  await header.click();
  await expect(content).toHaveClass(/active/);
  await expect(content).toBeVisible();

  const samples = [];
  for (let i = 0; i < 5; i++) {
    samples.push(await image.getAttribute('src'));
    await page.waitForTimeout(180);
  }
  expect(new Set(samples).size).toBe(1);
  expect(samples[0]).toBe(before);

  const imageMotion = await image.evaluate(el => {
    const s = getComputedStyle(el);
    return {
      animation: s.animationName,
      transitionDuration: s.transitionDuration,
      opacity: s.opacity,
      visibility: s.visibility
    };
  });
  expect(imageMotion.animation).toBe('none');
  expect(imageMotion.transitionDuration === '0s' || imageMotion.transitionDuration === '0s, 0s').toBeTruthy();
  expect(imageMotion.opacity).toBe('1');
  expect(imageMotion.visibility).toBe('visible');

  const contentMotion = await content.evaluate(el => {
    const s = getComputedStyle(el);
    return {
      transitionProperty: s.transitionProperty,
      opacity: s.opacity,
      animation: s.animationName
    };
  });
  expect(contentMotion.transitionProperty.split(',').map(v => v.trim())).not.toContain('opacity');
  expect(contentMotion.opacity).toBe('1');
  expect(contentMotion.animation).toBe('none');
});

test('переключатель темы реально меняет тему', async ({ page }) => {
  await page.goto('/', { waitUntil: 'networkidle' });
  const toggle = page.locator('#themeToggle');
  await expect(toggle).toBeVisible();
  const before = await page.locator('html').getAttribute('data-theme');
  await toggle.click();
  const after = await page.locator('html').getAttribute('data-theme');
  expect(after).not.toBe(before);
  expect(['light', 'dark']).toContain(after);
});

test('мобильная шапка: бургер открывает меню', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/', { waitUntil: 'networkidle' });
  const burger = page.locator('#burger');
  const nav = page.locator('#siteNav');
  await expect(burger).toBeVisible();
  await burger.click();
  await expect(nav).toHaveClass(/open/);
  await expect(nav).toBeVisible();
});
