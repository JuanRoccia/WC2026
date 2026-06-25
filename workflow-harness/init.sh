#!/usr/bin/env bash
# init.sh — Verificación e inicialización del workflow harness
#
# Este script verifica la integridad del harness y recopila información
# del proyecto antes de iniciar el workflow.
#
# Uso: bash init.sh

set -u
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ok()    { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
fail()  { printf "${RED}[FAIL]${NC}  %s\n" "$1"; }
info()  { printf "${BLUE}[INFO]${NC}  %s\n" "$1"; }

EXIT_CODE=0
PY_TESTS=0
BASH_TESTS=0

echo "═══════════════════════════════════════════════════════════"
echo "  WORKFLOW HARNESS - Inicialización del Entorno"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "── 1. Verificando estructura del harness ──────────────"

# Directorios base requeridos
for dir in agents tasks skills tests qa prompts audits user; do
  if [ ! -d "$dir" ]; then
    fail "Falta directorio: $dir/"
    EXIT_CODE=1
  else
    ok "Directorio existe: $dir/"
  fi
done

echo ""
echo "── 2. Verificando archivos base del workflow ──────────"

# Archivos core del workflow
for f in "AGENTS.md" "feature_list.json" "07-BUGS-REPORT.md" "TESTING-MANUAL.md"; do
  if [ ! -f "$f" ]; then
    warn "Falta archivo base: $f"
  else
    ok "Existe $f"
  fi
done

echo ""
echo "── 3. Verificando documentación (docs/) ──────────────"

for f in "docs/architecture.md" "docs/conventions.md" "docs/verification.md"; do
  if [ ! -f "$f" ]; then
    warn "Falta documento: $f"
  else
    ok "Existe $f"
  fi
done

echo ""
echo "── 4. Verificando agentes definidos ───────────────────"

AGENTS=("01-arquitecto.md" "02-code-reviewer.md" "03-tester-debugger.md" "04-frontend-ui.md" "05-backend.md" "06-ghost.md" "07-qa-browser.md")
for agent in "${AGENTS[@]}"; do
  if [ ! -f "agents/$agent" ]; then
    warn "Falta definición de agente: $agent"
  else
    ok "Agente definido: $agent"
  fi
done

echo ""
echo "── 5. Verificando tareas por agente ───────────────────"

for task in "task-arquitecto.md" "task-code-reviewer.md" "task-tester.md" "task-frontend.md" "task-backend.md" "task-ghost.md" "task-qa-browser.md"; do
  if [ ! -f "tasks/$task" ]; then
    warn "Falta tarea: tasks/$task"
  else
    ok "Tarea existe: $task"
  fi
done

echo ""
echo "── 6. Verificando QA Automation ─────────────────────"

for f in "qa/qa-runner.mjs" "qa/qa-register.mjs" "qa/setup-qa-local.sh" "qa/README.md"; do
  if [ ! -f "$f" ]; then
    warn "Falta archivo QA: $f"
  else
    ok "Existe $f"
  fi
done

echo ""
echo "── 7. Verificando skills disponibles ──────────────────"

SKILL_COUNT=$(find skills/ -type f 2>/dev/null | wc -l)
if [ "$SKILL_COUNT" -eq 0 ]; then
  warn "No hay skills definidos en skills/"
else
  ok "Skills disponibles: $SKILL_COUNT archivo(s)"
fi

echo ""
echo "── 8. Ejecutando tests del harness ──────────────────"

# Skip tests if running in test mode to prevent infinite loops
if [ "${WORKFLOW_TEST:-0}" -eq 1 ]; then
  info "Modo test detectado, omitiendo ejecución de tests"
else
  if [ -d "tests" ]; then
    # Tests de Python (verificar que python3 sea ejecutable real)
    if python3 -c "import sys; sys.exit(0)" >/dev/null 2>&1; then
      PY_TESTS=$(find tests/ -name "test_*.py" 2>/dev/null | wc -l)
      if [ "$PY_TESTS" -gt 0 ]; then
        if python3 -m unittest discover -s tests -v 2>&1; then
          ok "Todos los tests de Python pasan"
        else
          fail "Hay tests de Python rotos"
          EXIT_CODE=1
        fi
      fi
    else
      warn "Python no disponible, omitiendo tests de Python"
    fi
    
    # Tests de Bash
    BASH_TESTS=$(find tests/ -name "test_*.sh" 2>/dev/null | wc -l)
    if [ "$BASH_TESTS" -gt 0 ]; then
      echo "Encontrados $BASH_TESTS tests de Bash"
      for test in tests/test_*.sh; do
        if [ -x "$test" ]; then
          if bash "$test" 2>&1; then
            ok "Test $test pasó"
          else
            fail "Test $test falló"
            EXIT_CODE=1
          fi
        fi
      done
    fi
    
    if [ "$PY_TESTS" -eq 0 ] && [ "$BASH_TESTS" -eq 0 ]; then
      warn "No hay tests en tests/"
    fi
  else
    warn "Carpeta tests/ no existe todavía"
  fi
fi

echo ""
echo "── 9. Generando configuración inicial ─────────────────"

# Verificar si estamos en modo interactivo
if [ -t 0 ]; then
  # Preguntar al usuario sobre el proyecto
  info "Para configurar el workflow, necesito información sobre el proyecto:"
  echo ""
  
  read -p "¿Cuál es el nombre del proyecto? (ej: MiApp): " PROJECT_NAME
  read -p "¿Qué tipo de proyecto es? (ej: e-commerce, saas, landing): " PROJECT_TYPE
  read -p "¿Se subirá a GitHub? (y/n): " GITHUB_CHOICE
  
  if [[ "$GITHUB_CHOICE" =~ ^[Yy]$ ]]; then
    info "Se configurará .gitignore para excluir /workflow y archivos sensibles"
    GITHUB_REPO=true
  else
    GITHUB_REPO=false
  fi
else
  # Modo no interactivo - usar valores por defecto
  PROJECT_NAME="Workflow Harness"
  PROJECT_TYPE="generic"
  GITHUB_REPO=false
  info "Modo no interactivo - usando valores por defecto"
fi

# Crear archivo de configuración del proyecto
cat > .workflow-config.json <<EOF
{
  "project_name": "$PROJECT_NAME",
  "project_type": "$PROJECT_TYPE",
  "github_repo": $GITHUB_REPO,
  "initialized_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "harness_version": "1.0.0"
}
EOF

ok "Configuración guardada en .workflow-config.json"

# Crear .gitignore si se requiere
if [ "$GITHUB_REPO" = true ]; then
  if [ ! -f ".gitignore" ]; then
    cat > .gitignore <<EOF
# Workflow harness - archivos internos
/workflow
/agents
/tasks
/skills
audits/
user/
*.md
!README.md

# Dependencias
node_modules/
__pycache__/
*.pyc

# Entorno
.env
.DS_Store
EOF
    ok "Creado .gitignore inicial"
  else
    warn ".gitignore ya existe, no se sobrescribe"
  fi
fi

echo ""
echo "── 10. Verificando capa de specs ────────────────────"

if [ -d "specs" ]; then
  if [ -f "specs/_template.md" ]; then
    ok "Template de specs existe: _template.md"
  else
    warn "Falta _template.md en specs/"
  fi

  if [ -f "specs/_README.md" ]; then
    ok "Guía de specs existe: _README.md"
  else
    warn "Falta _README.md en specs/"
  fi

  ACTIVE_COUNT=0
  DRAFT_COUNT=0
  for dir in specs/*/; do
    if [ -f "${dir}spec.md" ]; then
      if grep -q "Estado.*active" "${dir}spec.md" 2>/dev/null; then
        ACTIVE_COUNT=$((ACTIVE_COUNT + 1))
      elif grep -q "Estado.*draft" "${dir}spec.md" 2>/dev/null; then
        DRAFT_COUNT=$((DRAFT_COUNT + 1))
      fi
    fi
  done

  if [ "$ACTIVE_COUNT" -gt 0 ]; then
    ok "Specs activas: $ACTIVE_COUNT"
  else
    warn "No hay specs activas en specs/"
  fi
  if [ "$DRAFT_COUNT" -gt 0 ]; then
    warn "Specs en draft: $DRAFT_COUNT (promover a active cuando corresponda)"
  fi
else
  warn "Carpeta specs/ no existe (opcional para proyectos nuevos)"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  RESUMEN DE INICIALIZACIÓN"
echo "═══════════════════════════════════════════════════════════"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
  ok "Harness verificado correctamente. Puedes comenzar a trabajar."
  info "Proyecto: $PROJECT_NAME ($PROJECT_TYPE)"
  info "Configuración: .workflow-config.json"
else
  fail "Harness tiene problemas. Revisa los errores arriba."
fi

exit $EXIT_CODE
