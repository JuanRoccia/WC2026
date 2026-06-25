# Arquitectura — Qué significa "hacer un buen trabajo"

> Este documento define el estándar de calidad del workflow harness.
> Los agentes evalúan su trabajo contra este archivo.

## Principios

1. **Capas claras.** El harness tiene capas definidas:
   - `agents/` — definiciones de roles y comportamiento de agentes.
   - `tasks/` — tareas específicas asignadas a cada agente.
   - `skills/` — capacidades especializadas reutilizables.
   - `progress/` — seguimiento de sesiones y bitácora.
   - `qa/` — tests E2E con navegador real (Playwright).
   No introducir capas adicionales sin documentar la razón en `feature_list.json`.

2. **Sin dependencias externas innecesarias.** Bash y Python stdlib son suficientes.
   Si se requiere una herramienta externa, primero documentarse en `feature_list.json` (estado `blocked`).

3. **Errores explícitos.** Los scripts y archivos de configuración deben validar
   entradas y lanzar errores claros con mensajes descriptivos.

4. **Atomicidad en archivos críticos.** Operaciones sobre `feature_list.json`,
   `progress/current.md` y archivos de configuración deben ser atómicas.
   Escribir a archivo temporal y luego `mv`/`rename`.

5. **Inmutabilidad de registros históricos.** `progress/history.md` es append-only.
   Nunca editar entradas anteriores.

## Flujo del workflow

```
usuario ─→ init.sh (verificación)
           │
           ├─→ AGENTS.md (lee instrucciones)
           │
           └─→ agents/[rol].md (asume rol)
                │
                ├─→ tasks/task-[rol].md (lee tarea)
                │
                └─→ progress/current.md (registra trabajo)
                     │
                     └─→ feature_list.json (actualiza estado)
```

## Estructura de datos

### feature_list.json
- Formato JSON estructurado con array de `features`.
- Cada feature tiene: `id`, `name`, `title`, `description`, `priority`, `acceptance`, `status`.
- Estados válidos: `pending`, `in_progress`, `done`, `blocked`.

### progress/current.md
- Plantilla de sesión actual.
- Se vacía al cerrar sesión y se mueve a `history.md`.

### agents/*.md
- Definición de rol, responsabilidades, instrucciones específicas.
- Un archivo por agente siguiendo patrón: `NN-nombre.md`.

### specs/*/spec.md
- Contrato funcional de un módulo usando formato BDD (DADO/CUANDO/ENTONCES).
- Cada spec tiene estado: `draft`, `active`, o `deprecated`.
- Se complementa con `changelog.md` (delta funcional) y `decisions.md` (ADRs).

## La capa de specs

### Por qué existe

El harness orquesta CÓMO trabajan los agentes (vía `agents/`, `tasks/`,
`progress/`). Pero sin specs, cada sesión arranca de cero respecto al
comportamiento esperado del producto.

La capa `specs/` agrega contexto persistente: un agente que retoma un módulo
después de semanas lee la spec y sabe qué contratos funcionales respetar.

### Relación con tasks/ y feature_list.json

| Componente | Rol | Ejemplo |
|------------|-----|---------|
| `tasks/` | Órdenes para el agente | "Implementar login con remember me" |
| `specs/` | Contratos del sistema | "El sistema SHALL mantener sesiones de 30 días" |
| `feature_list.json` | Inventario de qué falta | Estado global de features |

**No son redundantes**:
- `tasks/` dice QUÉ HACER ahora.
- `specs/` dice QUÉ DEBE HACER el sistema (contexto estable).
- `feature_list.json` dice QUÉ FALTA (estado del proyecto).

### Principio clave

Las specs capturan COMPORTAMIENTO ESPERADO, no implementación.

Un agente debe poder entender qué hace el módulo sin leer código fuente.
Si necesita leer código para entender la spec, la spec está mal.

### Cuándo las specs bloquean

**Nunca**. Las specs son contexto, no gates.

Un agente puede:
- Implementar algo no especificado (documentarlo luego).
- Cuestionar la spec si encuentra contradicciones.
- Modificar la spec si el comportamiento cambia (vía changelog).

Pero NO puede ignorar una spec existente sin documentar por qué.

## Qué NO hacer

- No usar rutas hardcodeadas a proyectos específicos (ej: `/home/runner/workspace/`).
- No mezclar múltiples tareas en una sesión.
- No marcar `done` sin ejecutar `./init.sh` y ver tests verdes.
- No editar `progress/history.md` (solo append).
- No dejar archivos temporales ni TODOs sin contexto.
