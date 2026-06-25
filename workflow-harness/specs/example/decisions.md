# Decisiones Técnicas — Roles y Permisos Multi-Tenant

> ADRs (Architecture Decision Records) livianos.
> Cada entrada documenta una decisión, su contexto, alternativas y consecuencias.

---

## [2026-05-16] Deny explícito en vez de ACL negativas

**Contexto**: Necesitamos que un permiso deny tenga precedencia sobre cualquier
allow. Dos opciones: (1) almacenar denies como entradas separadas en la tabla
de permisos, (2) usar ACL negativas (lista negra global).

**Decisión**: Almacenar denies como entradas separadas con flag
`effect: "deny"`.

**Opción descartada**: ACL negativas. Son más difíciles de auditar, el orden
de evaluación importa, y el modelo mental es más complejo para los agentes
que mantienen el sistema.

**Consecuencia**:
- La evaluación de permisos necesita dos queries: una para allows (por rol)
  y otra para denies (directas del usuario + tenant-level).
- Consistencia simple: deny siempre gana, sin importar orden.
- El log de auditoría es más claro: vemos exactamente qué deny se aplicó.

---

## [2026-05-10] Límite de 50 roles por tenant

**Contexto**: Sin límite, un tenant con cientos de roles degrada performance
de evaluación de permisos (cada request evalúa todos los roles asignados).

**Decisión**: Hard limit de 50 roles por tenant, configurable variable de
entorno `MAX_ROLES_PER_TENANT`.

**Opción descartada**: Límite blando con warning. Agrega complejidad
(threshold, periodic cleanup) sin beneficio claro para el caso de uso actual.

**Consecuencia**:
- Validación en creación de roles: rechazar si se excede el límite.
- Para tenants que necesiten más: excepción vía feature flag.
- El límite es documentado en la spec y en el error message de la API.

---

## [2026-05-01] Log de auditoría en tabla separada (no en JSONB)

**Contexto**: Necesitamos auditoría inmutable de cambios en roles. Opciones:
(1) tabla dedicada `audit_role_changes`, (2) columna JSONB en la tabla de
roles con historial, (3) event sourcing.

**Decisión**: Tabla dedicada con columnas fijas.

**Opción descartada**: JSONB es flexible pero difícil de consultar y auditar.
Event sourcing es overkill para este caso (solo auditoría, no proyecciones).

**Consecuencia**:
- Schema fijo: `actor_id, action, target_type, target_id, old_value, new_value, timestamp, tenant_id`.
- Consultas simples: `SELECT * FROM audit_role_changes WHERE tenant_id = ? ORDER BY timestamp DESC`.
- No hay riesgo de mutación: tabla es insert-only (triggers restringen UPDATE/DELETE).
