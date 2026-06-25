---
name: dark-luxury-tailwind
description: Diseño Dark Luxury / Premium Dark implementado con Tailwind CSS. Usar cuando el usuario quiere interfaces oscuras de alta gama con acentos dorados o plateados, tipografía refinada y sensación de exclusividad usando clases de Tailwind con configuración extendida. Incluye tailwind.config.js, componentes con @apply y HTML de ejemplo.
---

# SKILL: Dark Luxury con Tailwind CSS

## Concepto

Dark Luxury tiene buena cobertura en Tailwind para los fondos oscuros (`bg-slate-*`, `bg-zinc-*`) pero la paleta metálica dorada y los detalles de lujo requieren extensión del config. Lo que necesita configuración:
- Colores oro/platino/champagne específicos
- Box-shadows con glow dorado
- Gradientes lineales metalicos (no están en Tailwind por defecto)
- Tipografía serif para displays

---

## tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,jsx,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Fondos oscuros con matiz — nunca negro puro
        'lux': {
          'deep':    '#080810',   // fondo principal
          'surface': '#0F0F1A',   // cards y paneles
          'raised':  '#161624',   // elementos elevados
          'overlay': '#1E1E30',   // modales, tooltips
        },
        // Metales
        'gold': {
          DEFAULT: '#C9A84C',
          'light': '#E8D5A3',
          'dim':   '#7A6030',
          'glow':  '#C9A84C26', // 15% opacity para glows
        },
        'platinum': {
          DEFAULT: '#B8B8C8',
          'dim':   '#6B6B80',
        },
        // Texto
        'lux-text': {
          'primary':   '#F0EDE8',
          'secondary': '#9090A8',
          'muted':     '#4A4A60',
        },
      },
      backgroundImage: {
        // Gradiente metálico dorado
        'gold-gradient': 'linear-gradient(135deg, #C9A84C 0%, #E8D5A3 50%, #C9A84C 100%)',
        'gold-h':        'linear-gradient(90deg, transparent 0%, #7A6030 20%, #C9A84C 50%, #7A6030 80%, transparent 100%)',
        // Fondo sutil
        'lux-gradient':  'linear-gradient(180deg, #1A1A2E 0%, #080810 100%)',
        // Grid de fondo
        'lux-grid':      'linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px)',
      },
      boxShadow: {
        'lux':          '0 8px 32px rgba(0,0,0,0.4)',
        'lux-card':     '0 4px 24px rgba(0,0,0,0.3)',
        'lux-elevated': '0 16px 48px rgba(0,0,0,0.5)',
        'gold-glow':    '0 0 30px rgba(201,168,76,0.2)',
        'gold-glow-lg': '0 0 50px rgba(201,168,76,0.4)',
        'gold-pulse':   '0 0 20px rgba(201,168,76,0.15)',
      },
      borderColor: {
        'lux-subtle': 'rgba(255,255,255,0.06)',
        'gold-dim':   'rgba(201,168,76,0.3)',
        'gold-hover': 'rgba(201,168,76,0.6)',
      },
      fontFamily: {
        'display': ['Cormorant Garamond', 'Georgia', 'serif'],
        'body':    ['DM Sans', 'sans-serif'],
      },
      fontSize: {
        'display-sm': ['clamp(2rem,4vw,3rem)', { lineHeight: '1.1', letterSpacing: '0.04em' }],
        'display-md': ['clamp(2.5rem,5vw,4rem)', { lineHeight: '1.1', letterSpacing: '0.04em' }],
        'display-lg': ['clamp(3rem,6vw,5rem)', { lineHeight: '1.05', letterSpacing: '0.04em' }],
      },
      animation: {
        'lux-reveal': 'luxReveal 0.9s cubic-bezier(0.16,1,0.3,1) forwards',
        'gold-pulse': 'goldPulse 3s ease-in-out infinite',
      },
      keyframes: {
        luxReveal: {
          '0%':   { opacity: '0', transform: 'translateY(30px)', filter: 'blur(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)', filter: 'blur(0)' },
        },
        goldPulse: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(201,168,76,0.15)' },
          '50%':      { boxShadow: '0 0 40px rgba(201,168,76,0.3)' },
        },
      },
      transitionDuration: {
        '400': '400ms',
      },
    },
  },
  plugins: [],
}
```

---

## CSS Base (@layer)

```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-lux-deep font-body text-lux-text-secondary leading-relaxed;
    background-image:
      linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 60px 60px;
  }

  h1, h2, h3 {
    @apply font-display text-lux-text-primary font-normal;
    letter-spacing: 0.04em;
    line-height: 1.15;
  }
}

