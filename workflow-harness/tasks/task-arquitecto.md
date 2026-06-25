# Tareas Específicas: ARQUITECTO

## Objetivo Principal

Análisis arquitectónico de alto nivel y resolución de problemas técnicos críticos del proyecto.

---

## Tareas Asignadas

### 🔴 Prioridad Crítica

#### 1. Remediación de Vulnerabilidades de Seguridad

**Tareas específicas**:
1.1 **Implementar Rate Limiting**
- Ubicación: archivo de entrada del servidor
- Acción: Instalar y configurar rate limiting
- Límites sugeridos según el proyecto

1.2 **Agregar Headers de Seguridad**
- Ubicación: configuración del servidor
- Acción: Configurar headers (Helmet.js, etc.)
- Headers mínimos: CSP, HSTS, X-Frame-Options

1.3 **Revisar Sesiones**
- Ubicación: configuración de auth
- Acción: Ajustar TTL y configuración de cookies

1.4 **Remover Debug/Logs de Producción**
- Ubicación: archivos de configuración o storage
- Acción: Eliminar o condicionar a entorno dev

---

### 🟠 Prioridad Alta

#### 2. Análisis de Sistemas Críticos

**Tareas específicas**:
2.1 **Revisar flujos de pagos (si aplica)**
- Archivos de integración con pasarelas
- Identificar gaps en el flujo actual

2.2 **Proponer mejoras de robustez**
- Retry logic
- Validación server-side
- Monitoreo

---

### 🟡 Prioridad Media

#### 3. Optimización Arquitectónica

3.1 **Revisar estructura de datos**
- Esquema de base de datos
- Oportunidades de normalización

3.2 **Analizar patrones de API**
- Endpoints y rutas
- Propuestas de mejora REST/GraphQL

3.3 **Evaluar estrategias de cache**
- Cliente y servidor
- Oportunidades de optimización

---

## Archivos Clave a Revisar

| Archivo | Propósito |
|---------|-----------|
| Entry point | Archivo principal del servidor |
| Auth config | Configuración de autenticación |
| Storage/DB | Operaciones de base de datos |
| Routes/API | Endpoints y rutas |
| Webhooks | Integraciones externas |
| Schema | Esquema de base de datos |

---

## ✅ Checklist de Entregable

- [ ] Rate limiting implementado
- [ ] Headers de seguridad configurados
- [ ] Sesiones revisadas
- [ ] Debug/logs de producción removidos
- [ ] Reporte de análisis de sistemas críticos
- [ ] Propuestas de optimización arquitectónica

---

## Coordinación con Otros Agentes

- **Code Reviewer**: Compartirá hallazgos que requieran decisiones arquitectónicas
- **Backend**: Implementará las mejoras técnicas aprobadas
- **Frontend**: Coordinará cambios necesarios en el cliente
- **Tester**: Validará que los cambios funcionen

---
*Última actualización: Mayo 2026*
