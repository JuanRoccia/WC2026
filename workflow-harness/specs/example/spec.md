---
# Módulo: Gestión de Roles y Permisos Multi-Tenant

> **Estado**: active
> **Versión**: 1.2.0
> **Última revisión**: 2026-05-16
> **Propietario**: arquitecto

## Descripción

Gestiona roles, permisos y asignaciones de usuarios en un contexto
multi-tenant. Cada tenant opera de forma aislada: los roles y permisos
de un tenant no son visibles ni aplicables en otro.

## Requisitos

### REQ-01: Aislamiento de roles por tenant

El sistema SHALL garantizar que los roles creados en un tenant solo sean
visibles y asignables dentro de ese tenant.

#### Escenario: Admin crea rol en Tenant A

- DADO que existe un tenant A y un tenant B
- DADO que el usuario "admin" tiene rol super-admin en tenant A
- CUANDO "admin" crea el rol "editor" en tenant A
- ENTONCES el rol "editor" existe en tenant A
- Y NO es visible en tenant B

#### Escenario: Usuario sin permisos intenta listar roles de otro tenant

- DADO un usuario autenticado en tenant A
- CUANDO intenta listar los roles del tenant B vía API
- ENTONCES el sistema rechaza la solicitud con error 403
- Y NO expone información sobre la existencia del tenant B

### REQ-02: Asignación de roles a usuarios

El sistema SHALL permitir asignar múltiples roles a un usuario dentro
de un mismo tenant, con herencia de permisos.

#### Escenario: Asignación de roles acumulativos

- DADO que el rol "visor" tiene permiso `proyecto:leer`
- DADO que el rol "editor" tiene permiso `proyecto:escribir`
- CUANDO se asigna "visor" y "editor" al usuario "maria" en tenant A
- ENTONCES "maria" tiene los permisos `proyecto:leer` y `proyecto:escribir`

#### Escenario: Usuario en múltiples tenants

- DADO que "maria" tiene rol "editor" en tenant A y rol "visor" en tenant B
- CUANDO accede a tenant A
- ENTONCES tiene permisos de "editor"
- CUANDO accede a tenant B
- ENTONCES tiene permisos de "visor"
- Y los permisos de un tenant NO contaminan al otro

### REQ-03: Permisos deny con precedencia

El sistema SHALL garantizar que un permiso explícitamente denegado tenga
precedencia sobre cualquier permiso concedido por herencia de roles.

#### Escenario: Deny override explícito

- DADO que "editor" tiene permiso `proyecto:eliminar`
- DADO que se asigna deny explícito de `proyecto:eliminar` al usuario "juan"
- CUANDO "juan" intenta eliminar un proyecto
- ENTONCES el sistema rechaza la acción
- Y el deny tiene precedencia sobre el permiso heredado del rol

#### Escenario: Deny a nivel de tenant vs usuario

- DADO un deny global en tenant A para `exportar:datos`
- DADO que "admin" tiene rol "super-admin" que concede `exportar:datos`
- CUANDO "admin" intenta exportar datos en tenant A
- ENTONCES la acción es denegada
- Y el deny a nivel tenant prevalece sobre permisos de rol

### REQ-04: Roles por defecto en creación de tenant

El sistema SHALL asignar roles por defecto al crear un nuevo tenant.

#### Escenario: Tenant nuevo tiene admin por defecto

- DADO que se crea un nuevo tenant C
- CUANDO el usuario creador es asignado al tenant
- ENTONCES el usuario recibe el rol "owner" del tenant
- Y el rol "owner" tiene todos los permisos del tenant
- Y el rol "owner" no puede ser eliminado

### REQ-05: Auditoría de cambios en roles

El sistema SHALL registrar toda modificación en roles, asignaciones y
permisos con timestamp, actor y tenant.

#### Escenario: Cambio de rol queda registrado

- DADO que "admin" cambia el rol de "usuario1" de "visor" a "editor"
- CUANDO se consulta el log de auditoría del tenant
- ENTONCES existe un registro con: timestamp, actor="admin",
  acción="role_change", target="usuario1", from="visor", to="editor"

#### Escenario: Eliminación de rol

- DADO que "admin" elimina el rol "visor"
- DADO que "usuario1" tenía asignado "visor"
- CUANDO "usuario1" intenta acceder al sistema
- ENTONCES el sistema le asigna el rol por defecto "sin-roles"
- Y se registra el cambio en el log de auditoría

## Contratos de API

### POST /api/tenants/:tenantId/roles

**Entrada**:
```json
{
  "name": "editor",
  "permissions": ["proyecto:leer", "proyecto:escribir"],
  "extends": null
}
```
**Salida**: `201 Created` con el rol creado.
**Errores**:
- `400` si el nombre ya existe en el tenant
- `403` si el usuario no tiene permiso `roles:crear`
- `422` si el permiso referenciado no existe en el sistema

### GET /api/tenants/:tenantId/users/:userId/permissions

**Entrada**: headers con `X-Tenant-ID` y `Authorization`
**Salida** (200):
```json
{
  "user_id": "uuid",
  "tenant_id": "uuid",
  "roles": ["editor", "visor"],
  "permissions": {
    "proyecto:leer": "allow",
    "proyecto:escribir": "allow",
    "proyecto:eliminar": "deny"
  },
  "inherited_from": {
    "proyecto:leer": "rol:editor",
    "proyecto:eliminar": "deny:directo"
  }
}
```
**Errores**:
- `403` si el usuario no pertenece al tenant
- `404` si el tenant no existe

## Reglas de negocio

- Un rol no puede tener el mismo nombre dentro del mismo tenant.
- Un usuario siempre tiene al menos un rol dentro de un tenant.
- No se puede eliminar el rol "owner" de un tenant mientras existan usuarios
  con ese rol asignado.
- Los permisos deny se almacenan explícitamente, no por ausencia.
- La herencia de permisos es aditiva excepto cuando hay deny explícito.
- El log de auditoría es inmutable: no se puede editar ni eliminar registros.
- Un tenant no puede tener más de 50 roles definidos (límite de negocio).

## Dependencias de otros módulos

- `specs/authn/` — autenticación: el módulo de permisos depende de que
  el usuario esté autenticado y sepa su tenant activo.
- `specs/tenants/` — ciclo de vida de tenants: la creación de un tenant
  debe disparar la asignación de roles por defecto.

## Lo que este módulo NO hace

- No gestiona autenticación (login, logout, sessions, MFA).
- No gestiona el ciclo de vida de tenants (creación, suspensión, eliminación).
- No implementa UI de administración de roles.
- No sincroniza roles entre tenants (cada tenant es independiente).
- No valida que un permiso referenciado exista globalmente (se valida en
  creación, no en asignación).
