# Prompt — Tests y Documentación (Feature #11)

## (1) Orden de lectura

1. `AGENTS.md`
2. `progress/current.md`
3. `feature_list.json` — feature #11
4. `src/` completo — entender cada módulo
5. `workflow-harness/specs/_template.md`
6. `workflow-harness/tests/` — estructura existente de tests del harness

## (2) Contexto

No hay tests unitarios ni de integración. Todos los módulos necesitan cobertura de pytest.

Hay que escribir tests para cada predictor, módulo de probabilidad, simulación Monte Carlo, servicios y API endpoints.

También crear init.sh que verifique el entorno (Python, imports, tests).

## (3) Tarea Técnica

1. **init.sh**: script que verifique:
   - python3 --version >= 3.11
   - pip install -r requirements.txt
   - python -c "from src.main import app; print('OK')"
   - pytest tests/ -v
2. **tests/test_probability.py**:
   - elo_expectation valores conocidos
   - poisson_prob suma = 1
   - dixon_coles_tau simetría
   - scoreline_matrix suma = 1
   - brier_score, rps_score, log_loss_score casos borde
3. **tests/test_predictors.py**:
   - NullModel retorna 33/33/33
   - FifaRankingModel sin datos retorna degradado
   - EloModel favorito local
   - Cada predictor implementa IPredictor
4. **tests/test_simulation.py**:
   - GroupTableCalculator con casos conocidos
   - Desempate por puntos, h2h, diff
5. **tests/test_api.py**:
   - GET /health retorna 200
   - GET /fixtures retorna 72 fixtures
   - GET /fixtures/{id} retorna predicción

## (4) Restricciones

- Tests deben ser independientes (no compartir estado mutable)
- Usar monkeypatch para mockear datos si es necesario
- No modificar código fuente para hacer tests pasar
- init.sh debe fallar con código de salida != 0 si algo falla

## (5) Criterios de Éxito

- [ ] pytest tests/ -v pasa 100%
- [ ] init.sh termina sin errores
- [ ] Cobertura mínima: probability 90%, predictors 80%, simulation 70%
- [ ] init.sh es ejecutable (chmod +x)

## (6) Cierre de Sesión

1. Ejecuta `./init.sh` — todo verde
2. Marca feature #11 como done
3. Mueve resumen a progress/history.md
