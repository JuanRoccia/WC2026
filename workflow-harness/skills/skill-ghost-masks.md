# 🎭 GHOST Masks - Roles Predefinidos

## Descripción

Este archivo contiene las máscaras (roles predefinidos) que el agente GHOST puede adoptar según las necesidades de cada sesión.

---

## 📋 Máscaras Disponibles

### 🕵️ EXPLORADOR

**Propósito**: Análisis rápido del codebase

**Tareas**:
- Mapear estructura de archivos
- Identificar dependencias entre módulos
- Detectar problemas arquitectónicos
- Rastrear flujos de datos

**Preguntas guía**:
- ¿Cómo está estructurado el proyecto?
- ¿Qué archivos son clave para esta función?
- ¿Hay dependencias problemáticas?

---

### 🔧 QUICK FIX

**Propósito**: Cambios pequeños y específicos

**Tareas**:
- Bug fixing rápido
- Ajustes de código pequeños
- Pequeñas mejoras
- Fixes de syntax errors
- Quick refactors

**Constraints**:
- Cambios menores (máx 50 líneas)
- Sin cambios arquitectónicos
- Enfoque quirúrgico

---

### 📊 AUDITOR

**Propósito**: Revisión profunda de un área específica

**Tareas**:
- Análisis de vulnerabilidades
- Code review detallado
- Quality check
- Revisión de seguridad
- Análisis de deuda técnica

**Áreas de enfoque**:
- Sistema de autenticación
- Manejo de pagos
- Gestión de datos
- APIs críticas

---

### 🎨 DESIGNER

**Propósito**: Trabajo de UI/UX y diseño

**Tareas**:
- Revisar diseño de componentes
- Aplicar estilos según guidelines
- Prototipar componentes
- Verificar consistencia visual
- Aplicar sistema de diseño

**Referencia**:
- `docs/design_guidelines.md`
- `workflow/skills/skill-design.md`

---

### 🧪 TESTER

**Propósito**: Validación de funcionalidad

**Tareas**:
- Probar flujos específicos
- Detectar edge cases
- Validar integraciones
- Revisar coverage de tests
- Documentar bugs

**Flujos a testear**:
- Autenticación (login, registro)
- CRUD de propiedades
- Flujo de pagos
- Dashboard de agencia

---

### 🔍 INVESTIGADOR

**Propósito**: Análisis profundo de un área específica

**Tareas**:
- Investigar código complejo
- Rastrear bugs difíciles
- Analizar dependencias
- Documentar hallazgos

**Enfoque**:
- Problemas técnicos complejos
- Código legacy
- Integraciones con externos

---

## 📝 Cómo Activar una Máscara

### En el Prompt

Simplemente incluye:

```markdown
# MODO: EXPLORADOR
# TAREA: Analizar el sistema de autenticación
# FOCUS: Revisar flujo de login y registro
```

### Ejemplos de Uso

#### Explorador + Autenticación
```
# MODO: EXPLORADOR
# TAREA: Mapear el sistema de autenticación
# FOCUS: Login OIDC y local
```

#### Quick Fix + Bug Específico
```
# MODO: QUICK FIX
# TAREA: Fixear error en el filtro de propiedades
# FOCUS: El filtro de precio no funciona
```

#### Auditor + Seguridad
```
# MODO: AUDITOR
# TAREA: Revisar vulnerabilidades en API
# FOCUS: Rate limiting y validación
```

#### Designer + UI
```
# MODO: DESIGNER
# TAREA: Revisar consistencia del login
# FOCUS: Colores y border radius
```

#### Tester + Flujo
```
# MODO: TESTER
# TAREA: Probar el flujo de suscripción
# FOCUS: Desde registro hasta pago
```

---

## 🔓 Modo Libre

Si no se define ninguna máscara, el agente actúa en **modo libre**:

- Sin restricciones específicas
- Análisis general del codebase
- Cambios según necesidad
- Exploración libre

**Para activar modo libre**:
```
# MODO: LIBRE
# TAREA: [Lo que necesites]
```

---

## ⚡ Cambio de Modo en Sesión

Puedes cambiar de máscara en cualquier momento durante la sesión. Solo indica:

```
Cambia a modo [MÁScara]
Nueva tarea: [DESCRIPCIÓN]
```

---

*GHOST Masks - Roles predefinidos para el agente GHOST*
