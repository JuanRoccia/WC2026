# Changelog — Roles y Permisos Multi-Tenant

> Registro de cambios funcionales. NO es un log de commits.
> Cada entrada describe un cambio en el COMPORTAMIENTO esperado del módulo.

## [1.2.0] - 2026-05-16

### Added
- REQ-05: Auditoría de cambios en roles. Ahora toda modificación en roles,
  asignaciones y permisos queda registrada en un log inmutable.
- Escenario: eliminación de rol con re-asignación automática a "sin-roles".

### Changed
- REQ-03: El deny a nivel de tenant ahora prevalece sobre permisos de rol,
  incluso para super-admins. Antes los super-admins podían bypassar denies.

## [1.1.0] - 2026-05-10

### Added
- REQ-04: Roles por defecto en creación de tenant ("owner" asignado
  automáticamente).
- Regla de negocio: no se puede eliminar rol "owner" con usuarios activos.

### Changed
- REQ-01: Se aclaró que el error 403 NO debe exponer si el tenant B existe.
  (Antes devolvía "tenant not found", ahora es "forbidden" genérico).

## [1.0.0] - 2026-05-01

### Added
- REQ-01: Aislamiento de roles por tenant.
- REQ-02: Asignación de roles a usuarios con herencia.
- REQ-03: Permisos deny con precedencia sobre allow.
- Contratos de API: POST /roles, GET /permissions.
- Reglas de negocio iniciales (20 roles máx, naming único por tenant).

### Decisions
- Se eligió deny explícito en vez de ACL negativas (ver decisions.md).
- Límite de 50 roles por tenant como constraint inicial.
