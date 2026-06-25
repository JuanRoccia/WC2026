---
name: neobrutalism-design
description: Diseño web con estética Neobrutalism. Usar cuando el usuario quiere interfaces con bordes gruesos negros, sombras offset, colores planos y crudos, tipografía pesada y sensación de diseño intencional, raw y sin pulir. Ideal para startups jóvenes, tools para devs, portfolios llamativos, webs de productos y SaaS con personalidad fuerte.
---

# SKILL: Neobrutalism Design

## Concepto

El **Neobrutalism** es una reacción deliberada contra el diseño pulido y genérico. Toma el brutalismo arquitectónico (raw, sin ocultar la estructura) y lo traslada a la web: bordes negros duros, sombras sin blur, colores planos casi agresivos, y tipografía que no pide permiso.

Referentes: Figma Community (algunos plugins), Linear (versiones tempranas), Gumroad, Cara.app, productos de indie hackers.

---

## Reglas de Diseño

### Principios Fundamentales
1. **Sin border-radius suave** — o 0px, o valores pequeños (4-6px max en bordes, nunca 20px+)
2. **Sombra offset sin blur** — `box-shadow: 4px 4px 0 #000` es la firma del estilo
3. **Bordes negros duros** — `border: 2px solid #000` o `3px solid #000`
4. **Colores planos y crudos** — sin gradientes, sin opacidades, colores 100% sólidos
5. **Tipografía pesada** — weights 700–900, tamaños grandes, sin miedo

---

## Paleta de Color

Neobrutalism trabaja con colores saturados sobre fondos claros o negros:

```css
:root {
  /* Fondos */
  --bg-primary: #FFFBF5;      /* crema/off-white */
  --bg-dark: #0D0D0D;         /* casi negro */
  
  /* Colores de acento (usar 1-2 por proyecto) */
  --yellow: #FFE600;
  --coral: #FF6B6B;
  --mint: #00F5C4;
  --blue: #0057FF;
  --orange: #FF8C00;
  --pink: #FF3CAC;
  --lime: #CCFF00;
  
  /* Estructura */
  --black: #0D0D0D;
  --white: #FFFBF5;
  --border: 2px solid #0D0D0D;
  --shadow: 4px 4px 0px #0D0D0D;
  --shadow-lg: 6px 6px 0px #0D0D0D;
  --shadow-hover: 2px 2px 0px #0D0D0D;
}
```

### Combinaciones de Paleta que Funcionan
| Fondo | Acento | Estilo |
|-------|--------|--------|
| `#FFFBF5` (crema) | `#FFE600` (amarillo) | Energético, startup |
| `#0D0D0D` (negro) | `#CCFF00` (lima) | Dark mode agresivo |
| `#FFFBF5` (crema) | `#0057FF` (azul) | Sólido, confiable |
| `#F0E6FF` (lavanda) | `#FF3CAC` (rosa) | Creativo, femtech |

---

## Tipografía

```html
<!-- Opciones recomendadas -->
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800&family=DM+Mono:wght@500&display=swap" rel="stylesheet">
<!-- Alternativas igual de buenas -->
<!-- Bebas Neue (display), Archivo Black, Syne, Fraunces (serif bold) -->
```

```css
h1, h2, h3 {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

/* Texto decorativo con outline (muy neobrutalist) */
.text-outline {
  -webkit-text-stroke: 2px var(--black);
  color: transparent;
}
```

---

## Componentes Clave

### Card Base
```css
.neo-card {
  background: #FFFBF5;
  border: 2px solid #0D0D0D;
  box-shadow: 4px 4px 0px #0D0D0D;
  border-radius: 4px;
  padding: 1.5rem;
  transition: all 0.15s ease;
}

.neo-card:hover {
  box-shadow: 2px 2px 0px #0D0D0D;
  transform: translate(2px, 2px);
}
```

### Botón Primario
```css
.neo-btn {
  background: #FFE600;
  color: #0D0D0D;
  border: 2px solid #0D0D0D;
  box-shadow: 4px 4px 0px #0D0D0D;
  border-radius: 4px;
  padding: 0.65rem 1.4rem;
  font-weight: 700;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.12s ease;
}

.neo-btn:hover {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0px #0D0D0D;
}

.neo-btn:active {
  transform: translate(4px, 4px);
  box-shadow: none;
}
```

### Botón Outline
```css
.neo-btn-outline {
  background: transparent;
  color: #0D0D0D;
  border: 2px solid #0D0D0D;
  box-shadow: 4px 4px 0px #0D0D0D;
  /* mismo efecto hover que el primario */
}
```

### Input
```css
.neo-input {
  background: #fff;
  border: 2px solid #0D0D0D;
  box-shadow: 3px 3px 0px #0D0D0D;
  border-radius: 4px;
  padding: 0.65rem 1rem;
  font-size: 1rem;
  font-weight: 500;
  outline: none;
  transition: box-shadow 0.12s, transform 0.12s;
}

.neo-input:focus {
  box-shadow: 4px 4px 0px #0057FF;
  border-color: #0057FF;
}
```

### Badge / Tag
```css
.neo-badge {
  display: inline-block;
  background: #FFE600;
  border: 2px solid #0D0D0D;
  border-radius: 4px;
  padding: 0.15rem 0.6rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
```

### Navbar
```css
.neo-navbar {
  background: #FFFBF5;
  border-bottom: 2px solid #0D0D0D;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
```

---

## Layout y Composición

```css
/* Grid neobrutalist con separadores visibles */
.neo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 0; /* Sin gap — los bordes se fusionan */
}

.neo-grid > * {
  border: 2px solid #0D0D0D;
  margin: -1px; /* Overlap borders */
}

/* Sección hero */
.neo-hero {
  background: #FFE600;
  border-bottom: 3px solid #0D0D0D;
  padding: 6rem 2rem;
  position: relative;
}
```

---

## Animaciones

En neobrutalism las animaciones son **abruptas y mecánicas**, no suaves:

```css
/* Hover offset effect */
.neo-card {
  transition: transform 0.1s ease, box-shadow 0.1s ease;
}

/* Bounce de botón */
@keyframes neoPop {
  0%   { transform: scale(1); }
  40%  { transform: scale(0.95) translate(3px, 3px); }
  100% { transform: scale(1); }
}
.neo-btn:active {
  animation: neoPop 0.15s ease;
}
```

---

## Decoraciones Características

```css
/* Líneas decorativas */
.neo-divider {
  border: none;
  border-top: 3px solid #0D0D0D;
  margin: 2rem 0;
}

/* Acento de esquina */
.neo-corner-mark {
  position: absolute;
  top: -2px; right: -2px;
  width: 16px; height: 16px;
  background: #FFE600;
  border: 2px solid #0D0D0D;
}

/* Texto con background highlight */
.neo-highlight {
  background: #FFE600;
  padding: 0 4px;
  border-radius: 2px;
}
```

---

## Anti-patrones a Evitar

- ❌ `border-radius` mayor a 8px (destruye la estética)
- ❌ `box-shadow` con blur (ej: `0 4px 12px rgba(0,0,0,0.1)` — esto es el enemigo)
- ❌ Gradientes en backgrounds
- ❌ Tipografía delgada o elegante (weights < 600)
- ❌ Colores pasteles sin saturación
- ❌ Demasiados colores (máximo 2 acentos por UI)

---

## Casos de Uso Ideales

- Landing pages de startups / indie projects
- Tools y utilidades para desarrolladores
- Portfolios de diseñadores que quieren destacar
- SaaS con personalidad irreverente
- Webs de productos digitales (templates, plugins)
- Apps de productividad con estética de "herramienta real"
