# Bitácora histórica (append-only)

> Cada vez que se cierra una sesión, su resumen se añade aquí.
> No edites entradas anteriores. Solo añades al final.

---

## 2026-05-01 — Inicialización del workflow-harness
- **Agente:** humano (Juan Manuel)
- **Cambios:** creación inicial de la estructura del harness (AGENTS.md, init.sh, feature_list.json, progress/).
- **Resultado:** entorno base listo. Pendiente limpieza de referencias específicas de proyectos.

---

## 2026-05-04 — Limpieza y Generización del Harness
- **Agente:** humano (Juan Manuel)
- **Cambios:**
  - Eliminado `00-INICIO.md` (reemplazado por AGENTS.md)
  - Eliminado `09-TODO.md` (reemplazado por feature_list.json)
  - Movido `07-BUGS-REPORT.md` a `audits/`
  - Adaptado `08-LOOP.md` a genérico
  - Task 7 (tests_structure) completada
  - Creados tests en `tests/` (test_feature_list.py, test_structure.py, test_init.sh)
  - Actualizado `init.sh` para ejecutar tests automáticamente
  - Eliminado `skill-gsap.txt` (solo un link a GitHub)
  - Eliminado `skill-business-logic.md` (DIROCCO específico)
  - `audit.md` y `auditoria.md` convertidos a plantillas genéricas
  - `user/TUTORIAL.md` convertido a guía genérica del harness
  - `07-BUGS-REPORT.md` renombrado (plantilla genérica)
  - Task 6 (skills_audit) completada
  - Task 3 (clean_project_references) completada
  - `init.sh` actualizado para modo no interactivo
  - Arreglado `test_init.sh` (sintaxis)
  - Task 4 (progress_structure) completada
  - Task 5 (docs_structure) completada
  - Task 2 (agents_md_entrypoint) completada
  - Task 1 (init_script) completada

- **Resultado:** ✅ Harness completamente genérico y projectless. Todas las tareas en `feature_list.json` marcadas como `done`.

---

*Última actualización: 2026-05-04*

---

## 2026-06-25 — Codebase audit, bugfixes, GitHub push
- **Agente:** big-pickle (opencode)
- **Análisis:** Audit completo del codebase — 27 archivos Python, 9 templates, 5 CSVs, 1 JSON. Detectados 2 bugs críticos, 5 altos, 6 medios, 4 bajos.
- **Cambios:**
  - **Bug crítico fix #1** (`recent_form.py`): Columnas `home_goals`/`away_goals` no existen en CSV (son `home_score`/`away_score`). `team_id` se comparaba contra nombres originales sin normalizar. El modelo ahora computa forma reciente correctamente.
  - **Bug crítico fix #2** (`monte_carlo.py` `_sample_match`): Usaba probabilidades de resultado (0-1) como medias Poisson. Ahora usa `expected_home_goals`/`expected_away_goals` del modelo predictivo. Muestreo estadísticamente correcto.
  - **Fix altos:**
    - Selección de mejores terceros: ahora ordena por puntos → GD → GS (antes solo puntos)
    - `selector.py`: Match `"Goles"` cambiado a `"Modelo de goles"` (antes coincidía también con `"Goles + Contexto"`)
    - `DirectPrediction` class creada — `predict_direct()` ahora retorna expected_goals además de probabilidades
  - **Fix medios:**
    - `goal_plus_context.py`: imports movidos a nivel de módulo
    - `routes.py`: import muerto `OutcomeProbabilities` eliminado
    - `requirements.txt`: `csvkit` removido (no se usa)
    - `pyproject.toml`: dependencias sincronizadas, sección `[dev]` añadida
    - `seed_real_results.py`: path absoluto reemplazado por `Path(__file__).resolve()`
    - `loader.py`: `flag_code` ahora se lee del CSV
    - `.gitignore`: expandido (pycache, venv, IDE, coverage, etc.)
    - `README.md`: tabla de features actualizada al estado real
    - `feature_list.json`: feature #8 evaluación marcada como `in_progress`
  - **GitHub:** Repo inicializado, commit inicial (54 archivos, 100K+ líneas), push a `https://github.com/JuanRoccia/WC2026`
  - Feature #18 agregada: barra de progreso para simulación Monte Carlo (pending)
- **Verificación:** `python -c "from src.main import app"` → OK. Servidor inicia en :8000. Endpoints health, fixtures, fixture_detail, groups, predictor_lab, rankings responden OK.
- **Problemas conocidos que persisten:**
  1. `simulation/bracket.py` es código muerto (nunca se importa ni llama)
  2. Bracket de eliminatorias no sigue el seeding real de WC2026 (parea secuencialmente)
  3. EvaluationService sin persistencia (en memoria)
  4. Sin tests de pytest para el proyecto
  5. Sin init.sh en raíz del proyecto
