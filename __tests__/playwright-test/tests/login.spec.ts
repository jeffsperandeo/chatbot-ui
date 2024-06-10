import { test, expect, Page } from '@playwright/test';

test('start chatting is displayed', async ({ page }: { page: Page }) => {
  await page.goto('http://localhost:3000/');
  await expect(page.getByRole('link', { name: 'Start Chatting' })).toBeVisible();
});

test('No password error message', async ({ page }: { page: Page }) => {
  await page.goto('http://localhost:3000/login');
  await page.getByPlaceholder('you@example.com').fill('dummyemail@gmail.com');
  await page.getByRole('button', { name: 'Login' }).click();
  await page.waitForLoadState('networkidle');
  await expect(page.getByText('Invalid login credentials')).toBeVisible();
});

test('No password for signup', async ({ page }: { page: Page }) => {
  await page.goto('http://localhost:3000/login');
  await page.getByPlaceholder('you@example.com').fill('dummyEmail@Gmail.com');
  await page.getByRole('button', { name: 'Sign Up' }).click();
  await expect(page.getByText('Signup requires a valid')).toBeVisible();
});

test('invalid username for signup', async ({ page }: { page: Page }) => {
  await page.goto('http://localhost:3000/login');
  await page.getByPlaceholder('you@example.com').fill('dummyEmail');
  await page.getByPlaceholder('••••••••').fill('dummypassword');
  await page.getByRole('button', { name: 'Sign Up' }).click();
  await expect(page.getByText('Unable to validate email')).toBeVisible();
});

test('password reset message', async ({ page }: { page: Page }) => {
  await page.goto('http://localhost:3000/login');
  await page.getByPlaceholder('you@example.com').fill('demo@gmail.com');
  await page.getByRole('button', { name: 'Reset' }).click();
  await expect(page.getByText('Check email to reset password')).toBeVisible();
});
