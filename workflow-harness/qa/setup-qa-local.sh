#!/usr/bin/env bash
# setup-qa-local.sh — Install Playwright and set up QA environment
#
# Usage: bash qa/setup-qa-local.sh

set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ok()    { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
fail()  { printf "${RED}[FAIL]${NC}  %s\n" "$1"; exit 1; }
info()  { printf "${BLUE}[INFO]${NC}  %s\n" "$1"; }

EXIT_CODE=0

echo "═══════════════════════════════════════════════════════════"
echo "  QA ENVIRONMENT SETUP"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check Node.js
echo "── 1. Verifying Node.js ──────────────────────────────"
if command -v node &> /dev/null; then
  ok "Node.js $(node -v)"
else
  fail "Node.js is not installed. Install Node.js 18+ first."
fi

# Check npm
if command -v npm &> /dev/null; then
  ok "npm $(npm -v)"
else
  fail "npm is not installed."
fi

# Install Playwright
echo ""
echo "── 2. Installing Playwright ──────────────────────────"
if [ -f "package.json" ]; then
  if grep -q "playwright" package.json 2>/dev/null; then
    ok "Playwright already in package.json"
  else
    info "Installing playwright..."
    npm install --save-dev playwright
  fi
else
  info "No package.json found. Installing playwright globally..."
  npm install --save-dev playwright
fi

# Install browsers
echo ""
echo "── 3. Installing Playwright browsers ─────────────────"
npx playwright install chromium 2>&1 || {
  warn "Could not install Chromium. Try: npx playwright install chromium"
  EXIT_CODE=1
}

# Create QA reports directory
echo ""
echo "── 4. Creating QA reports directory ──────────────────"
mkdir -p qa/qa-reports/screenshots
ok "Directory qa/qa-reports/screenshots/ ready"

# Verify QA scripts
echo ""
echo "── 5. Verifying QA scripts ───────────────────────────"
for script in "qa/qa-runner.mjs" "qa/qa-register.mjs"; do
  if [ -f "$script" ]; then
    ok "Script exists: $script"
  else
    warn "Script not found: $script"
  fi
done

echo ""
echo "═══════════════════════════════════════════════════════════"
if [ $EXIT_CODE -eq 0 ]; then
  ok "QA environment ready. Run: node qa/qa-runner.mjs --url http://localhost:5000"
else
  warn "QA setup completed with warnings."
fi
echo "═══════════════════════════════════════════════════════════"

exit $EXIT_CODE