@layer components {

  /* ── Navbar ── */
  .lux-nav {
    @apply fixed top-0 left-0 right-0 z-50 flex items-center justify-between;
    @apply px-12 py-5 backdrop-blur-xl border-b;
    background: rgba(8, 8, 16, 0.85);
    border-color: rgba(255, 255, 255, 0.06);
  }

  /* ── Cards ── */
  .lux-card {
    @apply bg-lux-surface rounded-2xl p-10 relative overflow-hidden;
    @apply border transition-all duration-300;
    border-color: rgba(255, 255, 255, 0.06);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
  }
  /* Línea dorada que aparece en hover (via pseudo en CSS, toggle con group en Tailwind) */
  .lux-card::before {
    content: '';
    @apply absolute top-0 left-0 right-0 h-px opacity-0 transition-opacity duration-300;
    background: linear-gradient(135deg, #C9A84C 0%, #E8D5A3 50%, #C9A84C 100%);
  }
  .lux-card:hover {
    @apply -translate-y-0.5;
    border-color: rgba(201, 168, 76, 0.3);
  }
  .lux-card:hover::before {
    @apply opacity-100;
  }

  .lux-card-raised {
    @apply lux-card bg-lux-raised;
  }

  /* ── Botones ── */
  /* Outline dorado (default) */
  .lux-btn {
    @apply relative overflow-hidden inline-flex items-center justify-center;
    @apply px-8 py-3 rounded-full cursor-pointer transition-all duration-300;
    @apply text-gold text-xs font-medium uppercase tracking-widest;
    @apply border;
    border-color: #7A6030;
  }
  .lux-btn::before {
    content: '';
    @apply absolute inset-0 opacity-0 transition-opacity duration-300 rounded-full;
    background: linear-gradient(135deg, #C9A84C 0%, #E8D5A3 50%, #C9A84C 100%);
  }
  .lux-btn span {
    @apply relative z-10;
  }
  .lux-btn:hover {
    @apply text-lux-deep border-transparent;
  }
  .lux-btn:hover::before {
    @apply opacity-100;
  }

  /* Sólido dorado (CTA) */
  .lux-btn-solid {
    @apply inline-flex items-center justify-center;
    @apply px-10 py-3.5 rounded-full cursor-pointer transition-all duration-300;
    @apply text-lux-deep text-xs font-semibold uppercase tracking-widest;
    @apply shadow-gold-glow hover:shadow-gold-glow-lg hover:-translate-y-0.5;
    background: linear-gradient(135deg, #C9A84C 0%, #E8D5A3 50%, #C9A84C 100%);
  }

  /* Ghost (texto dorado sin borde) */
  .lux-btn-ghost {
    @apply inline-flex items-center justify-center gap-2;
    @apply px-4 py-2 text-gold text-xs uppercase tracking-widest font-medium;
    @apply cursor-pointer transition-colors duration-300;
    @apply hover:text-gold-light;
  }

  /* ── Inputs ── */
  .lux-input {
    @apply w-full bg-lux-raised text-lux-text-primary;
    @apply px-4 py-3.5 rounded-xl outline-none;
    @apply text-sm font-light tracking-wide;
    @apply transition-all duration-300;
    @apply placeholder:text-lux-text-muted;
    border: 1px solid rgba(255, 255, 255, 0.06);
  }
  .lux-input:focus {
    border-color: rgba(201, 168, 76, 0.4);
    box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.08);
  }

  /* ── Separador dorado ── */
  .lux-divider {
    @apply border-none h-px my-12 w-3/5 mx-auto;
    background: linear-gradient(90deg, transparent 0%, #7A6030 20%, #C9A84C 50%, #7A6030 80%, transparent 100%);
  }

  /* ── Stat / Métrica ── */
  .lux-stat {
    @apply text-center py-8 px-6;
  }
  .lux-stat-value {
    @apply font-display text-5xl font-semibold leading-none;
    background: linear-gradient(135deg, #C9A84C 0%, #E8D5A3 50%, #C9A84C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .lux-stat-label {
    @apply text-lux-text-muted text-xs uppercase tracking-[0.2em] mt-2;
  }

  /* ── Badge ── */
  .lux-badge {
    @apply inline-flex items-center gap-1.5;
    @apply px-3 py-1 rounded-full text-xs uppercase tracking-widest font-medium;
    @apply text-gold;
    border: 1px solid rgba(201, 168, 76, 0.3);
    background: rgba(201, 168, 76, 0.05);
  }

  /* ── Label de sección ── */
  .lux-label {
    @apply text-gold text-xs font-light uppercase tracking-[0.15em] mb-3 block;
  }

  /* ── Reveal de entrada ── */
  .lux-reveal {
    @apply animate-lux-reveal;
  }

  /* ── Orbes de fondo (insertar como divs en el HTML) ── */
  .lux-orb {
    @apply fixed rounded-full pointer-events-none -z-10;
    filter: blur(120px);
    opacity: 0.06;
  }
  .lux-orb-gold  { @apply bg-gold w-[600px] h-[600px] -top-48 -right-24; }
  .lux-orb-blue  { background: #4060C0; @apply w-[500px] h-[500px] -bottom-48 -left-24; }
}
```

---

## HTML — Componentes Listos

### Estructura base

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
</head>
<body>
  <!-- Orbes de fondo -->
  <div class="lux-orb lux-orb-gold"></div>
  <div class="lux-orb lux-orb-blue"></div>

  <!-- Contenido -->
  <div class="relative z-10">
    ...
  </div>
</body>
</html>
```

### Navbar

```html
<nav class="lux-nav">
  <span class="font-display text-lux-text-primary text-xl tracking-[0.1em]">BRAND</span>
  <div class="flex items-center gap-8">
    <a href="#" class="text-lux-text-secondary hover:text-lux-text-primary text-xs uppercase tracking-widest transition-colors">Servicios</a>
    <a href="#" class="text-lux-text-secondary hover:text-lux-text-primary text-xs uppercase tracking-widest transition-colors">Nosotros</a>
    <button class="lux-btn"><span>Contacto</span></button>
  </div>
</nav>
```

### Hero

```html
<section class="min-h-screen flex items-center px-8 md:px-20 pt-20">
  <div class="max-w-3xl lux-reveal">
    <span class="lux-label">Portfolio exclusivo</span>
    <h1 class="font-display text-display-lg text-lux-text-primary mb-6">
      Diseño que<br/>
      <em class="italic text-gold">trasciende</em>
    </h1>
    <p class="text-lux-text-secondary text-lg font-light leading-relaxed max-w-xl mb-10">
      Creamos experiencias visuales que comunican lujo, confianza y diferenciación en cada detalle.
    </p>
    <div class="flex items-center gap-6">
      <button class="lux-btn-solid">Ver portfolio</button>
      <button class="lux-btn-ghost">Hablar con nosotros →</button>
    </div>
  </div>
</section>
```

### Card de servicio

```html
<div class="lux-card group">
  <span class="lux-label">Estrategia</span>
  <h3 class="font-display text-2xl text-lux-text-primary mb-4">
    Consultoría de Marca
  </h3>
  <p class="text-lux-text-secondary text-sm leading-relaxed mb-8">
    Definición de identidad, posicionamiento y arquitectura de marca para empresas de alto valor.
  </p>
  <button class="lux-btn-ghost text-xs">Explorar →</button>
</div>
```

### Stats / KPIs

```html
<div class="grid grid-cols-1 md:grid-cols-3 gap-px bg-white/5">
  <div class="lux-stat bg-lux-surface">
    <div class="lux-stat-value">98%</div>
    <div class="lux-stat-label">Satisfacción del cliente</div>
  </div>
  <div class="lux-stat bg-lux-surface">
    <div class="lux-stat-value">14K</div>
    <div class="lux-stat-label">Proyectos entregados</div>
  </div>
  <div class="lux-stat bg-lux-surface">
    <div class="lux-stat-value">32</div>
    <div class="lux-stat-label">Países alcanzados</div>
  </div>
</div>
```

### Formulario

```html
<div class="lux-card max-w-lg mx-auto">
  <span class="lux-label">Contacto exclusivo</span>
  <h2 class="font-display text-3xl text-lux-text-primary mb-8">
    Iniciemos una conversación
  </h2>

  <div class="space-y-5">
    <div>
      <label class="lux-label">Nombre completo</label>
      <input type="text" placeholder="Tu nombre" class="lux-input" />
    </div>
    <div>
      <label class="lux-label">Email corporativo</label>
      <input type="email" placeholder="nombre@empresa.com" class="lux-input" />
    </div>
    <div>
      <label class="lux-label">Mensaje</label>
      <textarea rows="4" placeholder="Contanos sobre tu proyecto..." class="lux-input resize-none"></textarea>
    </div>
  </div>

  <div class="lux-divider"></div>

  <button class="lux-btn-solid w-full">Enviar consulta</button>
</div>
```

### Modal / Dialog

```html
<div class="fixed inset-0 bg-lux-deep/80 backdrop-blur-sm z-50 flex items-center justify-center p-6">
  <div class="lux-card-raised max-w-md w-full">
    <div class="flex items-center justify-between mb-6">
      <h3 class="font-display text-xl text-lux-text-primary">Confirmar</h3>
      <button class="text-lux-text-muted hover:text-lux-text-secondary transition-colors">✕</button>
    </div>
    <p class="text-lux-text-secondary text-sm leading-relaxed mb-8">
      Esta acción procesará tu solicitud. El equipo se comunicará dentro de las 24hs hábiles.
    </p>
    <div class="flex gap-4 justify-end">
      <button class="lux-btn-ghost text-xs">Cancelar</button>
      <button class="lux-btn-solid text-xs px-6 py-2.5">Confirmar</button>
    </div>
  </div>
</div>
```

---

## Gradiente Dorado con Texto (Tailwind no lo cubre — requiere CSS inline)

```html
<!-- Opción 1: style inline -->
<span style="background: linear-gradient(135deg, #C9A84C, #E8D5A3, #C9A84C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
  Texto dorado
</span>

<!-- Opción 2: clase custom en @layer utilities -->
```

```css
@layer utilities {
  .text-gold-gradient {
    background: linear-gradient(135deg, #C9A84C 0%, #E8D5A3 50%, #C9A84C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}
```

```html
<!-- Uso -->
<span class="text-gold-gradient font-display text-5xl">Valor destacado</span>
```

---

## Referencia Rápida: Clases Nativas de Tailwind para Dark Luxury

| Propiedad | Clase Tailwind |
|-----------|---------------|
| Fondo oscuro con matiz | `bg-lux-deep` (config) |
| Texto blanco cálido | `text-lux-text-primary` (config) |
| Texto secundario | `text-lux-text-secondary` (config) |
| Borde sutil | `border border-white/[0.06]` |
| Blur de navbar | `backdrop-blur-xl` |
| Spacing generoso | `p-10`, `py-8`, `space-y-8` |
| Tipografía display | `font-display` (config) |
| Tracking amplio | `tracking-widest` |
| Transición lenta | `transition-all duration-300` |
| Translate en hover | `hover:-translate-y-0.5` |

---

## Anti-patrones a Evitar

- ❌ `bg-black` — usar `bg-lux-deep` (negro con matiz)
- ❌ `text-white` — usar `text-lux-text-primary` (blanco cálido)
- ❌ `bg-yellow-400`, `bg-red-500` como acentos — rompen el refinamiento
- ❌ `font-sans` para displays — siempre `font-display` (serif)
- ❌ `duration-75` o `duration-150` — las animaciones deben ser lentas (`duration-300`+)
- ❌ `rounded-none` — el lujo usa radios suaves (`rounded-xl`, `rounded-2xl`)
- ❌ `border-4` o bordes gruesos — máximo `border` (1px)

---

## Casos de Uso Ideales

- Plataformas fintech / wealth management
- Landing pages de productos crypto premium
- Agencias de diseño de alto nivel
- Portfolios de fotógrafos / cinematógrafos
- Marcas de moda y lujo digital
- SaaS Enterprise con imagen premium
