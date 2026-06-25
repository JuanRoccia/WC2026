---
# Módulo: [NOMBRE]

> **Estado**: draft | active | deprecated
> **Versión**: 0.1.0
> **Última revisión**: [FECHA]
> **Propietario**: [agente o humano responsable]

## Descripción

[Una o dos frases: qué hace este módulo, cuál es su responsabilidad principal.]

## Requisitos

### REQ-01: [Nombre del requisito]

El sistema SHALL [comportamiento esperado, específico y verificable].

#### Escenario: [Nombre]

- DADO [contexto/estado inicial]
- CUANDO [acción o evento]
- ENTONCES [resultado esperado]
- Y [consecuencias adicionales si aplica]

#### Escenario: [Edge case]

- DADO [contexto de edge case]
- CUANDO [acción]
- ENTONCES [comportamiento esperado en el edge]

### REQ-02: [Nombre del requisito]

[repetir estructura para cada requisito]

## Contratos de API (si aplica)

### [Nombre del endpoint o función]

**Entrada**: [descripción o schema simplificado]
**Salida**: [descripción o schema simplificado]
**Errores esperados**: [lista de errores y cuándo ocurren]

## Reglas de negocio

- [Regla 1: invariante que siempre debe cumplirse]
- [Regla 2]

## Dependencias de otros módulos

- `specs/[otro-modulo]/` — [por qué depende]

## Lo que este módulo NO hace

- [Exclusión explícita 1]
- [Exclusión explícita 2]
