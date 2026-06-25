# Tutorial del Workflow Harness - Guía para el Usuario

**Workflow Harness** es un sistema de orquestación para agentes de IA. Con esta guía aprenderás a usar todas las funciones de forma simple y rápida.

---

## Paso 1: Iniciar Sesión

1. Abre una terminal en la raíz del proyecto
2. Ejecuta el script de inicialización:
   ```bash
   bash init.sh
   ```
3. Completa la información solicitada (nombre del proyecto, tipo, etc.)

> **Tip:** El script verifica que todo el harness esté correctamente configurado.

---

## Paso 2: Conocer el Menú

En la pantalla verás las diferentes secciones:

| Ícono | Sección | Para qué sirve |
|-------|---------|----------------|
| 📋 | **AGENTS.md** | Punto de entrada y contexto |
| 🎯 | **feature_list.json** | Lista de tareas y estados |
| 📁 | **docs/** | Documentación del harness |
| 🔧 | **tasks/** | Tareas por agente |
| 🎨 | **skills/** | Habilidades especializadas |

---

## Paso 3: Configurar un Nuevo Proyecto

1. Andá a **AGENTS.md**
2. Leé la sección "Antes de empezar"
3. Ejecuta `./init.sh` para verificar el entorno
4. Configurá:
   - **Nombre del proyecto**
   - **Tipo de proyecto** (e-commerce, saas, landing, etc.)
   - **¿Se subirá a GitHub?** (para configurar .gitignore)

---

## Paso 4: Asignar Tareas a Agentes

Una vez configurado:

1. Andá a **features_list.json**
2. Identificá tareas con estado `pending`
3. Asigná un agente según el rol:

| Agente | Cuándo usarlo |
|--------|-------------|
| 🏗️ ARQUITECTO | Decisiones de arquitectura, seguridad |
| 📝 CODE REVIEWER | Revisión de código, calidad |
| 🧪 TESTER/DEBUGGER | Testing, debugging, documentación |
| 🎨 FRONTEND/UI | UI/UX, componentes, diseño |
| ⚙️ BACKEND | APIs, base de datos, lógica |
| 🎭 GHOST | Tareas flexibles, modos variables |

---

## Paso 5: Ejecutar el Workflow

Cuando un agente trabaja:

1. Leé el archivo de tarea en `tasks/task-[rol].md`
2. El agente analiza el codebase
3. El agente documenta en `progress/current.md`
4. Al finalizar:
   - Marcá la tarea como `done` en `feature_list.json`
   - Mové el resumen a `progress/history.md`
   - Vació `progress/current.md`

---

## Paso 6: Verificar Progreso

Para ver el estado general:

```bash
bash init.sh
```

El script te dirá:
- ✅ **[OK]** - Todo está bien
- ⚠️ **[WARN]** - Faltan archivos (no bloqueante)
- 🔴 **[FAIL]** - Hay errores (debe arreglarse)

---

## Paso 7: Control de Iteraciones (Opcional)

Si el proyecto requiere múltiples iteraciones:

1. Andá a **08-LOOP.md**
2. Seguí el flujo de iteraciones
3. Actualizá el contador de iteración
4. Al completar todas: cambiá estado a `COMPLETADO`

---

## Flujo Completo (Ejemplo Paso a Paso)

```
1. Ejecutar init.sh
         ↓
2. Leer AGENTS.md
         ↓
3. Configurar proyecto (init.sh)
         ↓
4. Asignar tarea a agente (feature_list.json)
         ↓
5. Agente lee task-[rol].md
         ↓
6. Agente analiza y trabaja
         ↓
7. Agente documenta en progress/current.md
         ↓
8. Verificar con init.sh
         ↓
9. Marcar tarea como done
         ↓
10. Mover resumen a progress/history.md
```

---

## Tips Rápidos

| Situación | Qué hacer |
|-----------|-----------|
| Quiero iniciar el workflow | Ejecuta `bash init.sh` y lee `AGENTS.md` |
| Un agente terminó su tarea | Marcá `done` en `feature_list.json` |
| Hay un error en el harness | Ejecuta `bash init.sh` para diagnóstico |
| Necesito documentación | Andá a `docs/` (architecture, conventions, verification) |
| Quiero un agente flexible | Usa **GHOST** con diferentes máscaras |

---

## Cómo Finalizar una Sesión

1. Ejecuta `bash init.sh` — todo verde
2. Si la tarea está lista: marcá `status: "done"` en `feature_list.json`
3. Mové el resumen de `progress/current.md` al final de `progress/history.md`
4. Vació `progress/current.md` dejando solo la plantilla
5. No dejes archivos temporales, ni `print()` de debug, ni TODOs sin contexto

---

## ¿Necesitás Ayuda?

Si tenés dudas sobrealguna función:
- Leé `AGENTS.md` nuevamente
- Consultá la documentación en `docs/`
- Revisá ejemplos en `progress/` (history.md)
- Contactá al administrador del sistema

---

*Tutorial del Workflow Harness - Versión 1.0 - Mayo 2026*
