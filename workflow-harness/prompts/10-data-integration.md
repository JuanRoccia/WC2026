# Prompt — Integración con APIs Externas (Feature #10)

## (1) Orden de lectura

1. `AGENTS.md`
2. `progress/current.md`
3. `feature_list.json` — feature #10
4. `src/data/loader.py`
5. `src/services/data_service.py`
6. `src/web/routes.py`

## (2) Contexto

Los datos de rankings FIFA y ratings Elo son snapshots estáticos descargados manualmente. Para mantener el sistema actualizado durante el Mundial 2026, necesitamos endpoints que refresquen estos datos desde fuentes web.

Prioridad baja — implementar solo si hay tiempo.

## (3) Tarea Técnica

1. **Actualización FIFA**: scrap de página oficial FIFA o API pública para obtener ranking actualizado.
2. **Actualización Elo**: fetch desde eloratings.net o international-football.net.
3. **Endpoint POST /refresh/rankings**: trigger manual de actualización.

## (4) Restricciones

- No agregar dependencias pesadas (usar httpx que ya está)
- Cachear resultados para no exceder rate limits
- No bloquear el servidor durante fetch (usar asyncio)

## (5) Criterios de Éxito

- [ ] POST /refresh/rankings actualiza FIFA + Elo
- [ ] Datos se guardan en CSV con timestamp
- [ ] Fallback a datos anteriores si fetch falla

## (6) Cierre de Sesión

1. Prueba el endpoint
2. Si es viable, marca como done; si no, deja como blocked con nota
