#!/usr/bin/env node
/**
 * qa-register.mjs — Generic Registration Flow Test
 *
 * Tests the user registration flow end-to-end.
 * Configure via environment variables or CLI args.
 *
 * Usage:
 *   node qa/qa-register.mjs --url https://example.com
 *   APP_URL=http://localhost:5000 node qa/qa-register.mjs
 */

import { chromium } from "playwright";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const CONFIG = {
  url: process.env.APP_URL || process.argv.find((a) => a.startsWith("--url="))?.split("=")[1] || "http://localhost:5000",
  email: process.env.TEST_EMAIL || `qa-${Date.now()}@test.com`,
  password: process.env.TEST_PASSWORD || "QaTest1234",
  headless: process.env.HEADLESS !== "false",
  reportDir: path.join(__dirname, "qa-reports"),
};

const RESULTS = { passed: 0, failed: 0, errors: [] };
let screenshots = 0;

async function screenshot(page, label) {
  screenshots++;
  const dir = path.join(CONFIG.reportDir, "screenshots");
  fs.mkdirSync(dir, { recursive: true });
  const filepath = path.join(dir, `register-${String(screenshots).padStart(2, "0")}-${label}.png`);
  await page.screenshot({ path: filepath });
  return filepath;
}

async function main() {
  console.log("═══ QA Registration Test ═══");
  console.log(`URL:  ${CONFIG.url}`);
  console.log(`Email: ${CONFIG.email}`);
  console.log("");

  const browser = await chromium.launch({ headless: CONFIG.headless });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

  const checks = [];

  try {
    // Step 1: Load landing page
    await page.goto(CONFIG.url, { waitUntil: "networkidle", timeout: 30000 });
    await screenshot(page, "landing");
    checks.push({ label: "Landing page loads", pass: true });

    // Step 2: Find register button/link
    const registerBtn = page.locator('a, button', {
      hasText: /registr|crear cuenta|probá gratis|sign.?up|register|empezar/i,
    }).first();
    const btnVisible = await registerBtn.isVisible().catch(() => false);
    checks.push({ label: "Register CTA is visible", pass: btnVisible });

    if (btnVisible) {
      await registerBtn.click();
      await page.waitForTimeout(1500);
      await screenshot(page, "register-form");
    }

    // Step 3: Fill form
    const emailInput = page.locator('input[type="email"], input[name="email"]').first();
    const emailVisible = await emailInput.isVisible().catch(() => false);
    checks.push({ label: "Email field is visible", pass: emailVisible });

    if (emailVisible) {
      await emailInput.fill(CONFIG.email);
      const passInput = page.locator('input[type="password"]').first();
      await passInput.fill(CONFIG.password);

      const confirmInput = page.locator('input[type="password"]').nth(1);
      if (await confirmInput.isVisible().catch(() => false)) {
        await confirmInput.fill(CONFIG.password);
      }

      await screenshot(page, "form-filled");

      // Step 4: Submit
      const submitBtn = page.locator('button[type="submit"], button:has-text("continuar"), button:has-text("registrarme"), button:has-text("crear cuenta")').first();
      await submitBtn.click();
      await page.waitForTimeout(3000);
      await screenshot(page, "post-registration");

      // Step 5: Check success
      const currentUrl = page.url();
      const hasError = await page.locator('text=error', { exact: false }).isVisible().catch(() => false);
      const redirected = !currentUrl.includes(CONFIG.url.replace(/https?:\/\//, "").split("/")[0]);
      checks.push({
        label: "Registration completed",
        pass: !hasError || redirected,
      });
    }
  } catch (err) {
    checks.push({ label: "Test execution", pass: false });
    RESULTS.errors.push(err.message);
  }

  // Report
  for (const c of checks) {
    if (c.pass) {
      RESULTS.passed++;
      console.log(`  [PASS] ${c.label}`);
    } else {
      RESULTS.failed++;
      console.log(`  [FAIL] ${c.label}`);
    }
  }

  await browser.close();

  const score = RESULTS.passed + RESULTS.failed > 0
    ? Math.round((RESULTS.passed / (RESULTS.passed + RESULTS.failed)) * 100)
    : 0;

  console.log(`\nRESULTS: ${RESULTS.passed} passed, ${RESULTS.failed} failed`);
  console.log(`SCORE: ${score}/100`);
  process.exit(RESULTS.failed > 0 ? 1 : 0);
}

main();
