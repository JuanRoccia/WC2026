# Skill: QA Automation

## Description
Browser-based end-to-end testing using Playwright. Covers UI flows, console error detection, mobile responsiveness, and post-deploy regression.

## When to Use
- After backend/frontend changes that affect user-facing flows
- Before marking a feature as `done` in `feature_list.json`
- Post-deploy to verify nothing is broken
- When testing mobile responsiveness

## Playwright Basics

### Installation
```bash
bash qa/setup-qa-local.sh
```

### Running Tests
```bash
node qa/qa-runner.mjs --url http://localhost:5000 --test smoke
```

## Test Patterns

### 1. Page Object Pattern
Group selectors and interactions by page:
```js
const LandingPage = {
  registerBtn: () => page.locator('a, button', { hasText: /registr|empezar/i }),
  searchBar: () => page.locator('input[type="search"]'),
};
```

### 2. Console Monitoring
Always capture console errors during test execution:
```js
const errors = [];
page.on("console", (msg) => {
  if (msg.type() === "error") errors.push(msg.text());
});
```

### 3. Screenshot on Failure
Capture visual evidence whenever a check fails:
```js
if (!condition) {
  await page.screenshot({ path: `qa-reports/screenshots/fail-${Date.now()}.png` });
}
```

### 4. Viewport Testing
Test critical flows in both desktop (1280x800) and mobile (375x812):
```bash
node qa/qa-runner.mjs --viewport mobile --test smoke
```

## Best Practices

1. **Use data-testid attributes** where possible for stable selectors
2. **Avoid hard waits** — prefer `waitForSelector`, `waitForResponse`, `waitForURL`
3. **Isolate tests** — each test should work independently
4. **Use unique emails** — append `Date.now()` to avoid duplicate registration errors
5. **Check console errors** — often reveal JS bugs not visible in the UI

## Related

- `qa/qa-runner.mjs` — test runner implementation
- `qa/qa-register.mjs` — registration flow test
- `tasks/task-qa-browser.md` — specific QA tasks
- `agents/07-qa-browser.md` — QA Browser agent definition
