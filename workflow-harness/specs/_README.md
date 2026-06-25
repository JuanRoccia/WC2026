# specs/ — Contratos funcionales del sistema

> Esta carpeta captura QUÉ debe hacer el sistema, no CÓMO.
> Los agentes la usan como contexto estable de comportamiento esperado.

## ¿Para qué sirve?

El harness sabe orquestar cómo trabajan los agentes (`tasks/`, `agents/`,
`progress/`), pero sin specs cada sesión arranca de cero respecto al
comportamiento esperado del producto.

Las specs resuelven:

- **Contexto persistente**: un agente que vuelve a un módulo después de semanas
  no necesita re-descubrir lo que hacía.
- **Contratos verificables**: cada requisito está expresado como escenarios
  BDD (DADO/CUANDO/ENTONCES).
- **Memoria de decisiones**: `decisions.md` registra por qué se hizo algo,
  no solo qué se hizo.

## ¿Cuándo crear una spec?

Crear una spec nueva cuando un módulo:

1. Tiene más de 2 features o funcionalidades distintas.
2. Es tocado por más de un agente (arquitecto + backend, por ejemplo).
3. Involucra reglas de negocio no triviales (cálculos, permisos, multi-tenant).
4. Tiene integración con terceros (pagos, APIs externas, webhooks).

Un módulo sin spec es aceptable durante exploración/prototyping. Pero en
cuanto entra a producción, necesita spec.

## Estructura

```
specs/
  _template.md       ← copiar para crear specs nuevas
  _README.md         ← este archivo
  example/           ← módulo de ejemplo (no borrar)
    spec.md          ← contratos funcionales
    changelog.md     ← registro de cambios funcionales
    decisions.md     ← ADRs livianos (Architecture Decision Records)
  [modulo]/
    spec.md          ← REQUERIDO: contratos funcionales
    changelog.md     ← RECOMENDADO: delta funcional entre versiones
    decisions.md     ← RECOMENDADO: decisiones técnicas con contexto
```

## Cómo usar el template

1. Copiar `specs/_template.md` a `specs/[modulo]/spec.md`.
2. Rellenar frontmatter: estado, versión, fecha, propietario.
3. Escribir descripción del módulo (1-2 frases).
4. Para cada requisito funcional, crear un REQ-XX con escenarios BDD.
5. Si el módulo expone APIs, documentar contratos (entrada/salida/errores).
6. Enumerar reglas de negocio invariantes.
7. Documentar dependencias con otros módulos.
8. Ser explícito sobre lo que el módulo NO hace.

## Formato de escenarios

Usar Gherkin liviano:

```markdown
#### Escenario: [Nombre descriptivo]

- DADO [contexto/estado inicial]
- CUANDO [acción o evento]
- ENTONCES [resultado esperado]
- Y [consecuencias adicionales si aplica]
```

Cada escenario debe ser verificable de forma independiente.

## Changelog: qué registrar

`changelog.md` NO es un log de commits. Registra cambios funcionales:

- Nuevos requisitos agregados
- Comportamiento modificado (y por qué)
- Requisitos deprecados/eliminados
- Cambios en reglas de negocio

Formato:

```markdown
## [vX.Y.Z] - YYYY-MM-DD

### Added
- REQ-04: Soporte para recuperación de contraseña

### Changed
- REQ-02: Límite de intentos cambiado de 3 a 5
```

## Decisions: ADRs livianos

`decisions.md` regista decisiones técnicas con contexto:

```markdown
## [2026-05-16] Usamos PostgreSQL en vez de MongoDB

**Contexto**: Necesitamos transacciones ACID para pagos.
**Opción descartada**: MongoDB no soporta transacciones cross-document
de forma nativa.
**Consecuencia**: Esquema más rígido, pero consistencia fuerte.
```

## Estados de una spec

| Estado | Significado |
|--------|-------------|
| `draft` | En elaboración, puede cambiar sin aviso |
| `active` | Representa el comportamiento actual del módulo |
| `deprecated` | El módulo será eliminado o reemplazado |

Una spec en `draft` por más de 7 días debería promoverse a `active` o
descartarse.

## Principio clave

Las specs capturan COMPORTAMIENTO ESPERADO, no implementación.
Un agente debe poder entender qué hace el módulo sin leer código fuente.
Si necesita leer código para entender la spec, la spec está mal.
