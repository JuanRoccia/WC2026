# Template de Prompt — <Nombre de Feature>

> Template estándar de 6 secciones para prompts de features.
> Copia este archivo, renómbralo según la feature, y completa cada sección.

---

## (1) Orden de lectura

Lee los siguientes archivos **en este orden** antes de empezar:

1. `AGENTS.md` — punto de entrada del workflow
2. `progress/current.md` — estado de la sesión actual
3. `feature_list.json` — lista de tareas pendientes
4. `specs/[modulo-relevante]/spec.md` — contrato funcional (si existe)
5. `prompts/[prompt-anterior.md]` — prompt de la iteración previa (si existe)

---

## (2) Contexto

<!-- Describe el feedback, bug, o motivación detrás de esta feature.
     Incluye referencias a issues, conversaciones, o decisiones previas. -->

*
*

---

## (3) Tarea Técnica

<!-- Desglose de lo que hay que implementar, en orden lógico. -->

1.
2.
3.

---

## (4) Restricciones

<!-- Qué NO hacer, límites técnicos, reglas del harness. -->

- No modifiques archivos fuera del alcance de esta feature.
- No agregues dependencias sin aprobación.
- No automatices servicios de pago (Stripe, etc.).
- No toques `shared/schema.ts` sin incluir migración.
- Match existing code style del proyecto.
- Si el cambio modifica comportamiento de un módulo con spec, actualiza su `changelog.md`.
- Una sola feature por sesión.

---

## (5) Criterios de Éxito

<!-- Checklist que debe pasar para marcar la feature como done. -->

- [ ] Código implementado según la tarea técnica
- [ ] `./init.sh` pasa sin errores
- [ ] Tests relevantes pasan (si aplica)
- [ ] No hay regresiones en features existentes
- [ ] La sesión queda documentada en `progress/`

---

## (6) Cierre de Sesión

<!-- Protocolo a seguir al terminar. -->

1. Ejecuta `./init.sh` — debe salir todo verde.
2. Si la feature está completa:
   - Marca `status: "done"` en `feature_list.json`.
   - Commit message: `<feature-name>: <descripción concisa>`
3. Mueve el resumen de `progress/current.md` al final de `progress/history.md`.
4. Vacía `progress/current.md` dejando solo la plantilla.
5. Elimina archivos temporales, prints de debug, y TODOs sin contexto.
