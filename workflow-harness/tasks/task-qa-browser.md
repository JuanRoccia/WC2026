# Tareas Específicas: QA BROWSER

## Objetivo Principal
Validar que la aplicación funciona correctamente desde la perspectiva del usuario final,
detectando bugs visuales, errores de consola, y flujos rotos antes de marcar features como `done`.

---

## TASK-QA-001 — Smoke Test

Verificar que la aplicación responde y carga correctamente.

### Pasos
1. Abrir `${APP_URL}` en viewport desktop 1280px
2. Verificar que la landing page carga sin errores
3. Screenshot del estado inicial
4. Consultar `GET /api/health` — debe responder 200
5. Verificar que no hay errores de consola JS

### Checkpoints
- [ ] Landing page carga sin pantalla en blanco
- [ ] Health endpoint responde 200
- [ ] Sin errores de consola (TypeError, 404, CORS)
- [ ] Screenshot tomado

---

## TASK-QA-002 — Registro + Login

Probar el flujo completo de autenticación.

### Pasos
1. Abrir `${APP_URL}`
2. Localizar botón de registro ("Crear cuenta", "Probá gratis", "Empezar")
3. Screenshot del formulario antes de interactuar (sin bordes rojos)
4. Intentar enviar sin datos → verificar validación
5. Completar con datos válidos: email único (usar timestamp), password
6. Screenshot antes de enviar
7. Enviar y verificar resultado
8. Hacer logout
9. Login con las credenciales creadas
10. Screenshot post-login

### Checkpoints
- [ ] Botón de registro visible y funcional
- [ ] Formulario sin errores en estado inicial
- [ ] Validación en español (o idioma del proyecto)
- [ ] Registro exitoso sin error 500
- [ ] Login post-registro funciona
- [ ] Logout destruye sesión

---

## TASK-QA-003 — CRUD Entidad Principal

Crear, visualizar, editar y eliminar la entidad principal del proyecto.

### Pasos
1. Login con credenciales válidas
2. Navegar al formulario de creación
3. Screenshot del formulario vacío
4. Completar campos requeridos
5. Screenshot del formulario completo
6. Enviar y verificar creación
7. Screenshot del resultado
8. Editar la entidad creada
9. Verificar que los cambios persisten
10. Eliminar la entidad (si aplica)

### Checkpoints
- [ ] Formulario de creación accesible
- [ ] Validación de campos obligatorios funciona
- [ ] Creación exitosa sin errores
- [ ] Edición guarda cambios correctamente
- [ ] Consola sin errores durante todo el flujo

---

## TASK-QA-004 — Testing Mobile (375px)

Repetir flujos críticos en viewport móvil.

### Pasos generales
Para cada flujo de TASK-QA-001 a TASK-QA-003:
1. Cambiar viewport a 375x812
2. Repetir los mismos pasos
3. Documentar diferencias vs desktop

### Checkpoints específicos mobile
- [ ] Menú de navegación responsive funcional (hamburguesa → drawer)
- [ ] Formularios usables con teclado táctil (sin zoom forzado)
- [ ] Botones de ancho completo, sin overflow horizontal
- [ ] Landing/hero visible correctamente

---

## TASK-QA-005 — Admin Panel (si aplica)

Verificar el panel de administración.

### Pasos
1. Login como admin
2. Ir al dashboard de administración
3. Screenshot del dashboard con stats
4. Verificar navegación entre secciones
5. Probar gestión de usuarios/entidades (CRUD)

### Checkpoints
- [ ] Panel de admin carga correctamente
- [ ] Stats son valores reales (no hardcodeados)
- [ ] CRUD de gestión funciona

---

## TASK-QA-006 — Regresión Rápida Post-Deploy

Smoke test de 10 minutos para verificar que nada se rompió tras un deploy.

### Pasos
1. Landing carga → screenshot
2. Login exitoso → screenshot
3. Dashboard carga con datos → screenshot
4. Crear entidad mínima (verificar que no hay error 500)
5. Logout → screenshot
6. Verificar `/api/health` → 200

### Criterio de PASS/FAIL
- PASS: todos los pasos sin error, consola sin errores críticos
- FAIL: cualquier error 500, pantalla en blanco, o loop de auth

---

## Formato de Reporte

Usar el formato definido en `agents/07-qa-browser.md` (sección "Formato de reporte").
Incluir health score, screenshots, y pasos de reproducción para cada bug.

---

*Última actualización: Junio 2026*
