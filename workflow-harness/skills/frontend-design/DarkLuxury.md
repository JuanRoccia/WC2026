---
name: dark-luxury-design
description: Diseño web con estética Dark Luxury / Premium Dark. Usar cuando el usuario quiere interfaces oscuras de alta gama, con gradientes sutiles, acentos dorados o plateados, tipografía refinada, mucho espacio en blanco oscuro y sensación de exclusividad. Ideal para marcas premium, fintech, crypto, agencias de diseño, portfolios de alto nivel y productos de lujo.
---

# SKILL: Dark Luxury / Premium Dark Design

## Concepto

El **Dark Luxury** no es simplemente un dark mode. Es una estética de **sofisticación contenida**: fondos casi-negros con matiz de color (nunca negro puro), acentos metálicos (oro, platino, champagne), tipografía elegante con mucho espacio, y detalles que sugieren exclusividad sin gritar.

Referentes: Rolex, Louis Vuitton digital, Stripe Press, Linear (v2), plataformas crypto premium como Ledger Live, agencias de diseño top.

---

## Reglas de Diseño

### Principios Fundamentales
1. **Negro con matiz** — nunca `#000000`. Usar `#0A0A0F`, `#090C12`, `#0C0B10`
2. **Acentos metálicos** — oro (`#C9A84C`), platino (`#B8B8C8`), champagne (`#E8D5A3`)
3. **Espaciado generoso** — padding y margin grandes; el lujo necesita espacio para respirar
4. **Tipografía refinada** — serifs elegantes o sans-serifs ultra-ligeros/pesados con contraste
5. **Detalles mínimos, máximo impacto** — una línea dorada, un gradiente sutil, un borde de 1px
6. **Sin ruido visual** — máximo 3 elementos por pantalla visible

---

## Paleta de Color

```css
:root {
  /* Fondos oscuros con matiz */
  --bg-deep:    #080810;   /* fondo principal — casi negro azulado */
  --bg-surface: #0F0F1A;   /* cards y paneles */
  --bg-raised:  #161624;   /* elementos elevados */
  --bg-overlay: #1E1E30;   /* modales, tooltips */
  
  /* Acentos metálicos */
  --gold:         #C9A84C;
  --gold-light:   #E8D5A3;
  --gold-dim:     #7A6030;
  --platinum:     #B8B8C8;
  --platinum-dim: #6B6B80;
  
  /* Gradientes de acento */
  --gradient-gold: linear-gradient(135deg, #C9A84C 0%, #E8D5A3 50%, #C9A84C 100%);
  --gradient-subtle: linear-gradient(180deg, #1A1A2E 0%, #080810 100%);
  
  /* Texto */
  --text-primary:   #F0EDE8;      /* blanco cálido */
  --text-secondary: #9090A8;      /* gris azulado */
  --text-muted:     #4A4A60;
  --text-gold:      #C9A84C;
  
  /* Bordes */
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-gold:   rgba(201, 168, 76, 0.3);
  --border-hover:  rgba(201, 168, 76, 0.6);
}
```

---

## Tipografía

El contraste tipográfico es esencial: un serif lujoso para display, un sans limpio para cuerpo.

```html
<!-- Combinación principal -->
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<!-- Alternativa más contemporánea -->
<!-- Playfair Display + Inter Light -->
<!-- Bodoni Moda + Neue Haas (local) -->
```

```css
h1, h2, .display {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 400;
  letter-spacing: 0.04em;
  color: var(--text-primary);
  line-height: 1.15;
}

h1 { font-size: clamp(2.5rem, 6vw, 5rem); }

.subtitle {
  font-family: 'DM Sans', sans-serif;
  font-weight: 300;
  font-size: 0.9rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--text-gold);
}

body {
  font-family: 'DM Sans', sans-serif;
  font-weight: 400;
  color: var(--text-secondary);
  line-height: 1.7;
}
```

---

## Componentes Clave

### Card Premium
```css
.luxury-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 2.5rem;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s ease, transform 0.3s ease;
}

.luxury-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: var(--gradient-gold);
  opacity: 0;
  transition: opacity 0.3s;
}

.luxury-card:hover {
  border-color: var(--border-gold);
  transform: translateY(-2px);
}

.luxury-card:hover::before {
  opacity: 1;
}
```

