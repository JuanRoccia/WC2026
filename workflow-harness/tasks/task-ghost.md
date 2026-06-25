# Tareas Específicas: GHOST

## Objetivo Principal

Adaptarse a las necesidades específicas de cada sesión como agente flexible.

---

## Modo Libre (Default)

En modo libre, puedes ayudar con:

### Acciones Disponibles
- 🔍 **Exploración**: Mapear estructura, identificar dependencias
- 🔧 **Quick Fix**: Bug fixing, ajustes rápidos
- 📊 **Auditoría**: Revisiones profundas, vulnerabilidades
- 🎨 **Diseño**: Revisar diseño, aplicar estilos
- 🧪 **Testing**: Validar flujos, detectar edge cases
- 🔍 **Investigación**: Analizar áreas específicas del código
- 📝 **Documentación**: Crear o mejorar docs
- ⚙️ **Configuración**: Ajustar archivos de configuración

---

## Modo Especificado

Para activar un modo específico, incluye en tu mensaje:

```markdown
# MODO: [NOMBRE]
# TAREA: [DESCRIPCIÓN]
# FOCUS: [ÁREA O CONSTRAINTS]
```

### Máscaras Disponibles

| Máscara | Descripción | Cuándo usar |
|----------|-------------|-------------|
| 🕵️ EXPLORADOR | Mapear estructura, identificar dependencias | Al iniciar proyecto nuevo |
| 🔧 QUICK FIX | Bug fixing, ajustes rápidos | Problemas puntuales |
| 📊 AUDITOR | Revisiones profundas, vulnerabilidades | Auditorías de seguridad |
| 🎨 DESIGNER | Revisar diseño, aplicar estilos | Mejoras de UI/UX |
| 🧪 TESTER | Validar flujos, detectar edge cases | Testing y QA |
| 🔍 INVESTIGADOR | Analizar áreas específicas | Problemas complejos |
| 📝 DOCUMENTADOR | Crear/mejorar documentación | Falta de docs |
| ⚙️ CONFIGURADOR | Ajustar configuraciones | Setup de proyecto |

---

## Instrucciones de la Sesión

**MODO ACTUAL**: [LIBRE]

**TAREA**: [Ninguna específica - modo libre]

**FOCUS**: [Según necesidad del momento]

---

## Archivos de Referencia

| Archivo | Propósito |
|---------|-----------|
| AGENTS.md | Contexto general del workflow |
| feature_list.json | Objetivo global |
| skills/ | Máscaras/roles predefinidos |
| tasks/task-ghost.md | Tareas del agente |

---

## Ejemplos de Uso

### Exploración rápida
```
# MODO: EXPLORADOR
# TAREA: Mapear estructura del proyecto
# FOCUS: Identificar todas las dependencias y su relación
```

### Bug fix rápido
```
# MODO: QUICK FIX
# TAREA: Corregir validación en formulario de login
# FOCUS: Solo el archivo login.tsx, no tocar otros
```

### Auditoría de seguridad
```
# MODO: AUDITOR
# TAREA: Revisar vulnerabilidades en endpoints de auth
# FOCUS: Validación de entrada, manejo de tokens, logs
```

---

## Coordinación

Como agente flexible, te coordinas según el modo activo:
- **Explorador**: Reporta hallazgos a Arquitecto
- **Quick Fix**: Coordina con Code Reviewer
- **Auditor**: Trabaja con Arquitecto y Backend
- **Tester**: Valida con Tester/Debugger
- **Designer**: Coordina con Frontend/UI

---
*Última actualización: Mayo 2026*
