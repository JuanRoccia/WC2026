# Convenciones de código y documentación

> Homogeneidad extrema. La IA predice mejor cuando el repositorio se parece
> a sí mismo en todas partes.

## Estilo Markdown

- **Formato:** Markdown estándar con GFM (GitHub Flavored Markdown).
- **Líneas:** máximo 100 caracteres cuando sea posible.
- **Encabezados:** `#` para título principal, `##` para secciones, `###` para subsecciones.
- **Listas:** usar `-` para listas no ordenadas, números para ordenadas.
- **Código:** usar backticks `` ` `` para inline, triple backticks con lenguaje para bloques.

## Nombres de archivos

| Tipo                    | Convención        | Ejemplo               |
|-------------------------|-------------------|-----------------------|
| Agentes                 | `NN-nombre.md`   | `01-arquitecto.md`    |
| Tareas                  | `task-nombre.md`  | `task-arquitecto.md`  |
| Skills                  | `skill-nombre.md` | `skill-design.md`     |
| Documentos workflow     | `UPPER-KEBAB.md` | `AGENTS.md`           |
| Configuración           | `.lowercase`      | `.workflow-config.json`|
| JSON estructurado       | `lowercase.json`  | `feature_list.json`   |

## Estructura de archivos Markdown

Todo archivo MD en `agents/` y `tasks/` empieza con:

```markdown
# [TÍTULO DEL ROL/TAREA]

## Contexto

[Descripción breve]

## Responsabilidades

- [lista de responsabilidades]
```

## JSON

- **Formato:** JSON estándar con 2 espacios de indentación.
- **Strings:** comillas dobles `"..."` siempre.
- **Keys:** camelCase para datos dinámicos, snake_case para metadatos.
- **Arrays:** uno por línea con coma final (trailing comma no permitida en JSON).

Ejemplo `feature_list.json`:
```json
{
  "project": "workflow-harness",
  "features": [
    {
      "id": 1,
      "name": "init_script",
      "status": "done"
    }
  ]
}
```

## Bash Scripting (init.sh)

- **Shebang:** `#!/usr/bin/env bash`
- **Set:** `set -u` (tratar variables no definidas como error).
- **Colores:** usar variables para códigos de escape ANSI.
- **Funciones:** definir `ok()`, `warn()`, `fail()`, `info()` para consistencia.
- **Validaciones:** verificar existencia de archivos/directorios antes de operar.

## Tests

- Un archivo de test por módulo: `tests/test_<modulo>.py`.
- Nombres descriptivos: `test_init_sh_verifies_structure`.
- Tests usan `tempfile` o directorios temporales, limpian tras de sí.

## Manejo de errores

Scripts y archivos de configuración validan:

```bash
if [ ! -f "$archivo" ]; then
  fail "Falta archivo: $archivo"
  exit 1
fi
```

```json
{
  "error": "mensaje descriptivo",
  "code": "ERROR_CODE"
}
```

## Comentarios

Por defecto **no** se escriben en archivos de documentación. Solo en código
cuando explican un *por qué* no obvio. Los nombres deben hacer el resto.

## Git

- **Commits:** mensajes descriptivos en imperativo ("Crea init.sh", no "Creado init.sh").
- **.gitignore:** excluir `progress/`, archivos temporales, y secretos.
- **Ramas:** no crear ramas para el harness, trabajar en main o usar PRs.
