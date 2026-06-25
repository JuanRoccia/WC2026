---
name: japanese-minimalism-tailwind
description: Diseño Minimalismo Japonés / Wabi-Sabi implementado con Tailwind CSS. Usar cuando el usuario quiere interfaces con estética de calma profunda: paleta de tierra y neutros cálidos, mucho espacio en blanco, tipografía refinada con mucho peso en el espaciado, elementos que emergen del silencio, texturas sutiles y sensación de intención en cada elemento. Inspirado en el wabi-sabi, el diseño japonés de producto, la arquitectura de Tadao Ando y marcas como Muji, Aesop, Uniqlo. Ideal para portfolios contemplativos, marcas de bienestar, arquitectura, gastronomía premium y cualquier producto que valore la quietud y la calidad. Incluye tailwind.config.js completo, @layer components y HTML de ejemplo.
---

# SKILL: Minimalismo Japonés con Tailwind CSS

## Concepto

El **Minimalismo Japonés** no es simplemente "poca cosa". Es la filosofía de que cada elemento presente debe ganar su lugar. Viene del *wabi-sabi* (la belleza de la imperfección y lo transitorio), el *ma* (el espacio negativo como elemento activo), y el *kanso* (simplicidad sin ornamentación innecesaria).

En diseño digital se traduce en: fondos de tierra y neutros cálidos (nunca blanco frío), tipografía con mucho espacio de tracking, elementos aislados con aire a su alrededor, transiciones lentas y casi imperceptibles, y textura que se intuye más que se ve.

Referentes: Muji, Aesop, Uniqlo digital, Japan House, revistas de arquitectura como A+U, marcas de cerámica artesanal japonesa.

**La firma del Minimalismo Japonés:**
- Paleta de tierra: blancos cálidos, beiges, grises cálidos, verde oscuro, negro con matiz
- Espacio en blanco como protagonista — no como relleno
- Tipografía con tracking generoso (`tracking-widest`) y line-height amplio
- Sin border-radius dramático — esquinas rectas o con radio mínimo
- Transiciones muy lentas (500-800ms) y completamente lineales o ease
- Una imagen o elemento por pantalla — nunca competencia visual

---

## tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,jsx,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'wa': {
          // Fondos — neutros cálidos, nunca fríos
          'paper':    '#F8F5F0',   // papel japonés — blanco cálido con matiz
          'cream':    '#F0EBE3',   // crema profunda
          'sand':     '#E8E0D5',   // arena cálida
          'mist':     '#EDF0EC',   // verde muy palido (mist)

          // Tierra y profundidad
          'stone':    '#8C8279',   // gris cálido medio
          'ash':      '#B5AFA8',   // ceniza cálida
          'charcoal': '#3A3530',   // casi negro cálido
          'ink':      '#1A1714',   // negro profundo cálido — el más oscuro

          // Acentos contenidos — usar máximo UNO por proyecto
          'moss':     '#4A5C42',   // verde musgo oscuro (wabi-sabi)
          'clay':     '#8B5E52',   // terracota suave
          'iron':     '#4A4A52',   // gris azulado frío
          'rust':     '#7A3B2E',   // óxido contenido
          'gold':     '#8B6914',   // oro oscuro, nada brillante

          // Bordes y separadores
          'border':   '#D8D0C8',   // borde cálido apenas visible
          'border-lt':'#EAE5DF',   // borde muy sutil
        },
      },

      fontFamily: {
        // Japonés minimalista usa fuentes con mucho carácter o muy neutras
        'wa':         ['Cormorant', 'Georgia', 'serif'],         // refinada y con carácter
        'wa-sans':    ['Jost', 'Helvetica Neue', 'sans-serif'],  // sans neutro con tracking
        'wa-display': ['Bodoni Moda', 'Didot', 'serif'],         // display dramático
        'wa-mono':    ['DM Mono', 'Courier New', 'monospace'],   // datos limpios
      },

      fontSize: {
        'wa-xs':   ['0.65rem', { lineHeight: '1.8', letterSpacing: '0.15em' }],
        'wa-sm':   ['0.8rem',  { lineHeight: '1.8', letterSpacing: '0.1em' }],
        'wa-base': ['1rem',    { lineHeight: '1.9', letterSpacing: '0.04em' }],
        'wa-lg':   ['1.2rem',  { lineHeight: '1.8', letterSpacing: '0.03em' }],
        'wa-xl':   ['1.6rem',  { lineHeight: '1.5', letterSpacing: '0.01em' }],
        'wa-2xl':  ['2.4rem',  { lineHeight: '1.3', letterSpacing: '-0.01em' }],
        'wa-3xl':  ['3.6rem',  { lineHeight: '1.15',letterSpacing: '-0.02em' }],
        'wa-4xl':  ['5.5rem',  { lineHeight: '1.05',letterSpacing: '-0.03em' }],
        'wa-hero': ['clamp(4rem,9vw,9rem)', { lineHeight: '1.0', letterSpacing: '-0.03em' }],
      },

      spacing: {
        'wa-xs':  '0.75rem',
        'wa-sm':  '2rem',
        'wa-md':  '4rem',
        'wa-lg':  '8rem',
        'wa-xl':  '14rem',
        'wa-2xl': '20rem',
      },

      maxWidth: {
        'wa-text':  '60ch',
        'wa-narrow':'42ch',
        'wa-wide':  '80ch',
      },

      borderRadius: {
        'wa': '2px',   // casi nada — minimalismo japonés es casi recto
      },

      transitionDuration: {
        '400': '400ms',
        '600': '600ms',
        '800': '800ms',
      },

      transitionTimingFunction: {
        'wa': 'cubic-bezier(0.4, 0, 0.2, 1)',  // ease estándar, controlado
        'wa-slow': 'cubic-bezier(0.2, 0, 0, 1)', // muy controlado, sin rebote
      },

      animation: {
        'wa-reveal':  'waReveal 0.8s cubic-bezier(0.4,0,0.2,1) forwards',
        'wa-fade':    'waFade 1.2s ease forwards',
        'wa-rise':    'waRise 0.9s cubic-bezier(0.4,0,0.2,1) forwards',
      },
      keyframes: {
        waReveal: {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        waFade: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        waRise: {
          '0%':   { opacity: '0', transform: 'translateY(40px)', filter: 'blur(4px)' },
          '100%': { opacity: '1', transform: 'translateY(0)', filter: 'blur(0)' },
        },
      },

      backgroundImage: {
        // Textura muy sutil de papel — casi imperceptible
        'wa-texture': `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E")`,
      },
    },
  },
  plugins: [],
}
```

---

## CSS Base (@layer)

```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@200;300;400;500&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,700;1,6..96,400&family=DM+Mono:wght@300;400&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-wa-paper font-wa-sans text-wa-charcoal;
    font-size: 16px;
    line-height: 1.9;
    letter-spacing: 0.03em;
    -webkit-font-smoothing: antialiased;
  }

  /* El espacio entre párrafos es generoso */
  p + p {
    @apply mt-6;
  }

  /* Links sutiles */
  a {
    @apply text-wa-charcoal border-b border-wa-border;
    @apply transition-colors duration-600 ease-wa;
  }
  a:hover {
    @apply border-wa-ink;
  }

  /* Selección de texto */
  ::selection {
    background: rgba(74, 92, 66, 0.15); /* moss con alpha */
  }

  /* Scrollbar minimalista */
  ::-webkit-scrollbar { width: 3px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--wa-ash, #B5AFA8); }
}

