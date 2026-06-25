---
name: frosted-glass-design
description: Diseño web con estética Frosted Glass / Glassmorphism. Usar cuando el usuario quiere interfaces con efecto vidrio esmerilado, transparencias, blur de fondo, capas flotantes y sensación de profundidad moderna. Ideal para dashboards, apps web, landing pages premium y paneles de control.
---

# SKILL: Frosted Glass / Glassmorphism Design

## Concepto

El **Glassmorphism** simula superficies de vidrio esmerilado flotando sobre fondos con color o gradiente. La clave es la ilusión de profundidad: el contenido parece estar detrás del vidrio, el fondo se desenfoca, y las capas crean jerarquía visual sin bordes agresivos.

Referentes: macOS Big Sur, iOS, Windows 11, apps de finanzas modernas.

---

## Reglas de Diseño

### Fondo (obligatorio)
El frosted glass **no funciona sin un fondo interesante**. Siempre usar:
- Gradiente mesh vibrante (azul, violeta, teal, coral)
- Imagen borrosa de alta saturación
- Formas geométricas grandes con blur extremo como background

```css
body {
  background: linear-gradient(135deg, #1a1a4e 0%, #6c3fa0 40%, #00c9a7 100%);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* Orbes de color en el fondo */
body::before, body::after {
  content: '';
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
  z-index: 0;
}
body::before {
  width: 500px; height: 500px;
  background: #a855f7;
  top: -100px; left: -100px;
}
body::after {
  width: 400px; height: 400px;
  background: #06b6d4;
  bottom: -80px; right: -80px;
}
```

### Card / Panel de Vidrio
```css
.glass-card {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 20px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
  padding: 2rem;
}
```

### Variantes de intensidad
| Nivel | `background` | `blur` | Uso |
|-------|-------------|--------|-----|
| Sutil | `rgba(255,255,255,0.08)` | `blur(10px)` | Fondo de sección |
| Normal | `rgba(255,255,255,0.14)` | `blur(20px)` | Cards principales |
| Fuerte | `rgba(255,255,255,0.22)` | `blur(30px)` | Modales, nav activo |
| Dark glass | `rgba(0,0,0,0.35)` | `blur(20px)` | Overlays oscuros |

---

## Paleta de Color

```css
:root {
  /* Fondos */
  --bg-gradient: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  
  /* Glass */
  --glass-bg: rgba(255, 255, 255, 0.1);
  --glass-border: rgba(255, 255, 255, 0.2);
  --glass-shadow: rgba(0, 0, 0, 0.3);
  
  /* Texto sobre vidrio */
  --text-primary: #ffffff;
  --text-secondary: rgba(255, 255, 255, 0.7);
  --text-muted: rgba(255, 255, 255, 0.45);
  
  /* Acentos */
  --accent-primary: #a78bfa;   /* violeta suave */
  --accent-secondary: #34d399; /* teal/verde */
  --accent-warm: #f472b6;      /* rosa */
}
```

---

## Tipografía

Usar fuentes limpias y modernas que no peleen con la transparencia:
- Display: `Outfit`, `Sora`, `Plus Jakarta Sans`
- Body: `DM Sans`, `Nunito`
- Monospace (datos): `JetBrains Mono`

```html
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
```

---

## Componentes Clave

### Navbar flotante
```css
.navbar {
  position: fixed;
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  max-width: 900px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 50px;
  padding: 0.75rem 1.5rem;
  z-index: 100;
}
```

### Botón primario
```css
.btn-glass {
  background: rgba(167, 139, 250, 0.3);
  border: 1px solid rgba(167, 139, 250, 0.5);
  color: #fff;
  padding: 0.6rem 1.4rem;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.25s ease;
  backdrop-filter: blur(10px);
}
.btn-glass:hover {
  background: rgba(167, 139, 250, 0.5);
  box-shadow: 0 0 20px rgba(167, 139, 250, 0.4);
  transform: translateY(-1px);
}
```

### Input
```css
.glass-input {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #fff;
  padding: 0.75rem 1rem;
  outline: none;
  transition: border-color 0.2s;
}
.glass-input:focus {
  border-color: rgba(167, 139, 250, 0.7);
  background: rgba(255, 255, 255, 0.1);
}
```

---

## Animaciones Recomendadas

```css
/* Entrada de cards */
@keyframes glassReveal {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.97);
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
    backdrop-filter: blur(20px);
  }
}
.glass-card {
  animation: glassReveal 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Hover shimmer */
.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.08) 50%, transparent 60%);
  background-size: 200% 100%;
  opacity: 0;
  transition: opacity 0.3s;
}
.glass-card:hover::before {
  opacity: 1;
  animation: shimmer 0.6s ease;
}
@keyframes shimmer {
  from { background-position: 200% center; }
  to   { background-position: -200% center; }
}
```

---

## Anti-patrones a Evitar

- ❌ Usar `backdrop-filter` sobre fondo blanco o negro sólido (no se ve nada)
- ❌ Cards completamente opacas dentro de layouts glassmorphism
- ❌ Demasiadas capas de blur anidadas (performance hit)
- ❌ Texto gris oscuro sobre vidrio claro (bajo contraste)
- ❌ Bordes sin ningún alpha (rompen la ilusión de vidrio)

---

## Compatibilidad

```css
/* Fallback para navegadores sin backdrop-filter */
@supports not (backdrop-filter: blur(1px)) {
  .glass-card {
    background: rgba(30, 20, 60, 0.85);
  }
}
```

---

## Casos de Uso Ideales

- Dashboards financieros / crypto
- Landing pages de productos tech
- Apps de música / streaming
- Paneles de autenticación (login / register)
- Widgets de métricas y KPIs
- Portfolios creativos
