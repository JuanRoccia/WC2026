# Prompt — Servicio de Evaluación (Feature #8)

## (1) Orden de lectura

1. `AGENTS.md`
2. `progress/current.md`
3. `feature_list.json` — feature #8
4. `src/services/evaluation_service.py`
5. `src/models/evaluation.py`
6. `src/probability/metrics.py`
7. `src/web/routes.py`
8. `specs/evaluation/spec.md`

## (2) Contexto

EvaluationService existe con estructura básica pero no persiste datos ni genera reportes. Los resultados evaluados se pierden al reiniciar el servidor.

Necesitamos almacenamiento SQLite, cálculo de métricas agregadas por predictor, y endpoints para consultar performance histórica.

## (3) Tarea Técnica

1. **Persistencia SQLite**: guardar cada evaluación en `data/wc2026.db` con tabla `evaluations` (fixture_id, predictor_name, home_goals, away_goals, home_win_p, draw_p, away_win_p, brier, rps, log_loss, timestamp).
2. **Métricas agregadas**: por predictor, calcular Brier medio, RPS medio, Top Pick Accuracy, detección de overconfident failures (alta confianza + resultado incorrecto).
3. **Endpoint /performance**: devolver tabla comparativa de predictores ordenada por Brier score ascendente.
4. **Inicializar DB al startup**: crear tabla si no existe.

## (4) Restricciones

- SQLAlchemy o sqlite3 nativo (sin dependencias extra)
- No borrar evaluaciones existentes en memoria
- Match existing code style del proyecto

## (5) Criterios de Éxito

- [ ] POST /fixtures/{id}/result persiste en SQLite
- [ ] GET /performance devuelve métricas agregadas desde DB
- [ ] Columnas: predictor, count, brier_avg, rps_avg, top_pick_acc, overconfident_fails
- [ ] Tabla se crea automáticamente al iniciar

## (6) Cierre de Sesión

1. Prueba con 3 resultados POST + GET /performance
2. Marca feature #8 como done
3. Documenta en progress/current.md
