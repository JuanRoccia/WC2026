# TAREA PRINCIPAL DEL WORKFLOW

## Contexto del Proyecto

**WC2026 Predictor** — Sistema de predicción de resultados para el Mundial FIFA 2026.

### Stack Tecnológico
- **Backend**: Python 3.11+ / FastAPI
- **ML/Stats**: NumPy, SciPy, Pandas (modelos estadísticos custom)
- **Frontend**: HTML + Jinja2 Templates + Tailwind CSS
- **Base de datos**: SQLite (via SQLAlchemy o directo)
- **Testing**: pytest

### Estado Actual del Proyecto

| Área | Estado |
|------|--------|
| Estructura base Python | DONE |
| Datos semilla (CSV) | DONE |
| Modelos de datos | DONE |
| Predictores (escalera) | DONE |
| Probabilidad y estadística | DONE |
| Simulación Monte Carlo | IN PROGRESS (needs cache optimization) |
| Web UI / API | IN PROGRESS (API works, needs templates) |
| Evaluación | PENDING |
| Tests | PENDING |

---

## Objetivo Global

Construir un sistema de predicción para el Mundial 2026 con:
- **6 modelos jerárquicos**: Null → FIFA → Elo → RecentForm → GoalModel (Poisson+Dixon-Coles) → GoalPlusRecentContext
- **Simulación Monte Carlo** (10,000 sims) del torneo completo
- **Web UI** para visualizar predicciones y simulaciones
- **Evaluación rigurosa** con Brier Score, RPS, LogLoss

---

## Flujo de Trabajo Recomendado

```
1. ARQUITECTO (big-pickle)
   └─> Diseña arquitectura de datos y APIs

2. BACKEND (big-pickle)
   └─> Implementa modelos, predictores, simulación

3. FRONTEND/UI (minimax-m2.1-free)
   └─> Implementa web UI con templates

4. CODE REVIEWER (glm-4.7-free)
   └─> Revisa calidad del código

5. TESTER/DEBUGGER (kimi-k2.5-free)
   └─> Escribe tests y documenta

6. QA BROWSER (big-pickle)
   └─> Testea flujos en navegador real
```

---

## Estructura de Archivos del Proyecto

```
WC2026/
├── workflow-harness/           # Metodología de desarrollo (AGENTS.md, init.sh, feature_list.json, progress/)
├── src/                        # Código fuente Python
│   ├── main.py                 # FastAPI entry point (uvicorn)
│   ├── config.py               # Configuración tipada vía pydantic-settings
│   ├── models/                 # Pydantic: Team, Group, Fixture, Prediction, Tournament, Evaluation
│   │   ├── team.py
│   │   ├── fixture.py
│   │   ├── prediction.py
│   │   ├── tournament.py
│   │   ├── rating.py
│   │   ├── evaluation.py
│   │   └── __init__.py
│   ├── data/                   # Carga de datos CSV (CsvLoader + load_all_data)
│   │   ├── loader.py
│   │   └── __init__.py
│   ├── predictors/             # Escalera de 6 modelos jerárquicos
│   │   ├── base.py             # IPredictor abstracto, MatchContext
│   │   ├── null_model.py       # 33/33/33 uniforme
│   │   ├── fifa_ranking.py     # FIFA points como proxy
│   │   ├── elo_model.py        # Elo rating con expectación
│   │   ├── recent_form.py      # Delta de forma con decaimiento
│   │   ├── goal_model.py       # Poisson + Dixon-Coles
│   │   ├── goal_plus_context.py# GoalModel + contexto
│   │   ├── selector.py         # FinalPredictionSelector
│   │   └── __init__.py
│   ├── probability/            # Matemáticas estadísticas
│   │   ├── distributions.py    # elo_expectation, poisson_prob, dixon_coles_tau, scoreline_matrix
│   │   ├── metrics.py          # brier_score, rps_score, log_loss_score
│   │   └── __init__.py
│   ├── simulation/             # Monte Carlo engine
│   │   ├── monte_carlo.py      # MonteCarloSimulator (10K iteraciones)
│   │   ├── group_table.py      # GroupTableCalculator (desempates)
│   │   └── __init__.py
│   ├── services/               # Lógica de negocio
│   │   ├── prediction_service.py
│   │   ├── evaluation_service.py
│   │   ├── data_service.py
│   │   └── __init__.py
│   └── web/                    # API REST
│       ├── routes.py
│       └── __init__.py
├── data/                       # Datos CSV semilla
│   ├── wc2026_groups.csv       # 12 grupos, 48 selecciones
│   ├── historical_results.csv  # ~49,445 partidos (1872-2025)
│   ├── elo_snapshot.csv        # 242 ratings Elo (2026-06-24)
│   ├── fifa_rankings.csv       # 211 rankings FIFA (2026-06-11)
│   └── goalscorers.csv         # ~41,000 goleadores históricos
├── tests/                      # Tests pytest (pendientes)
├── requirements.txt            # Dependencias
├── pyproject.toml              # Configuración del proyecto
└── progress/                   # Documentación de sesión
    └── current.md
```

---

## Inicio del Workflow

1. Ejecuta `bash init.sh` para verificar el entorno
2. Lee `AGENTS.md` para entender el sistema
3. Lee tu tarea en `tasks/task-[rol].md`
4. Trabaja y documenta en `progress/current.md`