- **Resultado:** ✅ Codebase auditado, bugs críticos corregidos, repo en GitHub listo.

---

## 2026-06-25 — Features #18, #19 + server commands en README
- **Agente:** big-pickle (opencode)
- **Cambios:**
  - Feature #18 agregada: barra de progreso para simulación Monte Carlo (pending)
  - Feature #19 agregada: predicciones del día con filtro por fecha (pending)
  - README.md: nueva sección "Servidor (pruebas locales)" con comandos PowerShell para start/stop con y sin `-PassThru`, y verificación con health endpoint
- **Resultado:** ✅ Sesión cerrada. Próximo paso: feature #18 o #19 según prioridad.

## 2026-06-24 — Primera iteración WC2026 Predictor
- **Agente:** big-pickle (opencode)
- **Contexto:** Se clonó Oloraculo (repo original .NET) para análisis de arquitectura, luego se eliminó. Se adaptó workflow-harness como metodología para el proyecto WC2026.
- **Stack elegido:** Python/FastAPI (en lugar de .NET/Blazor como Oloraculo original)
- **Cambios:**
  - Creada estructura completa del proyecto: src/ con models/, data/, predictors/, probability/, simulation/, services/, web/; data/ con 5 CSVs; tests/; requirements.txt; pyproject.toml
  - Modelos Pydantic: Team, Group, Fixture, MatchResult, FixtureContext, OutcomeProbabilities, MatchPrediction, MatchPredictionResult, TournamentProjection, TeamTournamentProbability, Rating, EvaluationRow
  - 6 predictores jerárquicos: NullModel, FifaRankingModel, EloModel, RecentFormModel, GoalModel (Poisson+Dixon-Coles), GoalPlusRecentContextModel
  - FinalPredictionSelector con calibración Elo/FIFA y degradación controlada
  - Módulo de probabilidad: elo_expectation, poisson_prob, dixon_coles_tau, scoreline_matrix, brier_score, rps_score, log_loss_score
  - MonteCarloSimulator: 12 grupos, bracket 32 equipos, seed 2026, 10K iteraciones
  - API REST: 10 endpoints (health, fixtures, fixture_detail, groups, simulation, predictor_lab, rankings/elo, rankings/fifa, performance, set_result)
  - Datos descargados: wc2026_groups.csv (48 selecciones), elo_snapshot.csv (242 equipos), fifa_rankings.csv (211 equipos), historical_results.csv (~49,445 partidos), goalscorers.csv (~41,000 goleadores)
  - Python 3.12 instalado vía winget, dependencias instaladas, servidor verificado en :8001
  - Bugfix: rename campo datetime→kickoff y date→record_date en modelos por shadowing de tipos
  - Bugfix: columna elo→elo_rating en loader.py
  - Caché añadida a PredictionService para /fixtures y predict_match
  - README.md completo creado
  - feature_list.json actualizado (13 features)
  - 6 prompts creados en workflow-harness/prompts/
- **Problemas conocidos que persisten:**
  1. Simulación Monte Carlo demasiado lenta (~790K predict_direct calls) — requiere precomputación de 2256 matchup probabilities
  2. GroupTableCalculator sin verificar (tiebreakers no probados)
  3. Sin frontend HTML (solo API JSON)
  4. EvaluationService sin persistencia SQLite
  5. Sin tests de pytest
  6. Sin init.sh funcional
  7. Player context hardcodeado (FixtureContext siempre default)
- **Resultado:** ✅ Primera iteración completa del back-end. Pendiente: cache optimization, frontend, tests, evaluation persistence.

---

## 2026-06-04 — Sistema de Prompts Reutilizables (Feature #11)
- **Agente:** big-pickle
- **Cambios:**
  - Creado `prompts/prompt-template.md` con template estándar de 6 secciones (orden de lectura, contexto, tarea técnica, restricciones, criterios de éxito, cierre de sesión)
  - Feature #11 agregada a `feature_list.json` y marcada como `done`
  - AGENTS.md actualizado — agregada entrada `prompts/` al mapa del repositorio
  - `init.sh` actualizado — verifica existencia de `prompts/`
  - `init.sh` → todo verde
- **Resultado:** ✅ Metodología de prompts formalizada como componente del harness.

---

