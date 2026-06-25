# TESTING-MANUAL.md — Guía de Testing Manual

> Este documento proporciona una guía genérica para realizar testing manual
> de cualquier proyecto gestionado con este workflow.

---

## Objetivo

Documentar el proceso de testing manual para validar funcionalidades críticas antes de marcar una feature como `done`.

---

## Preparación

### 1. Verificar Entorno
```bash
./init.sh
```
Debe terminar sin errores.

### 2. Leer Documentación
- `AGENTS.md` - Entender el workflow
- `tasks/task-[rol].md` - Tareas asignadas
- `docs/verification.md` - Criterios de verificación

### 3. Preparar Datos de Prueba
- Identificar qué datos se necesitan
- Crear datos de prueba en archivo separado si es necesario
- No usar datos reales de producción

---

## Flujo de Testing Manual

### Paso 1: Identificar Funcionalidades Críticas
Según la feature en desarrollo, identifica:
- Flujos principales (happy path)
- Flujos alternativos
- Casos de error esperados
- Edge cases

### Paso 2: Crear Matriz de Testing

| ID | Funcionalidad | Pasos | Datos | Esperado | Actual | Estado |
|----|----------------|-------|------|----------|--------|--------|
| TC01 | [Nombre] | 1,2,3 | [Datos] | [Resultado] | [Actual] | ✅/❌ |

### Paso 3: Ejecutar Casos de Prueba

#### Ejemplo: Login
```
TC01 - Login con credenciales válidas
1. Ir a /login
2. Ingresar email: test@example.com
3. Ingresar password: Test123!
4. Hacer click en "Iniciar Sesión"
→ Esperado: Redirección a /dashboard
→ Actual: [Completar]
→ Estado: [✅/❌]
```

### Paso 4: Documentar Resultados

#### Formato de Reporte
```markdown
## Reporte de Testing Manual - [Feature Nombre]

**Fecha**: [YYYY-MM-DD]
**Agente**: [Rol]
**Feature**: [id en feature_list.json]
**Entorno**: [Dev/Staging/Prod]

### Resumen
- Total casos: X
- Exitosos: Y
- Fallidos: Z
- Bloqueantes: W

### Casos Fallidos
[Detallar cada caso fallido con screenshots/logs]

### Bugs Encontrados
[Referencia a BUGS-REPORT.md]

### Recomendaciones
[Mejoras sugeridas]
```

---

## Áreas Críticas a Testear (Genérico)

### 1. Autenticación y Autorización
- [ ] Registro de usuario nuevo
- [ ] Login con credenciales válidas
- [ ] Login con credenciales inválidas
- [ ] Recuperación de contraseña
- [ ] Logout
- [ ] Refresh token
- [ ] Permisos por rol

### 2. CRUD Principal
- [ ] Crear entidad (todos los campos)
- [ ] Crear entidad (campos mínimos)
- [ ] Crear con datos inválidos (validación)
- [ ] Editar entidad
- [ ] Eliminar entidad (con confirmación)
- [ ] Listar entidades (paginación/filtros)

### 3. Integraciones Externas (si aplica)
- [ ] Webhook handlers
- [ ] APIs externas
- [ ] Pasarelas de pago
- [ ] Manejo de timeouts

### 4. UI/UX
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Accesibilidad (keyboard nav, ARIA labels)
- [ ] Loading states
- [ ] Error states
- [ ] Empty states
- [ ] Formularios (validación en tiempo real)

### 5. Seguridad
- [ ] SQL/NoSQL injection
- [ ] XSS
- [ ] CSRF
- [ ] Rate limiting
- [ ] Headers de seguridad

---

## Checklist de Cierre

Antes de marcar una feature como `done`:

- [ ] Todos los casos de prueba pasaron
- [ ] Bugs críticos han sido corregidos
- [ ] Se actualizó `progress/current.md`
- [ ] Se ejecutó `./init.sh` sin errores
- [ ] La feature está documentada
- [ ] No hay comentarios `TODO` sin contexto

---

## Tips para Testing Manual

1. **Usa datos realistas** pero no reales
2. **Documenta todo** con screenshots/logs
3. **Prueba casos edge** (valores límite, caracteres especiales)
4. **Verifica en diferentes navegadores** (si es web)
5. **Prueba conectividad intermitente** (si aplica)
6. **Usa herramientas de desarrollo** (DevTools, Postman, etc.)

---

## Herramientas Recomendadas

- **Browser DevTools** - Para debugging frontend
- **Postman/Insomnia** - Para testing de APIs
- **SQLite Browser** - Para inspeccionar base de datos local
- **curl/httpie** - Para requests rápidos desde terminal

---

*Guía genérica adaptada para workflow-harness*
