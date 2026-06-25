# Tareas Específicas: CODE REVIEWER

## Objetivo Principal

Asegurar la calidad del código en todo el proyecto mediante revisión sistemática.

---

## Tareas Asignadas

### 🔴 Prioridad Crítica

#### 1. Revisión de Seguridad
**Tareas específicas**:
1.1 **Validación de entrada**
- Ubicación: APIs/endpoints
- Acción: Verificar schemas de validación (Zod, Joi, etc.)
- Cobertura: todos los inputs de usuario

1.2 **Manejo de autenticación/sesiones**
- Ubicación: middleware de auth
- Acción: Revisar tokens, cookies, headers
- Verificar: expiración, renovación, logout

1.3 **Exposición de datos sensibles**
- Ubicación: respuestas de API, logs, errores
- Acción: Verificar que no se filtren secrets/passwords
- Revisar: stack traces, mensajes de error

---

### 🟠 Prioridad Alta

#### 2. Calidad de Código

**Tareas específicas**:
2.1 **Anti-patterns**
- Identificar código duplicado
- Detectar god classes/functions
- Revisar principio de responsabilidad única

2.2 **Manejo de errores**
- Verificar try/catch apropiados
- Revisar propagación de errores
- Validar mensajes de error

2.3 **Performance**
- N+1 queries
- Bucles innecesarios
- Carga excesiva de datos

---

### 🟡 Prioridad Media

#### 3. Estándares y Convenciones

3.1 **Estilo de código**
- Lint pasando
- Formato consistente
- Nombres descriptivos

3.2 **Documentación**
- JSDoc/TSDoc/Python docstrings
- README actualizado
- Comentarios útiles (no obvios)

---

## Archivos Clave a Revisar

| Archivo | Propósito |
|---------|-----------|
| Entry point | Archivo principal |
| Auth | Configuración de autenticación |
| Routes/API | Endpoints y rutas |
| Storage/DB | Operaciones de base de datos |
| Middleware | Middleware y utilidades |
| Components | Componentes UI (si aplica) |

---

## ✅ Checklist de Entregable

- [ ] Revisión de seguridad completada
- [ ] Anti-patterns identificados
- [ ] Performance revisada
- [ ] Estándares verificados
- [ ] Reporte generado

---

## Coordinación con Otros Agentes

- **Arquitecto**: Valida hallazgos que requieran decisiones arquitectónicas
- **Backend/Frontend**: Comunica hallazgos para corrección
- **Tester**: Valida bugs encontrados

---
*Última actualización: Mayo 2026*
