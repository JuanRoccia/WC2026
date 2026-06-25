#!/usr/bin/env bash
# test_init.sh - Validate that init.sh works correctly

set -u

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok()    { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
fail()  { printf "${RED}[FAIL]${NC}  %s\n" "$1"; exit 1; }

echo "═══════════════════════════════════════════════════════"
echo "  TEST INIT.SH"
echo "═══════════════════════════════════════════════════════"
echo ""

# Test 1: init.sh exists and is executable
echo "Test 1: init.sh exists and is executable"
if [ ! -f "init.sh" ]; then
  fail "init.sh does not exist"
fi

if [ ! -x "init.sh" ]; then
  echo "  Warning: init.sh not executable, making it executable..."
  chmod +x init.sh
fi
ok "init.sh exists and is executable"

# Test 2: init.sh has no bash syntax errors
echo ""
echo "Test 2: Syntax check for init.sh"
if bash -n init.sh 2>/dev/null; then
  ok "init.sh syntax is valid"
else
  fail "init.sh has syntax errors"
fi

# Test 3: init.sh executes without fatal errors
echo ""
echo "Test 3: Execution of init.sh (non-interactive mode)"
output=$(WORKFLOW_TEST=1 bash init.sh 2>&1)
if echo "$output" | grep -q "\[FAIL\]"; then
  fail "init.sh reports errors"
fi
ok "init.sh executes without fatal errors"

# Test 4: Verify init.sh checks core files
echo ""
echo "Test 4: init.sh verifies core files"
if grep -q "AGENTS.md" init.sh && \
   grep -q "feature_list.json" init.sh && \
   grep -q "docs/architecture.md" init.sh && \
   grep -q "agents/" init.sh; then
  ok "init.sh verifies core files and directories"
else
  fail "init.sh does not verify all core files"
fi

# Test 5: Verify output functions in init.sh
echo ""
echo "Test 5: init.sh has output functions"
if grep -q "ok()" init.sh && \
   grep -q "warn()" init.sh && \
   grep -q "fail()" init.sh; then
  ok "init.sh has ok(), warn(), fail() functions"
else
  fail "init.sh missing expected output functions"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ALL INIT.SH TESTS PASSED"
echo "═══════════════════════════════════════════════════════"