### Botón Primario Dorado
```css
.btn-luxury {
  background: transparent;
  color: var(--gold);
  border: 1px solid var(--gold-dim);
  border-radius: 50px;
  padding: 0.75rem 2rem;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-luxury::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--gradient-gold);
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: inherit;
}

.btn-luxury:hover {
  color: #0A0A0F;
  border-color: transparent;
}

.btn-luxury:hover::before {
  opacity: 1;
}

.btn-luxury span {
  position: relative;
  z-index: 1;
}
```

### Botón Sólido Dorado (CTA principal)
```css
.btn-luxury-solid {
  background: var(--gradient-gold);
  color: #0A0A0F;
  border: none;
  border-radius: 50px;
  padding: 0.85rem 2.5rem;
  font-weight: 600;
  font-size: 0.85rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: 0 0 30px rgba(201, 168, 76, 0.2);
  transition: box-shadow 0.3s, transform 0.3s;
}

.btn-luxury-solid:hover {
  box-shadow: 0 0 50px rgba(201, 168, 76, 0.4);
  transform: translateY(-1px);
}
```

### Línea separadora dorada
```css
.luxury-divider {
  border: none;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--gold-dim) 20%,
    var(--gold) 50%,
    var(--gold-dim) 80%,
    transparent 100%
  );
  margin: 3rem auto;
  width: 60%;
}
```

### Stat / Métrica de lujo
```css
.luxury-stat {
  text-align: center;
  padding: 2rem;
}

.luxury-stat .value {
  font-family: 'Cormorant Garamond', serif;
  font-size: 3.5rem;
  font-weight: 600;
  background: var(--gradient-gold);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

.luxury-stat .label {
  font-size: 0.75rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-top: 0.5rem;
}
```

### Navbar
```css
.luxury-nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  background: rgba(8, 8, 16, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-subtle);
  padding: 1.2rem 3rem;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
```

---

## Efectos de Fondo

```css
/* Glow sutil de color profundo */
body {
  background: var(--bg-deep);
  position: relative;
}

/* Orbe de color muy sutil para dar vida */
.bg-glow {
  position: fixed;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.06;
  pointer-events: none;
}
.bg-glow--gold {
  background: #C9A84C;
  top: -200px; right: -100px;
}
.bg-glow--blue {
  background: #4060C0;
  bottom: -200px; left: -100px;
}

/* Grid sutil de fondo (muy popular en fintech premium) */
.bg-grid {
  background-image:
    linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 60px 60px;
}
```

---

## Animaciones

Las animaciones son **lentas y fluidas** — el lujo no tiene prisa:

```css
/* Reveal de contenido */
@keyframes luxuryReveal {
  from {
    opacity: 0;
    transform: translateY(30px);
    filter: blur(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}

.reveal {
  animation: luxuryReveal 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Glow pulse en elementos de acento */
@keyframes goldPulse {
  0%, 100% { box-shadow: 0 0 20px rgba(201, 168, 76, 0.15); }
  50%       { box-shadow: 0 0 40px rgba(201, 168, 76, 0.3); }
}
```

---

## Anti-patrones a Evitar

- ❌ `#000000` como fondo — demasiado plano y sin vida
- ❌ Colores de acento saturados (rojo, verde brillante, amarillo) — rompen el refinamiento
- ❌ Tipografía sin serif en displays grandes (pierde la elegancia)
- ❌ Demasiados elementos por sección — el lujo necesita espacio
- ❌ Animaciones rápidas o bouncy — el ritmo debe ser lento y deliberado
- ❌ Bordes gruesos — máximo 1px salvo excepciones decorativas

---

## Casos de Uso Ideales

- Plataformas fintech / wealth management
- Landing pages de productos crypto premium
- Agencias de diseño de alto nivel
- Portfolios de fotógrafos / cinematógrafos
- Marcas de moda y lujo
- SaaS Enterprise con imagen premium
- Plataformas de arte digital / NFT de gama alta
