# WC2026 Predictor

Sistema de predicción de resultados para el Mundial FIFA 2026. Combina **6 modelos estadísticos jerárquicos** con **simulación Monte Carlo** para generar probabilidades de resultados de partidos y del torneo completo.

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.12+ / FastAPI |
| Modelos | NumPy, SciPy, Pandas |
| Predicción | Poisson + Dixon-Coles, Elo, FIFA Rankings, forma reciente |
| Simulación | Monte Carlo (10K iteraciones), bracket de 32 equipos |
| API | REST JSON (8 endpoints) |
 | Frontend | Jinja2 + Tailwind (9 templates) |
 | Testing | pytest (en progreso) |
| Metodología | workflow-harness (ver `workflow-harness/`) |

## Arquitectura

```
                      ┌──────────────┐
                      │   FastAPI     │
                      │  (8 routes)   │
                      └──────┬───────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
      ┌────────────┐ ┌────────────┐ ┌──────────────┐
      │ Predictor  │ │ MonteCarlo │ │ Evaluation   │
      │ Service    │ │ Simulator  │ │ Service      │
      └─────┬──────┘ └────────────┘ └──────────────┘
            │
    ┌───────┼───────────────┐
    ▼       ▼       ▼       ▼
 ┌─────┐ ┌─────┐ ┌─────┐ ┌──────────┐
 │Null │ │FIFA │ │Elo  │ │GoalModel │
 │Model│ │Rank │ │Model│ │+Context  │
 └─────┘ └─────┘ └─────┘ └──────────┘
```

### Escalera de predictores

Cada predictor implementa `IPredictor.predict(ctx) -> MatchPrediction`. El `FinalPredictionSelector` elige el mejor disponible según calibración Elo/FIFA y disponibilidad de datos:

| # | Predictor | Señales | Degradación |
|---|-----------|---------|-------------|
| 1 | NullModel | — | Base: 33/33/33 |
| 2 | FifaRankingModel | Puntos FIFA | Si faltan puntos |
| 3 | EloModel | Rating Elo | Si falta rating |
| 4 | RecentFormModel | Resultados recientes | Si faltan partidos |
| 5 | GoalModel | Poisson + Dixon-Coles | Si faltan goles históricos |
| 6 | GoalPlusRecentContext | GoalModel + lesiones | Si falta contexto |

## Instalación

```bash
# Python 3.12+ requerido
pip install -r requirements.txt
```

## Datos

Los datos CSV están en `data/`:

| Archivo | Contenido | Registros |
|---------|-----------|-----------|
| `wc2026_groups.csv` | Grupos del Mundial 2026 | 12 grupos, 48 selecciones |
| `historical_results.csv` | Partidos internacionales históricos | ~49,445 |
| `elo_snapshot.csv` | Ratings Elo actualizados | 242 equipos |
| `fifa_rankings.csv` | Rankings FIFA oficiales | 211 equipos |
| `goalscorers.csv` | Goleadores históricos | ~41,000 |

## Uso

```bash
# Iniciar servidor (dev con hot reload)
uvicorn src.main:app --reload --port 8000

# O usando el entry point
python -m src.main
```

### Servidor (pruebas locales)

**Iniciar** (de fondo, sin bloquear la terminal):
```powershell
$proc = Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000" -PassThru
Start-Sleep -Seconds 10
```

**Detener** (por puerto):
```powershell
$conn = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($conn) { Stop-Process -Id $conn.OwningProcess -Force; Write-Output "Server stopped" }
```

**Detener** (si guardaste el proceso con `-PassThru`):
```powershell
Stop-Process -Id $proc.Id -Force
```

**Verificar** que responde:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
```

### Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Healthcheck con conteos |
| GET | `/fixtures` | Los 72 fixtures con predicción |
| GET | `/fixtures/{id}` | Predicción detallada + escalera |
| GET | `/groups` | Grupos con equipos y fixtures |
| GET | `/simulation` | Simulación Monte Carlo (10K) |
| GET | `/predictor/lab?home=X&away=Y` | Comparar dos equipos |
| GET | `/rankings/elo` | Top 30 Elo ratings |
| GET | `/rankings/fifa` | Top 30 FIFA rankings |
| GET | `/performance` | Métricas de evaluación |
| POST | `/fixtures/{id}/result?home_goals=X&away_goals=Y` | Ingresar resultado real |

### Ejemplos

```bash
curl http://localhost:8000/health
# {"status":"ok","fixtures":72,"groups":12,"predictors":6}

curl http://localhost:8000/simulation
# {"simulation_count":10000,"most_likely_champion":"argentina",...}

curl "http://localhost:8000/predictor/lab?home=argentina&away=brazil"
# {"home":"argentina","away":"brazil","home_win":42.3,"draw":27.8,"away_win":29.9,"top_pick":"home"}
```

## Estado del proyecto

Ver `feature_list.json` en `workflow-harness/` para la lista completa de features y su estado.

| Feature | Estado |
|---------|--------|
| Estructura base Python | ✅ Done |
| Importación de datos | ✅ Done |
| Modelos de datos | ✅ Done |
| Escalera de 6 predictores | ✅ Done |
| Probabilidad y estadística | ✅ Done |
| Generación de fixtures | ✅ Done |
| API REST + Web UI | ✅ Done |
| Simulación Monte Carlo | ✅ Done (optimizada) |
| Evaluación de predicciones | 🔧 In progress (almacenamiento persistente pendiente) |
| Tests | ⏳ Pending |
| Predictor Lab interactivo | ✅ Done |

## Pendiente

1. **Tests** — pytest para predictores, probabilidad, simulación
2. **EvaluationService** — almacenamiento persistente y reportes detallados
3. **Bracket seeding** — implementar el bracket real de 32 equipos del Mundial 2026

## Desarrollo

Este proyecto usa [workflow-harness](workflow-harness/) como metodología de desarrollo. Ver `workflow-harness/AGENTS.md` para entender el flujo.
