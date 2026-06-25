# Tareas Específicas: TESTER/DEBUGGER

## Objetivo Principal

Asegurar la calidad mediante testing, debugging y documentación técnica.

---

## Tareas Asignadas

### 🔴 Prioridad Crítica

#### 1. Análisis de Cobertura de Tests

**Estado actual**: Identificar tests existentes y gaps

**Tareas específicas**:
1.1 **Mapear tests existentes**
- Ubicación: carpeta tests/
- Acción: Inventario de archivos de test
- Identificar: qué está cubierto y qué no

1.2 **Identificar áreas críticas sin cobertura**
- Autenticación y autorización
- Flujos de pago (si aplica)
- CRUD de recursos principales
- Validaciones de entrada

1.3 **Crear tests faltantes**
- Tests unitarios para lógica de negocio
- Tests de integración para APIs
- Tests E2E para flujos críticos

---

### 🟠 Prioridad Alta

#### 2. Identificación de Edge Cases

**Tareas específicas**:
2.1 **Mapear edge cases no cubiertos**
- Entradas inválidas
- Estados límite
- Condiciones de carrera
- Timeouts y errores de red

2.2 **Documentar casos encontrados**
- Descripción del caso
- Pasos para reproducir
- Resultado esperado vs actual

---

#### 3. Debugging de Problemas

**Tareas específicas**:
3.1 **Reproducir bugs reportados**
- Seguir pasos del reporte
- Identificar causa raíz
- Documentar hallazgos

3.2 **Proponer soluciones**
- Fix propuesto
- Impacto en el sistema
- Tests para prevenir regresión

---

### 🟡 Prioridad Media

#### 4. Documentación Técnica

**Tareas específicas**:
4.1 **Documentar funciones/componentes críticos**
- Propósito y responsabilidad
- Parámetros de entrada
- Retorno esperado
- Edge cases

4.2 **Crear guías de testing**
- Cómo ejecutar tests
- Cómo agregar nuevos tests
- Mejores prácticas

---

## Formato de Reporte

```markdown
## Estado de Testing

### Coverage Actual
- Archivos con tests: X
- Archivos sin tests: Y
- Cobertura estimada: Z%

### Áreas Críticas Sin Cobertura
| Área | Criticidad | Riesgo |
|------|------------|--------|
| ...  | Alta       | ...    |

### Edge Cases Identificados
| Flujo | Edge Case | Prioridad |
|-------|-----------|-----------|
| ...   | ...       | ...       |

### Bugs Encontrados
| Archivo | Descripción | Severidad | Reproducción |
|---------|-------------|-----------|--------------|
| ...     | ...         | 🔴/🟠/🟡  | ...          |
```

---

## ✅ Checklist de Entregable

- [ ] Análisis de cobertura completado
- [ ] Edge cases identificados
- [ ] Bugs documentados
- [ ] Documentación técnica creada
- [ ] Tests faltantes implementados

---

## Coordinación con Otros Agentes

- **Code Reviewer**: Valida bugs encontrados
- **Arquitecto/Backend/Frontend**: Comunica bugs para corrección
- **Ghost**: Soporte en testing específico

---
*Última actualización: Mayo 2026*
