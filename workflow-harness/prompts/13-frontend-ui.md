# Prompt — Frontend UI con Jinja2 + Tailwind (Feature #13)

## (1) Orden de lectura

1. `AGENTS.md`
2. `progress/current.md`
3. `feature_list.json` — feature #13
4. `src/web/routes.py` — API endpoints existentes
5. `src/main.py` — FastAPI app
6. `src/config.py` — Settings
7. `workflow-harness/skills/frontend-design/` — estilos disponibles

## (2) Contexto

La API REST está completa y funcional, pero no hay interfaz visual. Los usuarios deben usar curl o herramientas HTTP.

Implementar templates Jinja2 con Tailwind CSS (CDN) para todas las vistas, montados bajo el router existente. Diseño responsive para mobile y desktop.

## (3) Tarea Técnica

1. **Crear `src/web/templates/`**: base.html (layout con nav), index.html, fixtures.html, fixture_detail.html, groups.html, simulation.html, performance.html, predictor_lab.html, rankings.html.
2. **Crear `src/web/static/`**: CSS extra si es necesario (mínimo).
3. **Agregar rutas HTML** en routes.py que rendericen templates (prefijo /ui/ o rutas directas con HTMLResponse).
4. **Navegación**: menú superior con links a todas las vistas.
5. **Vista fixtures**: tabla con 72 partidos, predicción (home%, draw%, away%), indicador visual de favorito.
6. **Vista fixture detail**: escalera completa de 6 predictores, scoreline matrix heatmap (CSS grid).
7. **Vista simulation**: tabla de probabilidades por equipo con barras de progreso, campeón destacado.
8. **Vista groups**: 12 tabs/grupos con tabla de posiciones simulada.
9. **Predictor Lab**: formulario con dos selects de equipos, muestra resultados en tiempo real.
10. **Performance**: tabla comparativa de predictores con métricas, color coding.

## (4) Restricciones

- Tailwind CSS vía CDN (sin build step)
- Sin JavaScript frameworks — vanilla JS mínimo para interactividad
- No modificar endpoints JSON existentes
- Las rutas HTML deben coexistir sin conflictos
- Diseño Dark mode opcional

## (5) Criterios de Éxito

- [ ] base.html con layout y navegación responsive
- [ ] /ui/fixtures — tabla con 72 predicciones
- [ ] /ui/fixtures/{id} — detalle con escalera
- [ ] /ui/groups — 12 tabs de grupos
- [ ] /ui/simulation — tabla de probabilidades
- [ ] /ui/performance — ranking de predictores
- [ ] /ui/lab — predictor interactivo
- [ ] /ui/rankings — Elo y FIFA
- [ ] Navegación funcional entre todas las vistas

## (6) Cierre de Sesión

1. Verifica navegación completa en navegador
2. Prueba cada vista con datos reales del servidor
3. Marca feature #13 y actualiza feature #7 como done
4. Documenta en progress/current.md
