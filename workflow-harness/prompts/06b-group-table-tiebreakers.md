# Prompt — Verificación de GroupTableCalculator y Tiebreakers (Feature #6b)

## (1) Orden de lectura

1. `AGENTS.md`
2. `progress/current.md`
3. `feature_list.json` — feature #6
4. `src/simulation/group_table.py`
5. `src/models/tournament.py`

## (2) Contexto

El GroupTableCalculator implementa criterios de desempate: puntos > h2h > diff > goles > FIFA ranking. Pero nunca se verificó con casos reales de Mundial (ej: grupo con triple empate a 5 puntos).

La simulación Monte Carlo depende de estos desempates para determinar quién avanza. Si están mal, todas las probabilidades son incorrectas.

## (3) Tarea Técnica

1. **Verificar GroupTableCalculator.calculate()**: escribir test con casos conocidos:
   - Grupo con líder claro (9 puntos)
   - Empate a 4 puntos resuelto por h2h
   - Triple empate a 5 puntos resuelto por diff de goles
   - Empate perfecto (todo igual) resuelto por FIFA ranking
2. **Verificar selección de 8 mejores terceros**: simular 12 grupos y confirmar que los mejores 8 terceros avanzan correctamente.
3. **Agregar logging** para debuggear decisiones de desempate.

## (4) Restricciones

- No cambiar el algoritmo de desempate (debe seguir reglas FIFA)
- Match existing code style

## (5) Criterios de Éxito

- [ ] Test de desempate por puntos → h2h pasa
- [ ] Test de triple empate pasa
- [ ] Test de empate por ranking pasa
- [ ] GrupoTableCalculator se puede invocar desde tests aislados

## (6) Cierre de Sesión

1. Tests pasan al 100%
2. Documenta resultados en progress/
