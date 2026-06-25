#!/usr/bin/env bash
set -u
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; BLUE='\033[0;34m'; NC='\033[0m'
ok()   { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn() { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
fail() { printf "${RED}[FAIL]${NC}  %s\n" "$1"; }
info() { printf "${BLUE}[INFO]${NC}  %s\n" "$1"; }
EXIT_CODE=0

echo "================================================"
echo "  WC2026 Predictor - Verificacion de Entorno"
echo "================================================"
echo ""

echo "-- 1. Python version --"
if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    fail "Python no encontrado"
    exit 1
fi
pyver=$($PY -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
info "Python: $pyver"
major=$(echo $pyver | cut -d. -f1)
minor=$(echo $pyver | cut -d. -f2)
if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 11 ]); then
    fail "Se requiere Python >= 3.11 (encontrado $pyver)"
    EXIT_CODE=1
else
    ok "Python $pyver"
fi

echo ""
echo "-- 2. Virtual environment --"
if [ -d ".venv" ]; then
    ok ".venv/ existe"
    source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true
else
    warn "No hay .venv/ - creando..."
    $PY -m venv .venv
    if [ $? -eq 0 ]; then
        ok ".venv/ creado"
        source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true
    else
        fail "No se pudo crear .venv/"
        EXIT_CODE=1
    fi
fi

echo ""
echo "-- 3. Dependencies --"
if $PY -m pip install -e ".[dev]" 2>&1 | tail -5; then
    ok "Dependencias instaladas"
else
    fail "Error instalando dependencias"
    EXIT_CODE=1
fi

echo ""
echo "-- 4. Import verification --"
$PY -c "
from src.config import settings; print(f'  Config: OK ({len(vars(settings))} vars)')
from src.data.loader import CsvLoader; print(f'  DataLoader: OK')
from src.models.prediction import OutcomeProbabilities; print(f'  Models: OK')
from src.predictors.null_model import NullModel; print(f'  NullModel: OK')
from src.predictors.elo_model import EloModel; print(f'  EloModel: OK')
from src.predictors.fifa_ranking import FifaRankingModel; print(f'  FifaRanking: OK')
from src.predictors.recent_form import RecentFormModel; print(f'  RecentForm: OK')
from src.predictors.goal_model import GoalModel; print(f'  GoalModel: OK')
from src.predictors.goal_plus_context import GoalPlusRecentContextModel; print(f'  GoalPlusContext: OK')
from src.predictors.selector import FinalPredictionSelector; print(f'  Selector: OK')
from src.probability import elo_expectation, brier_score, scoreline_matrix; print(f'  Probability: OK')
from src.simulation.monte_carlo import MonteCarloSimulator; print(f'  MonteCarlo: OK')
from src.simulation.group_table import GroupTableCalculator; print(f'  GroupTable: OK')
from src.services.prediction_service import PredictionService; print(f'  PredictionService: OK')
from src.services.evaluation_service import EvaluationService; print(f'  EvaluationService: OK')
from src.services.data_service import DataService; print(f'  DataService: OK')
" 2>&1
if [ $? -eq 0 ]; then
    ok "Todas las importaciones OK"
else
    fail "Fallaron importaciones"
    EXIT_CODE=1
fi

echo ""
echo "-- 5. Data files --"
for f in data/wc2026_groups.csv data/historical_results.csv data/elo_snapshot.csv data/fifa_rankings.csv; do
    if [ -f "$f" ]; then
        ok "$f existe"
    else
        fail "Falta $f"
        EXIT_CODE=1
    fi
done

echo ""
echo "-- 6. Running tests --"
if $PY -m pytest tests -v --tb=short 2>&1; then
    ok "Todos los tests pasan"
else
    fail "Hay tests fallando"
    EXIT_CODE=1
fi

echo ""
echo "================================================"
if [ $EXIT_CODE -eq 0 ]; then
    ok "Entorno listo para trabajar"
else
    fail "Hay problemas que resolver"
fi
exit $EXIT_CODE
