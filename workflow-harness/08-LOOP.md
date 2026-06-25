# 08-LOOP - Control de Iteraciones del Workflow

> Este archivo es opcional y sirve para proyectos que requieran múltiples iteraciones.
> Para proyectos simples, este archivo puede eliminarse.

---

## Configuración

```yaml
# Configuración del Loop
ITERACIONES_TOTALES: 3
ITERACION_ACTUAL: 1
FECHA_INICIO: "2026-05-01"
ULTIMA_ACTUALIZACION: "2026-05-01"
ESTADO: "EN_PROGRESO"
```

---

## Objetivo

Ejecutar múltiples iteraciones del workflow para completar las áreas definidas en `feature_list.json` de manera sistemática.

---

## Flujo del Loop

```
AGENTS.md → task-arquitecto.md → task-code-reviewer.md → task-tester.md → 
task-frontend.md → task-backend.md → task-ghost.md → 08-LOOP.md
                   ↓
             Revisar progreso
                   ↓
             Actualizar contador
                   ↓
             Si ITERACION_ACTUAL < ITERACIONES_TOTALES → Continuar
             Si ITERACION_ACTUAL = ITERACIONES_TOTALES → Finalizar
```

---

## Iteraciones

### Iteración 1 (En progreso)
| Campo | Valor |
|-------|-------|
| Inicio | 2026-05-01 |
| Estado | ⚠️ EN_PROGRESO |
| Tareas completadas | Setup inicial, limpieza, tests |

### Iteración 2 (Pendiente)
| Campo | Valor |
|-------|-------|
| Inicio | - |
| Estado | ⏳ PENDIENTE |
| Tareas | Auditoría de skills, integración final |

### Iteración 3 (Pendiente)
| Campo | Valor |
|-------|-------|
| Inicio | - |
| Estado | ⏳ PENDIENTE |
| Tareas | Producción, CI/CD, Deployment |

---

## Cómo Usar Este Archivo

### Al Iniciar una Iteración
1. Leer `AGENTS.md` para contexto del workflow
2. Revisar `feature_list.json` para ver tareas pendientes
3. Ejecutar las fases del workflow en orden

### Al Finalizar una Fase
1. Actualizar este archivo con el progreso
2. Marcar tareas completadas en `feature_list.json`
3. Continuar con la siguiente fase

### Al Llegar a Este Archivo (08-LOOP.md)
1. **Revisar progreso**: ¿Qué se completó?
2. **Actualizar contador**: `ITERACION_ACTUAL += 1`
3. **Si hay más iteraciones**: Volver a `AGENTS.md`
4. **Si se completaron todas**: Finalizar y documentar resultados

---

## Comandos de Control

### Iniciar Iteración
```markdown
# ITERACION_ACTUAL: 2
# ULTIMA_ACTUALIZACION: [FECHA_HOY]
```

### Completar Iteración
```markdown
# ITERACION_ACTUAL: 2 → 3
# Completado: [TAREAS_REALIZADAS]
```

### Finalizar Workflow
```markdown
# ESTADO: COMPLETADO
# FECHA_FIN: [FECHA_HOY]
```

---

## Tareas del feature_list.json

Ver archivo `feature_list.json` para ver el listado completo de tareas.

### Pendientes de Esta Iteración
- [ ] [TAREA 1]
- [ ] [TAREA 2]
- [ ] [TAREA 3]

---

## Referencias

| Archivo | Propósito |
|---------|-----------|
| `AGENTS.md` | Punto de entrada y contexto |
| `feature_list.json` | Lista de tareas |
| `TASK-PRINCIPAL.md` | Objetivo global |
| `tasks/*.md` | Tareas por agente |
| `progress/` | Seguimiento de sesiones |

---

*08-LOOP - Control de Iteraciones - Workflow Harness Genérico*