@layer components {

  /* ── Navbar ── */
  .wa-nav {
    @apply flex items-center justify-between;
    @apply px-wa-md py-6 border-b border-wa-border-lt;
  }
  .wa-nav-logo {
    @apply font-wa-display text-xl font-normal tracking-widest text-wa-ink;
    letter-spacing: 0.2em;
  }
  .wa-nav-link {
    @apply font-wa-sans text-wa-xs font-light uppercase tracking-widest;
    @apply text-wa-stone hover:text-wa-ink transition-colors duration-400 ease-wa;
  }

  /* ── Titulares ── */
  .wa-headline-hero {
    @apply font-wa text-wa-hero font-light text-wa-ink;
  }
  .wa-headline-xl {
    @apply font-wa text-wa-4xl font-light text-wa-ink;
  }
  .wa-headline-lg {
    @apply font-wa text-wa-3xl font-light text-wa-ink;
  }
  .wa-headline-md {
    @apply font-wa text-wa-2xl font-light text-wa-ink;
  }
  .wa-headline-sm {
    @apply font-wa text-wa-xl font-normal text-wa-ink;
  }

  /* Titular en itálica — muy wabi-sabi */
  .wa-italic {
    @apply font-wa italic font-light;
  }

  /* ── Etiqueta / Label ── */
  .wa-label {
    @apply font-wa-sans text-wa-xs font-light uppercase tracking-[0.25em] text-wa-stone;
    @apply block mb-3;
  }

  /* ── Cuerpo de texto ── */
  .wa-body {
    @apply font-wa-sans text-wa-base font-light text-wa-charcoal;
    @apply max-w-wa-text leading-[1.9];
  }
  .wa-body-serif {
    @apply font-wa text-wa-lg font-light text-wa-charcoal;
    @apply max-w-wa-text leading-[1.8];
  }

  /* ── Cards ── */
  .wa-card {
    @apply bg-wa-paper border border-wa-border-lt;
    @apply p-10 transition-all duration-600 ease-wa;
  }
  .wa-card:hover {
    @apply border-wa-border bg-wa-cream;
  }

  /* Card de producto (estilo Muji) */
  .wa-product-card {
    @apply flex flex-col;
    @apply transition-all duration-600 ease-wa cursor-pointer;
  }
  .wa-product-card-image {
    @apply bg-wa-sand overflow-hidden aspect-square mb-6;
  }
  .wa-product-card-image img {
    @apply w-full h-full object-cover;
    @apply transition-transform duration-800 ease-wa-slow;
  }
  .wa-product-card:hover .wa-product-card-image img {
    @apply scale-105;
  }
  .wa-product-name {
    @apply font-wa-sans text-wa-sm font-light text-wa-charcoal tracking-wider mb-1;
  }
  .wa-product-detail {
    @apply font-wa-sans text-wa-xs font-light text-wa-stone tracking-wider;
  }
  .wa-product-price {
    @apply font-wa-mono text-wa-sm text-wa-charcoal mt-2 tracking-wide;
  }

  /* ── Botones ── */
  /* Minimalismo japonés: los botones son sutiles, casi invisibles */
  .wa-btn {
    @apply inline-flex items-center gap-4;
    @apply font-wa-sans text-wa-xs font-light uppercase tracking-[0.2em];
    @apply text-wa-charcoal border border-wa-border px-8 py-4;
    @apply transition-all duration-400 ease-wa cursor-pointer;
  }
  .wa-btn:hover {
    @apply bg-wa-charcoal text-wa-paper border-wa-charcoal;
  }

  /* Botón de acento (muy contenido) */
  .wa-btn-accent {
    @apply wa-btn bg-wa-charcoal text-wa-paper border-wa-charcoal;
    @apply hover:bg-wa-ink hover:border-wa-ink;
  }

  /* Botón ghost — solo texto con línea inferior */
  .wa-btn-ghost {
    @apply inline-flex items-center gap-3;
    @apply font-wa-sans text-wa-xs font-light uppercase tracking-[0.2em];
    @apply text-wa-charcoal border-b border-wa-border pb-0.5;
    @apply transition-all duration-400 ease-wa cursor-pointer;
  }
  .wa-btn-ghost:hover {
    @apply border-wa-ink text-wa-ink;
  }

  /* ── Inputs ── */
  .wa-input {
    @apply w-full bg-transparent;
    @apply font-wa-sans text-wa-base font-light text-wa-charcoal;
    @apply border-0 border-b border-wa-border py-3 px-0;
    @apply tracking-wide outline-none;
    @apply transition-all duration-400 ease-wa;
    @apply placeholder:text-wa-ash placeholder:font-light placeholder:tracking-wide;
  }
  .wa-input:focus {
    @apply border-wa-charcoal;
  }

  /* ── Separadores ── */
  .wa-rule {
    @apply border-none h-px bg-wa-border my-wa-md;
  }
  .wa-rule-lt {
    @apply border-none h-px bg-wa-border-lt my-wa-sm;
  }
  /* Separador estilo japonés — línea cortada + espacio */
  .wa-rule-accent {
    @apply flex items-center gap-6 my-wa-md;
  }
  .wa-rule-accent::before,
  .wa-rule-accent::after {
    content: '';
    @apply flex-1 h-px bg-wa-border;
  }

  /* ── Quote ── */
  .wa-quote {
    @apply font-wa italic text-wa-xl font-light text-wa-charcoal;
    @apply border-l-2 border-wa-moss pl-8 my-wa-md;
    @apply max-w-wa-text;
  }
  .wa-quote cite {
    @apply font-wa-sans text-wa-xs font-light not-italic text-wa-stone;
    @apply tracking-wider mt-3 block;
  }

  /* ── Estadísticas / Números ── */
  .wa-stat {
    @apply text-center py-wa-md;
  }
  .wa-stat-value {
    @apply font-wa text-wa-4xl font-light text-wa-ink;
    @apply block mb-2;
  }
  .wa-stat-label {
    @apply font-wa-sans text-wa-xs font-light uppercase tracking-[0.25em] text-wa-stone;
    @apply block;
  }

  /* ── Badge sutil ── */
  .wa-badge {
    @apply inline-block font-wa-sans text-wa-xs font-light uppercase tracking-[0.2em];
    @apply text-wa-stone border border-wa-border px-4 py-1;
  }

  /* ── Imagen con caption ── */
  .wa-figure {
    @apply my-wa-lg;
  }
  .wa-caption {
    @apply font-wa-sans text-wa-xs font-light text-wa-stone tracking-wider;
    @apply mt-4 text-center;
  }

  /* ── Reveal de contenido ── */
  .wa-reveal { @apply animate-wa-reveal; }
  .wa-fade   { @apply animate-wa-fade; }
  .wa-rise   { @apply animate-wa-rise; }

  /* ── Sidebar / Columna secundaria ── */
  .wa-sidebar-rule {
    @apply border-l border-wa-border pl-8 ml-8;
  }
}

