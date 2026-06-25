# QA Automation — Workflow Harness

This directory contains browser-based QA automation for the project being developed with this harness.

## Structure

```
qa/
├── qa-runner.mjs           # Generic Playwright test runner
├── qa-register.mjs         # Registration flow test
├── setup-qa-local.sh       # Environment setup script
├── qa-reports/             # Generated reports and screenshots
│   └── screenshots/
└── README.md               # This file
```

## Prerequisites

- Node.js 18+
- npm

## Setup

```bash
bash qa/setup-qa-local.sh
```

This installs Playwright and Chromium, then creates the reports directory.

## Usage

```bash
# Run smoke test against a local server
node qa/qa-runner.mjs --url http://localhost:5000 --test smoke

# Run registration test
node qa/qa-runner.mjs --url https://example.com --test register

# Test on mobile viewport
node qa/qa-runner.mjs --url http://localhost:5000 --test smoke --viewport mobile

# Run post-deploy regression check
node qa/qa-runner.mjs --url https://staging.example.com --test regression

# Headed mode (watch the browser)
node qa/qa-runner.mjs --url http://localhost:5000 --headless false
```

## Available Tests

| Test        | Description |
|-------------|-------------|
| `smoke`     | Landing page load, health endpoint, console errors |
| `register`  | Full registration flow (sign up, form, submit) |
| `regression`| Quick post-deploy smoke test |

## Adding New Tests

1. Create a new function in `qa-runner.mjs` following the existing pattern
2. Register it in the `TEST_RUNNERS` object
3. Add acceptance criteria in `task-qa-browser.md`

## Configuration

The runner accepts these arguments:

| Arg           | Default                   | Description |
|---------------|---------------------------|-------------|
| `--url`       | `http://localhost:5000`    | Base URL of the app |
| `--test`      | `smoke`                   | Test to run |
| `--viewport`  | `desktop`                 | `desktop` or `mobile` |
| `--report-dir`| `qa/qa-reports/`          | Output directory |
| `--email`     | `qa-test@test.com`        | Test credentials |
| `--password`  | `QaTest1234`              | Test credentials |
| `--headless`  | `true`                    | Run headless or headed |
