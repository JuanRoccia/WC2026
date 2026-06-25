# AGENTS.md — Mapa de navegación para agentes de IA

> Este archivo es el **punto de entrada** para cualquier agente que trabaje en este
> repositorio. NO es una biblia de reglas: es un **mapa**. Lee solo lo que
> necesites cuando lo necesites (divulgación progresiva).

---

## 0. Directrices de Comportamiento (Karpathy)

Follow these behavioral guidelines to reduce common LLM coding mistakes. These bias toward caution over speed; use judgment for trivial tasks.

### 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## 1. Antes de empezar (obligatorio)

1. Ejecuta `./init.sh` y verifica que termina sin errores. Si falla, **para**
   y resuelve el entorno antes de tocar código.
2. Lee `progress/current.md` para entender en qué estado quedó la última sesión.
3. Si existe `specs/[módulo-relevante]/spec.md`, léela antes de tocar ese módulo.
4. Lee `TODO.md` y elige **una** tarea con estado `pending`. No
   trabajes en más de una a la vez.

## 2. Mapa del repositorio

| Archivo / carpeta            | Qué contiene                                              | Cuándo leerlo |
|------------------------------|-----------------------------------------------------------|---------------|
| `TODO.md`                    | Lista de tareas con estado (pending / in_progress / done)  | Siempre, al empezar |
| `progress/current.md`        | Estado de la sesión actual                                | Siempre, al empezar |
| `progress/history.md`        | Bitácora append-only de sesiones anteriores               | Si necesitas contexto histórico |
| `agents/`                    | Definiciones de roles de agentes (arquitecto, backend, etc) | Al asumir un rol específico |
| `tasks/`                     | Tareas específicas por agente                             | Al ejecutar tarea de un rol |
| `skills/`                    | Skills especializados (PDF, GSAP, diseño, etc.)          | Según necesidad técnica |
| `TASK-PRINCIPAL.md`          | Objetivo global del workflow                              | Para entender el propósito general |
| `TESTING-MANUAL.md`          | Guía de testing manual                                    | Antes de validar cambios |
| `BUGS-REPORT.md`             | Plantilla para reportar bugs                              | Al encontrar un error |
| `specs/`                     | Contratos funcionales de cada módulo                     | Antes de tocar cualquier módulo |
| `audits/`                    | Auditorías de seguridad y calidad                         | Para revisar hallazgos previos |
| `tests/`                     | Tests automáticos o manuales                              | Para verificar |
| `qa/`                        | Tests E2E con navegador (Playwright)                     | Antes de marcar feature como `done` |
| `prompts/`                   | Templates de prompts reutilizables (6-sección)            | Al planificar una nueva feature |
| `user/`                      | Documentación para usuarios                               | Referencia externa |
| `init.sh`                    | Script de verificación de entorno                         | Al iniciar sesión |

## 3. Reglas duras (no negociables)

- **Una sola tarea a la vez.** No mezcles cambios de varias tareas en la misma sesión.
- **No declares una tarea `done` sin pruebas verdes.** Ejecuta `./init.sh` y
  asegúrate de que el bloque de tests pasa al 100%.
- **Documenta lo que haces** en `progress/current.md` mientras trabajas, no al final.
- **Deja el repositorio limpio** antes de cerrar la sesión (ver §5).
- **Si modificás comportamiento de un módulo que tiene spec, actualizá el
  changelog.md de esa spec con el delta funcional.**
- **Si no sabes algo, busca en `docs/`** antes de inventarlo.

## 4. Cómo elegir una tarea

```
1. Abre feature_list.json
2. Filtra por status == "pending"
3. Coge la de mayor prioridad (menor "id")
4. Cambia su status a "in_progress" y guarda
5. Anota en progress/current.md: tarea, hora de inicio, plan breve
```

## 5. Cierre de sesión (lifecycle)

Antes de terminar:

1. Ejecuta `./init.sh` — todo verde.
2. Si la tarea está acabada: marca `status: "done"` en `TODO.md`.
3. Mueve el resumen de `progress/current.md` al final de `progress/history.md`.
4. Vacía `progress/current.md` dejando solo la plantilla.
5. No dejes archivos temporales, ni `print()` de debug, ni TODOs sin contexto.

## 6. Si te bloqueas

- Relee la sección relevante de `agents/` o `docs/`.
- Si la herramienta no hace lo que esperas, **no inventes un workaround**:
  documenta el bloqueo en `progress/current.md` y para la sesión.

---

## 7. Roles disponibles

| Rol | Archivo | Responsabilidad |
|-----|---------|-----------------|
| **ARQUITECTO** | `agents/01-arquitecto.md` | Diseño de datos, APIs, arquitectura |
| **CODE REVIEWER** | `agents/02-code-reviewer.md` | Calidad de código, bugs, anti-patterns |
| **TESTER/DEBUGGER** | `agents/03-tester-debugger.md` | Testing, documentación, edge cases |
| **FRONTEND/UI** | `agents/04-frontend-ui.md` | UI, UX, componentes |
| **BACKEND** | `agents/05-backend.md` | APIs, lógica de negocio, BD |
| **QA BROWSER** | `agents/07-qa-browser.md` | Testing E2E en navegador real |
| **GHOST** | `agents/06-ghost.md` | Agente flexible para tareas variables |

---

*Este archivo sirve como punto de entrada del workflow.*