## 2026-06-24 — Frontend UI con Jinja2 + Tailwind (Features #7, #13)
- **Agente:** big-pickle (opencode)
- **Cambios:**
  - Creados 9 templates HTML con Jinja2 + Tailwind (CDN):
    - `base.html` — layout responsive con navegación sticky, dark mode
    - `index.html` — página principal con resumen y tarjetas de acceso
    - `fixtures.html` — tabla de 72 partidos con predicciones coloreadas
    - `fixture_detail.html` — escalera completa de 6 predictores, score más probable
    - `groups.html` — grilla de 12 grupos con equipos y fixtures
    - `simulation.html` — tabla de probabilidades Monte Carlo con barras de progreso
    - `performance.html` — ranking de predictores con métricas y color coding
    - `predictor_lab.html` — formulario interactivo con selects + JS vanilla
    - `rankings.html` — top 30 Elo y FIFA lado a lado
  - Agregadas 8 rutas HTML en routes.py (`/ui/`, `/ui/fixtures`, `/ui/fixtures/{id}`, `/ui/groups`, `/ui/simulation`, `/ui/performance`, `/ui/lab`, `/ui/rankings`)
  - Configurado Jinja2Templates en routes.py
  - Cambiado puerto default a 8001 en main.py
  - Bugfix: `GoalPlusRecentContextModel` no seteaba `most_likely_score` ni `scoreline` — siempre devolvía (0,0)
- **Feature status:**
  - #7 (web_api): done (API + templates completos)
  - #13 (frontend_ui): done (8 vistas creadas y verificadas en navegador)
  - #14 (fix_prediction_quality): created — pendiente (GoalPlusRecentContextModel corregido, falta computar attack/defense strengths desde históricos)
- **Problemas conocidos:**
  1. Predicciones idénticas entre equipos de distinto nivel (attack/defense_strength siempre 1.0)
  2. Sin tests de pytest
  3. EvaluationService sin persistencia
  4. Sin init.sh en raíz del proyecto
  5. Player context hardcodeado
- **Resultado:** ✅ Frontend UI completo. Sesión cerrada.

---

## 2026-06-25 — Bracket seeding oficial WC2026 (Features #20, #21)
- **Agente:** big-pickle (opencode)
- **Cambios:**
  - Implementado bracket oficial del Mundial 2026 con seeding correcto (Annex C)
  - Creado `src/simulation/annex_c.py` con las 495 combinaciones de la tabla oficial FIFA
  - `MonteCarloSimulator._simulate_knockout()` reemplazado por `_build_r32_matches()` + `_simulate_bracket()` con estructura de llaves real:
    - R32: 16 partidos (8 winner-vs-3rd vía Annex C, 4 winner-vs-runner-up, 4 runner-up-vs-runner-up)
    - R16: M89-M96 con pairings oficiales
    - QF → SF → Final con bracket path correcto
  - Eliminado `src/simulation/bracket.py` (BracketBuilder era dead code)
  - Actualizado `src/simulation/__init__.py`
  - Tests actualizados: `TestBracketBuilder` → `TestAnnexC` (6 nuevos tests)
  - Agregadas 3 nuevas features a `feature_list.json`: #24 CI/CD, #25 Docker, #26 dev tooling
  - Feature #20 → done, Feature #21 → done
- **Verificación:** `python -m pytest tests/ -q` → 130 passed (0 failures), ~3:46 min
- **Problemas conocidos que persisten:**
  1. EvaluationService sin persistencia (feature #22)
  2. Sin barra de progreso en simulación (feature #18)
  3. Sin predicciones por fecha (feature #19)
  4. Sin datos de FixtureContext (feature #23)
  5. CI/CD, Docker, dev tooling sin configurar (features #24-#26)
- **Resultado:** ✅ Bracket corregido. Sesión cerrada.

---

## 2026-06-25 — Barra de progreso simulación Monte Carlo (Feature #18)
- **Agente:** big-pickle (opencode)
- **Cambios:**
  - `MonteCarloSimulator.__init__` acepta `progress_callback` opcional, reporta avance en `_precompute` y `simulate`
  - Nuevo endpoint SSE `/simulation/stream?count=N` que transmite progreso en tiempo real
  - `/ui/simulation` ahora carga instantáneamente (sin bloquear por simulación)
  - `simulation.html` reescrito: barra de progreso animada con EventSource, resultados se muestran al completar
  - `/simulation` (JSON) conserva comportamiento síncrono para compatibilidad
- **Archivos modificados:**
  - `src/simulation/monte_carlo.py` — progress_callback en constructor, _precompute, simulate
  - `src/web/routes.py` — nuevo /simulation/stream, /ui/simulation simplificado
  - `src/web/templates/simulation.html` — progress bar + EventSource JS
- **Verificación:** `python -m pytest tests/ -q` → 130 passed (~3.5 min)
- **Resultado:** ✅ Feature #18 completada. Sesión cerrada.