@layer utilities {
  /* Ma — el espacio como elemento de diseño */
  .ma-sm  { @apply py-wa-sm; }
  .ma-md  { @apply py-wa-md; }
  .ma-lg  { @apply py-wa-lg; }
  .ma-xl  { @apply py-wa-xl; }

  /* Texto vertical japonés decorativo */
  .text-vertical {
    writing-mode: vertical-rl;
    text-orientation: mixed;
    @apply tracking-widest;
  }

  /* Opacity contenida */
  .wa-muted { @apply text-wa-stone; }
  .wa-hint  { @apply text-wa-ash; }
}
```

---

## HTML — Componentes Listos

### Navbar

```html
<nav class="wa-nav max-w-7xl mx-auto">
  <!-- Texto vertical decorativo (opcional) -->
  <span class="text-vertical text-wa-xs text-wa-ash font-light tracking-widest hidden lg:block select-none">
    Est. 2024
  </span>

  <span class="wa-nav-logo">SHIZUKA</span>

  <div class="flex items-center gap-8">
    <a href="#" class="wa-nav-link">Colección</a>
    <a href="#" class="wa-nav-link">Proceso</a>
    <a href="#" class="wa-nav-link">Nosotros</a>
    <a href="#" class="wa-btn text-xs px-6 py-3">Contacto</a>
  </div>
</nav>
```

### Hero minimalista

```html
<section class="max-w-7xl mx-auto px-wa-md py-wa-xl">
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-wa-xl items-center min-h-[70vh]">

    <!-- Texto -->
    <div class="wa-reveal">
      <span class="wa-label">Primavera — Verano 2026</span>
      <h1 class="wa-headline-hero mb-8">
        La quietud<br/>
        <em class="wa-italic">que permanece</em>
      </h1>
      <p class="wa-body mb-wa-md">
        Objetos diseñados para durar más que las modas.
        Materiales que mejoran con el tiempo. Formas que no piden nada.
      </p>
      <div class="flex items-center gap-8">
        <a href="#" class="wa-btn-accent">Ver colección</a>
        <a href="#" class="wa-btn-ghost">Nuestro proceso →</a>
      </div>
    </div>

    <!-- Imagen -->
    <div class="wa-figure lg:mt-0 mt-wa-md">
      <div class="aspect-portrait bg-wa-sand overflow-hidden">
        <img src="..." alt="Cerámica artesanal" class="w-full h-full object-cover" />
      </div>
      <p class="wa-caption">Serie Kiri, terracota sin esmaltar, 2026</p>
    </div>

  </div>
