# Verificación — Cómo demostrar que el trabajo funciona

> Regla de oro: **el agente no dice "funciona", lo demuestra**.
> Todo cambio termina con evidencia ejecutable, no con afirmaciones.

## Niveles de verificación

### Nivel 1 — Verificación de estructura (obligatorio)

El harness debe pasar `./init.sh` sin errores:

```bash
bash init.sh
```

Debe terminar con:
```
[OK]    Entorno listo. Puedes empezar a trabajar.
```

### Nivel 2 — Validación de archivos JSON (obligatorio para config)

Todo archivo `.json` debe ser válido:

```bash
python3 -c "import json; json.load(open('feature_list.json'))"
```

`feature_list.json` debe cumplir:
- Tiene array `features` con al menos un elemento.
- Cada feature tiene campos `id`, `name`, `status`.
- Máximo 1 feature en estado `in_progress`.
- Estados válidos: `pending`, `in_progress`, `done`, `blocked`.

### Nivel 3 — Verificación de links en Markdown (recomendado)

Los archivos `.md` no deben tener links rotos a archivos locales:

```bash
grep -r "\[.*\](.*\.md)" . --include="*.md" | while read line; do
  # extraer archivo referenciado y verificar existencia
done
```

### Nivel 4 — Test de integración del workflow (opcional pero recomendado)

Simular un ciclo completo de workflow:

```bash
# 1. Verificar entorno
./init.sh

# 2. Leer AGENTS.md
cat AGENTS.md | head -20

# 3. Cambiar estado de feature en feature_list.json
# (simular inicio de tarea)
python3 -c "
import json
data = json.load(open('feature_list.json'))
data['features'][0]['status'] = 'in_progress'
json.dump(data, open('feature_list.json', 'w'), indent=2)
"

# 4. Verificar que init.sh detecta in_progress
./init.sh

# 5. Revertir cambios
python3 -c "
import json
data = json.load(open('feature_list.json'))
data['features'][0]['status'] = 'done'
json.dump(data, open('feature_list.json', 'w'), indent=2)
"
```

## Anti-patrones (no hacer)

- ❌ "He creado el archivo, debería funcionar." → falta validación ejecutable.
- ❌ JSON que solo se verifica visualmente. → debe validarse con parser.
- ❌ `mock` del filesystem en tests. → usa `tempfile.TemporaryDirectory()` real.
- ❌ Marcar feature como `done` sin pasar `./init.sh`.
- ❌ Editar `progress/history.md` entradas anteriores. → solo append al final.

## Verificación final antes de cerrar sesión

```bash
./init.sh           # debe terminar con [OK] Entorno listo
```

Si `./init.sh` está rojo, **no** marques nada como `done`. Anota el bloqueo
en `progress/current.md` con estado `blocked` en `feature_list.json`.

## Checklist de cierre de sesión

- [ ] `./init.sh` pasa verde.
- [ ] Feature completada marcada como `done` en `feature_list.json`.
- [ ] Resumen de sesión añadido al final de `progress/history.md`.
- [ ] `progress/current.md` vaciado (dejar solo plantilla).
- [ ] No quedan archivos temporales (`*.tmp`, `__pycache__`, etc.).
- [ ] No hay TODOs sin contexto en el código/documentos.
