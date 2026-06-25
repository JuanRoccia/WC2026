# Tareas Específicas: BACKEND

## Objetivo Principal

Desarrollo y mejora de APIs, base de datos, e integración con servicios externos.

---

## Tareas Asignadas

### 🔴 Prioridad Crítica

#### 1. Mejora de Sistemas de Integración

**Tareas específicas**:
1.1 **Revisar endpoints de suscripción/pagos**
- POST /api/subscriptions/create-checkout
- POST /api/subscriptions/portal
- Manejo de errores

1.2 **Revisar webhook handler**
- Archivo de webhook
- Firma de webhook
- Casos edge (duplicados, retries)

1.3 **Implementar retry logic**
- Pagos exitosos con ventana cerrada
- State management para pagos pendientes

1.4 **Validación server-side**
- Precios contra pasarela
- Plan limits

---

#### 2. Seguridad de APIs

**Tareas específicas**:
2.1 **Rate limiting por endpoint**
- Implementar en rutas críticas
- Configurar límites apropiados

2.2 **Validación de entrada**
- Schemas completos (Zod, Joi, etc.)
- Sanitización

2.3 **Manejo de errores**
- No exponer stack traces
- Errores apropiados por tipo

---

### 🟠 Prioridad Alta

#### 3. Optimización de Queries

**Tareas específicas**:
3.1 **Revisar queries en capa de datos**
- N+1 queries
- Faltas de includes/joins

3.2 **Revisar índices**
- Foreign keys
- Campos filtrados frecuentemente

3.3 **Pagination**
- offset/limit vs cursor
- Default limits razonables

---

#### 4. Endpoints CRUD

**Tareas específicas**:
4.1 **Recursos principales**
- GET/POST/PUT/DELETE
- Validación de límites por plan

4.2 **Relaciones**
- Recursos padre/hijo
- Queries optimizadas

---

### 🟡 Prioridad Media

#### 5. Documentación de APIs

**Tareas específicas**:
5.1 **JSDoc/Comentarios en endpoints**
- Descripción
- Parámetros
- Respuestas

5.2 **Errores documentados**
- Códigos de error
- Mensajes

---

#### 6. Middleware y Utilidades

**Tareas específicas**:
6.1 **Revisar middleware existente**
- Logger
- Rate limit
- Status checks

6.2 **Agregar health check**
- GET /api/health
- DB connection check

---

## Archivos a Revisar

| Prioridad | Archivos |
|-----------|----------|
| Crítica | webhook handler, routes (subs) |
| Alta | storage/queries, routes |
| Media | middleware/*.ts/py |

---

## ✅ Checklist de Entregable

- [ ] Mejoras implementadas en sistema de pagos
- [ ] Rate limiting configurado
- [ ] Queries optimizadas identificadas
- [ ] Endpoints CRUD revisados
- [ ] Health check implementado
- [ ] Documentación de APIs

---

## Coordinación con Otros Agentes

- **Arquitecto**: Decisiones técnicas de seguridad
- **Code Reviewer**: Calidad de código
- **Frontend**: Necesidades de endpoints
- **Tester**: Validar flujos de API

---

## Formato de Endpoint Review

```markdown
### [Método] /api/[recurso]

**Descripción**:
[Qué hace]

**Validación**:
[Schema]

**Respuestas**:
- 200: ...
- 400: ...
- 401: ...
- 500: ...

**Issues**:
- [Si hay]
```

---
*Última actualización: Mayo 2026*