</section>
```

### Grid de productos (estilo Muji)

```html
<section class="max-w-7xl mx-auto px-wa-md py-wa-lg">
  <div class="wa-rule mb-wa-lg"></div>

  <div class="flex items-baseline justify-between mb-wa-md">
    <h2 class="wa-headline-md">Colección</h2>
    <a href="#" class="wa-btn-ghost">Ver todo →</a>
  </div>

  <div class="grid grid-cols-2 md:grid-cols-4 gap-8">

    <div class="wa-product-card">
      <div class="wa-product-card-image">
        <img src="..." alt="Cuenco Kiri" />
      </div>
      <span class="wa-label">Cerámica</span>
      <h3 class="wa-product-name">Cuenco Kiri</h3>
      <p class="wa-product-detail">Terracota sin esmaltar — Ø 14cm</p>
      <span class="wa-product-price">$4.800</span>
    </div>

    <div class="wa-product-card">
      <div class="wa-product-card-image">
        <img src="..." alt="Vasija Nami" />
      </div>
      <span class="wa-label">Cerámica</span>
      <h3 class="wa-product-name">Vasija Nami</h3>
      <p class="wa-product-detail">Gres con ceniza — 22cm</p>
      <span class="wa-product-price">$8.200</span>
    </div>

    <div class="wa-product-card">
      <div class="wa-product-card-image bg-wa-cream">
        <img src="..." alt="Plato Yama" />
      </div>
      <span class="wa-label">Mesa</span>
      <h3 class="wa-product-name">Plato Yama</h3>
      <p class="wa-product-detail">Porcelana cruda — Ø 26cm</p>
      <span class="wa-product-price">$3.600</span>
    </div>

    <div class="wa-product-card">
      <div class="wa-product-card-image">
        <img src="..." alt="Jarra Umi" />
      </div>
      <span class="wa-label">Mesa</span>
      <h3 class="wa-product-name">Jarra Umi</h3>
      <p class="wa-product-detail">Gres azul — 28cm</p>
      <span class="wa-product-price">$9.400</span>
    </div>

  </div>
</section>
```

### Sección de filosofía / About

```html
<section class="max-w-7xl mx-auto px-wa-md py-wa-xl">
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-wa-lg">

    <!-- Número decorativo -->
    <div class="lg:col-span-2 flex items-start pt-2">
      <span class="font-wa-mono text-wa-xs text-wa-ash font-light tracking-widest text-vertical hidden lg:block">
        Wabi-Sabi
      </span>
    </div>

    <!-- Contenido principal -->
    <div class="lg:col-span-6">
      <span class="wa-label">Nuestra filosofía</span>
      <h2 class="wa-headline-lg mb-wa-md">
        La belleza de lo<br/>
        <em class="wa-italic">imperfecto</em>
      </h2>
      <div class="wa-body-serif space-y-6">
        <p>
          El wabi-sabi nos enseña que la perfección no existe, y que en esa ausencia
          reside lo verdaderamente hermoso. Una marca de uso, una asimetría inesperada,
          la patina que deja el tiempo sobre el barro cocido.
        </p>
        <p>
          Trabajamos con las manos, con materiales que vienen de la tierra y vuelven
          a ella. Cada pieza es única no porque lo decidimos, sino porque no puede ser
          de otra manera.
        </p>
      </div>

      <blockquote class="wa-quote mt-wa-md">
        "No hay nada que un objeto bien hecho no pueda decir mejor que cualquier palabra."
        <cite>— Yanagi Sōetsu</cite>
      </blockquote>
    </div>

    <!-- Sidebar con stats -->
    <div class="lg:col-span-4 wa-sidebar-rule">
      <div class="space-y-wa-md">
        <div class="wa-stat text-left">
          <span class="wa-stat-value">12</span>
          <span class="wa-stat-label">años trabajando el gres</span>
        </div>
        <div class="wa-rule-lt"></div>
        <div class="wa-stat text-left">
          <span class="wa-stat-value">340+</span>
          <span class="wa-stat-label">piezas producidas a mano</span>
        </div>
        <div class="wa-rule-lt"></div>
        <div class="wa-stat text-left">
          <span class="wa-stat-value">1</span>
          <span class="wa-stat-label">taller, Bahía Blanca, Argentina</span>
        </div>
      </div>
    </div>

  </div>
</section>
```

### Formulario de contacto

```html
<section class="max-w-3xl mx-auto px-wa-md py-wa-xl">
  <span class="wa-label">Contacto</span>
  <h2 class="wa-headline-md mb-2">Conversemos</h2>
  <p class="wa-body mb-wa-lg">Respondemos dentro de los 2 días hábiles.</p>

  <form class="space-y-10">
    <div>
      <label class="wa-label">Tu nombre</label>
      <input type="text" placeholder="Juan García" class="wa-input" />
    </div>
    <div>
      <label class="wa-label">Email</label>
      <input type="email" placeholder="juan@ejemplo.com" class="wa-input" />
    </div>
    <div>
      <label class="wa-label">Mensaje</label>
      <textarea rows="5" placeholder="¿En qué podemos ayudarte?" class="wa-input resize-none"></textarea>
    </div>

    <div class="wa-rule-lt pt-2 flex items-center justify-between">
      <span class="font-wa-sans text-wa-xs font-light text-wa-ash tracking-wider">
        Respondemos en 1-2 días hábiles
      </span>
      <button type="submit" class="wa-btn-accent">Enviar</button>
    </div>
  </form>
