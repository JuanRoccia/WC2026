# BUGS-REPORT.md — Plantilla de Reporte de Bugs

> Este archivo es una plantilla para documentar bugs encontrados durante el desarrollo.
> Llena una sección por cada bug encontrado.

---

## Formato de Reporte de Bug

```markdown
### [Número] - [Título Breve]

**Fecha**: [YYYY-MM-DD]
**Severidad**: 🔴 Crítica / 🟠 Alta / 🟡 Media / 🟢 Baja
**Agente**: [Rol que encontro el bug]
**Estado**: Pending / In Progress / Fixed / Won't Fix

#### Descripción
[Descripción clara del problema]

#### Pasos para Reproducir
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

#### Comportamiento Esperado
[Qué debería pasar]

#### Comportamiento Actual
[Qué está pasando]

#### Ubicación
- **Archivo(s)**: [ruta/al/archivo]
- **Línea(s)**: [números de línea]
- **Función/Componente**: [nombre]

#### Causa Raíz (si se identificó)
[Explicación de la causa]

#### Solución Propuesta
[Descripción de cómo arreglarlo]

#### Evidencia
```
[Logs, screenshots, stack traces, etc.]
```

#### Relacionado
- Feature: [id de feature en feature_list.json]
- Otros bugs: [referencias]
```

---

## Bugs Reportados

### Ejemplo (borrar al usar)

### 1 - Error en validación de email

**Fecha**: 2026-05-01
**Severidad**: 🟠 Alta
**Agente**: TESTER/DEBUGGER
**Estado**: Pending

#### Descripción
La validación de email en el formulario de registro no acepta emails válidos con caracteres especiales.

#### Pasos para Reproducir
1. Ir a /register
2. Ingresar email: "user+test@example.com"
3. Enviar formulario

#### Comportamiento Esperado
El email debería ser aceptado como válido.

#### Comportamiento Actual
Muestra error "Email inválido".

#### Ubicación
- **Archivo(s)**: `src/utils/validation.ts`
- **Línea(s)**: 45-50
- **Función/Componente**: `validateEmail()`

#### Causa Raíz
La regex utilizada no permite caracteres especiales como `+` en la parte local del email.

#### Solución Propuesta
Actualizar la regex para seguir RFC 5322 o usar validator.js.

#### Evidencia
```
Error: Email inválido
Input: user+test@example.com
Regex actual: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
```

---

## Formato para Actualización de Estado

```markdown
### [Número] - [Título Breve] - ACTUALIZACIÓN

**Fecha**: [YYYY-MM-DD]
**Estado**: Fixed / In Progress / Won't Fix
**Agente que arregló**: [Rol]
**Commit**: [hash del commit si aplica]

#### Resolución
[Descripción de cómo se arregló]

#### Verificación
- [x] Test unitario agregado
- [x] Test manual pasado
- [x] Code review aprobado
```

---

*Esta es una plantilla genérica para workflow-harness*
