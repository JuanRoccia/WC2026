# Prompt — Optimización de Simulación Monte Carlo (Feature #6 + #12)

## (1) Orden de lectura

1. `AGENTS.md`
2. `progress/current.md`
3. `feature_list.json` — features #6 y #12
4. `src/simulation/monte_carlo.py` — implementación actual
5. `src/services/prediction_service.py` — predict_direct() y cache
6. `src/web/routes.py` — endpoint /simulation

## (2) Contexto

La simulación Monte Carlo (10,000 iteraciones) es extremadamente lenta porque cada sample_match() llama a predict_direct() que ejecuta los 6 predictores completos.

Esto resulta en ~790,000 llamadas a predict_direct() por simulación (48 partidos grupo + ~31 eliminatorias × 10,000 iteraciones). Cada llamada tarda ~0.13s, resultando en horas de ejecución.

Solución: precomputar las 48×47=2,256 permutaciones posibles de matchup probabilities al startup y usarlas directamente en _sample_match().

## (3) Tarea Técnica

1. **Precomputación al startup**: en PredictionService, precompute_all_matchups() que itera todas las permutaciones de team_ids (48 equipos) y llama predict_direct() cacheando en _direct_cache.
2. **MonteCarloSimulator usa cache**: _sample_match() debe leer de _probs_cache interna o del cache de PredictionService en lugar de llamar predict_fn.
3. **Limitar número de simulaciones**: parametrizar sim rápido (100 iteraciones para debug) vs completo (10,000).
4. **Verificar**: la simulación debe completar 10,000 iteraciones en < 60 segundos.

## (4) Restricciones

- No modificar la API de los endpoints
- Mantener seed reproducible
- No perder la capacidad de simular con resultados reales ingresados (is_played)
- _direct_cache debe invalidarse si se agregan nuevos resultados

## (5) Criterios de Éxito

- [ ] Precomputación corre en startup (2256 predictions, < 5 minutos una sola vez)
- [ ] _sample_match usa cache, no predict_fn directa
- [ ] Simulación 10K completa en < 60 segundos
- [ ] Seed 2026 produce resultados consistentes
- [ ] Resultados ingresados manualmente se respetan en simulación

## (6) Cierre de Sesión

1. Ejecuta `uvicorn src.main:app` y prueba GET /simulation
2. Marca features #6 y #12 como done si pasa en < 60s
3. Documenta en progress/current.md