</section>
```

### Footer editorial mínimo

```html
<footer class="border-t border-wa-border mt-wa-xl">
  <div class="max-w-7xl mx-auto px-wa-md py-wa-lg">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-wa-md">
      <div>
        <span class="wa-nav-logo text-lg block mb-4">SHIZUKA</span>
        <p class="font-wa-sans text-wa-xs font-light text-wa-stone leading-relaxed tracking-wide">
          Cerámica artesanal.<br/>Bahía Blanca, Argentina.
        </p>
      </div>
      <div>
        <span class="wa-label">Navegación</span>
        <div class="space-y-3">
          <a href="#" class="wa-nav-link block">Colección</a>
          <a href="#" class="wa-nav-link block">Proceso</a>
          <a href="#" class="wa-nav-link block">Nosotros</a>
          <a href="#" class="wa-nav-link block">Contacto</a>
        </div>
      </div>
      <div>
        <span class="wa-label">Newsletter</span>
        <p class="font-wa-sans text-wa-xs font-light text-wa-stone mb-4 tracking-wide">
          Nuevas piezas, una vez al mes.
        </p>
        <div class="flex gap-0 border-b border-wa-border">
          <input type="email" placeholder="tu@email.com"
                 class="wa-input border-0 border-none flex-1 text-xs py-2" />
          <button class="font-wa-sans text-wa-xs font-light uppercase tracking-widest text-wa-charcoal px-4 whitespace-nowrap">
            →
          </button>
        </div>
      </div>
    </div>

    <div class="wa-rule mt-wa-md"></div>
    <div class="flex items-center justify-between">
      <span class="font-wa-mono text-wa-xs text-wa-ash font-light tracking-wider">
        © 2026 Shizuka Cerámica
      </span>
      <span class="font-wa-mono text-wa-xs text-wa-ash font-light tracking-wider">
        Hecho a mano
      </span>
    </div>
  </div>
</footer>
```

---

## Principios del Espacio (Ma)

```html
<!-- El espacio NO es relleno — es el silencio entre notas -->
<!-- Usar siempre clases de espaciado generosas -->

<!-- ✅ Correcto: elementos con aire -->
<section class="py-wa-xl px-wa-md">
  <h2 class="wa-headline-lg mb-wa-md">Título</h2>
  <p class="wa-body">Texto con espacio a su alrededor.</p>
</section>

<!-- ❌ Incorrecto: elementos apretados -->
<section class="py-4 px-4">
  <h2 class="text-2xl mb-2">Título</h2>
  <p>Texto sin espacio.</p>
</section>
```

---

## Anti-patrones a Evitar

- ❌ Fondos blancos fríos (`#FFFFFF` puro) — usar siempre blancos cálidos (`wa-paper`, `wa-cream`)
- ❌ Más de 1 color de acento — el minimalismo japonés es radical en esto
- ❌ `rounded-xl` o `rounded-full` — esquinas rectas o `rounded-wa` (2px) máximo
- ❌ Animaciones rápidas o bouncy — todo es `duration-600` o más lento
- ❌ Tipografía sans-serif como display — serif refinada para titulares
- ❌ `font-bold` o `font-black` — el peso es `font-light` o `font-normal` siempre
- ❌ Relleno de espacio con elementos decorativos — el espacio vacío es intencional
- ❌ Más de 3 elementos por sección — nunca competencia visual
- ❌ Sombras dramáticas — si hay sombra, es `shadow-sm` con color muy neutro
- ❌ Gradientes de color — nunca en este estilo

---

## Casos de Uso Ideales

- Portfolios de artistas, fotógrafos, artesanos
- Marcas de bienestar, meditación, yoga
- Gastronomía premium y slow food
- Arquitectura y diseño de interiores
- Moda slow fashion y artesanía
- Marcas de cosmética natural y orgánica
- Espacios culturales y galerías de arte
- Consultoras y estudios profesionales con trabajo de largo aliento
