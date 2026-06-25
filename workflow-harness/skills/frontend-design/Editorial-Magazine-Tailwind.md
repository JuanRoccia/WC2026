---
name: editorial-magazine-tailwind
description: Diseño Editorial / Magazine implementado con Tailwind CSS. Usar cuando el usuario quiere interfaces con estética de revista impresa o digital de alta gama: grids asimétricos, tipografía serif dramática con contraste de tamaños extremos, columnas de texto, uso expresivo del espacio negativo, jerarquía visual clara y paleta contenida (blanco/negro + 1 acento). Ideal para blogs premium, revistas digitales, portfolios de escritores/fotógrafos, newsletters visuales, landing pages editoriales y medios de comunicación. Incluye tailwind.config.js completo, @layer components y HTML de ejemplo.
---

# SKILL: Editorial / Magazine con Tailwind CSS

## Concepto

**Editorial/Magazine** traslada los principios del diseño gráfico de revista al digital: la tiranía de la tipografía (tamaños extremos, contraste de pesos), el grid de columnas como estructura invisible, el espacio en blanco como elemento de diseño, y el uso de UNA imagen o elemento visual que domina la página.

Referentes: The New York Times digital, Monocle, Kinfolk magazine, The Atlantic, Vogue editorial, Bloomberg Businessweek, Pitchfork.

**La firma del Editorial:**
- Contraste tipográfico EXTREMO: display en 96-160px junto a body en 15px
- Grid de columnas asimétrico (no todo 50/50 — quizás 65/35 o 3/4 + 1/4)
- Espacio en blanco abundante y deliberado
- Paleta de 2-3 colores máximo: generalmente blanco/negro + 1 acento
- Imágenes que sangran hasta el borde (full bleed)
- Separadores tipográficos y numeración visible
- Pull quotes y capitulares

---

## tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,jsx,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'ed': {
          // Base — blanco y negro puros con matiz
          'ink':     '#0A0A0A',   // negro editorial (casi-negro, no puro)
          'paper':   '#FAFAF8',   // blanco papel (ligeramente cálido)
          'cream':   '#F5F0E8',   // crema para fondos secundarios
          'gray':    '#888884',   // gris medio para metadatos
          'gray-lt': '#D4D4D0',   // gris claro para bordes y separadores

          // Acento — elegir UNO por proyecto
          'red':     '#C8102E',   // rojo editorial (The Economist, Vogue)
          'blue':    '#003087',   // azul de periódico
          'amber':   '#D4870A',   // ámbar cálido (Monocle-like)
          'teal':    '#006B6B',   // teal premium
          'sage':    '#4A6741',   // verde sage (Kinfolk-like)
        },
      },

      fontFamily: {
        // Serif dramático para display y titulares
        'display':  ['Playfair Display', 'Georgia', 'serif'],
        'serif':    ['Lora', 'Georgia', 'serif'],
        // Sans-serif limpio para cuerpo y UI
        'sans-ed':  ['DM Sans', 'Helvetica Neue', 'sans-serif'],
        // Condensado para categorías y labels
        'condensed':['Barlow Condensed', 'Arial Narrow', 'sans-serif'],
        // Monospace para números y datos
        'mono-ed':  ['DM Mono', 'Courier New', 'monospace'],
      },

      fontSize: {
        // Escala tipográfica editorial — contrastes extremos
        'display-sm': ['clamp(3rem,6vw,5rem)', { lineHeight: '1.05', letterSpacing: '-0.02em' }],
        'display-md': ['clamp(4rem,8vw,7rem)', { lineHeight: '1.0',  letterSpacing: '-0.03em' }],
        'display-lg': ['clamp(5rem,10vw,10rem)',{ lineHeight: '0.95', letterSpacing: '-0.04em' }],
        'display-xl': ['clamp(6rem,14vw,14rem)',{ lineHeight: '0.9',  letterSpacing: '-0.05em' }],
        'kicker':     ['0.65rem', { lineHeight: '1', letterSpacing: '0.2em' }],
        'caption':    ['0.75rem', { lineHeight: '1.5', letterSpacing: '0.02em' }],
        'meta':       ['0.7rem',  { lineHeight: '1.4', letterSpacing: '0.05em' }],
      },

      lineHeight: {
        'editorial': '1.65',  // para cuerpo de texto largo
        'tight-ed':  '1.08',  // para titulares comprimidos
      },

      spacing: {
        // Espaciados editoriales — generosos
        'col':  '1.5rem',   // gap entre columnas
        'gutter': '4rem',   // margen lateral base
        'section': '8rem',  // separación entre secciones
      },

      maxWidth: {
        'article': '68ch',    // ancho óptimo de columna de texto
        'article-wide': '80ch',
        'headline': '16ch',   // titular corto e impactante
      },

      animation: {
        'ed-reveal':  'edReveal 0.8s cubic-bezier(0.16,1,0.3,1) forwards',
        'ed-slide':   'edSlide 0.6s cubic-bezier(0.16,1,0.3,1) forwards',
        'line-grow':  'lineGrow 0.5s ease forwards',
      },
      keyframes: {
        edReveal: {
          '0%':   { opacity: '0', transform: 'translateY(40px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        edSlide: {
          '0%':   { opacity: '0', transform: 'translateX(-30px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        lineGrow: {
          '0%':   { transform: 'scaleX(0)', transformOrigin: 'left' },
          '100%': { transform: 'scaleX(1)', transformOrigin: 'left' },
        },
      },
    },
  },
  plugins: [],
}
```

---

## CSS Base (@layer)

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&family=Barlow+Condensed:wght@500;700&family=DM+Mono:wght@400&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-ed-paper font-sans-ed text-ed-ink;
    font-size: 16px;
    -webkit-font-smoothing: antialiased;
  }

  /* Titulares con la fuente serif dramática */
  h1, h2, h3, h4 {
    @apply font-display text-ed-ink;
  }

  /* Cuerpo de artículo largo — siempre serif */
  .article-body p {
    @apply font-serif text-ed-ink text-base leading-editorial max-w-article;
    @apply mb-6;
  }

  /* Capitular */
  .article-body p:first-of-type::first-letter {
    @apply font-display text-6xl font-black float-left mr-3 mt-1 leading-none;
    color: inherit;
  }

  /* Selección de texto */
  ::selection {
    background: rgba(200, 16, 46, 0.15);
  }
}

@layer components {

  /* ── Kicker / Categoría (texto pequeño encima del titular) ── */
  .ed-kicker {
    @apply font-condensed text-kicker font-bold uppercase tracking-[0.2em];
    @apply text-ed-red border-b-2 border-ed-red pb-1 inline-block mb-4;
  }
  .ed-kicker-gray {
    @apply font-condensed text-kicker font-bold uppercase tracking-[0.2em];
    @apply text-ed-gray inline-block mb-4;
  }

  /* ── Titulares ── */
  .ed-headline-xl {
    @apply font-display font-black text-display-xl leading-tight-ed text-ed-ink;
  }
  .ed-headline-lg {
    @apply font-display font-black text-display-lg leading-tight-ed text-ed-ink;
  }
  .ed-headline-md {
    @apply font-display font-bold text-display-md leading-tight-ed text-ed-ink;
  }
  .ed-headline-sm {
    @apply font-display font-bold text-display-sm leading-tight-ed text-ed-ink;
  }

  /* Titular en itálica (muy editorial) */
  .ed-headline-italic {
    @apply font-display italic font-normal;
  }

  /* ── Deck / Subtítulo de artículo ── */
  .ed-deck {
    @apply font-serif text-lg text-ed-gray leading-relaxed max-w-article;
    @apply border-l-4 border-ed-ink pl-4;
  }

  /* ── Pull Quote ── */
  .ed-pullquote {
    @apply font-display italic text-3xl md:text-4xl font-normal leading-tight;
    @apply text-ed-ink border-t-2 border-b-2 border-ed-ink py-6 my-8;
    @apply text-center max-w-article-wide mx-auto;
  }
  .ed-pullquote cite {
    @apply font-sans-ed text-sm font-medium not-italic text-ed-gray mt-3 block;
  }

  /* ── Byline / Metadatos ── */
  .ed-byline {
    @apply flex items-center gap-4 font-sans-ed text-meta text-ed-gray;
    @apply border-t border-ed-gray-lt pt-4;
  }

  /* ── Cards de artículo ── */
  .ed-card {
    @apply border-t-2 border-ed-ink pt-6;
    @apply transition-all duration-300;
  }
  .ed-card:hover .ed-card-title {
    @apply text-ed-red;
    transition: color 0.2s;
  }
  .ed-card-title {
    @apply font-display font-bold text-xl md:text-2xl leading-tight;
    @apply text-ed-ink transition-colors duration-200 mb-3;
  }
  .ed-card-excerpt {
    @apply font-sans-ed text-sm text-ed-gray leading-relaxed mb-4 max-w-article;
  }
  .ed-card-meta {
    @apply font-sans-ed text-meta text-ed-gray uppercase tracking-wider;
  }

  /* Card hero (imagen full + overlay) */
  .ed-card-hero {
    @apply relative overflow-hidden aspect-video;
  }
  .ed-card-hero-content {
    @apply absolute bottom-0 left-0 right-0 p-8;
    background: linear-gradient(transparent, rgba(10,10,10,0.9));
  }

  /* ── Navbar editorial ── */
  .ed-nav {
    @apply flex items-center justify-between px-gutter py-5;
    @apply border-b-2 border-ed-ink;
  }
  .ed-nav-logo {
    @apply font-display font-black text-2xl md:text-3xl tracking-tight text-ed-ink;
  }
  .ed-nav-link {
    @apply font-condensed font-bold text-xs uppercase tracking-[0.15em];
    @apply text-ed-gray hover:text-ed-ink transition-colors duration-150;
  }

  /* ── Issue number / Edición ── */
  .ed-issue {
    @apply font-mono-ed text-meta text-ed-gray;
  }

  /* ── Separador editorial ── */
  .ed-rule {
    @apply border-none h-px bg-ed-ink my-8;
  }
  .ed-rule-light {
    @apply border-none h-px bg-ed-gray-lt my-6;
  }
  .ed-rule-thick {
    @apply border-none h-1 bg-ed-ink mb-6;
  }

  /* ── Número de sección gigante ── */
  .ed-section-num {
    @apply font-display font-black text-[180px] leading-none text-ed-gray-lt;
    @apply select-none pointer-events-none;
  }

  /* ── Tag / Categoría pill ── */
  .ed-tag {
    @apply inline-block font-condensed text-xs font-bold uppercase tracking-widest;
    @apply px-3 py-1 border border-ed-gray text-ed-gray;
    @apply hover:bg-ed-ink hover:text-ed-paper hover:border-ed-ink transition-all duration-150;
  }
  .ed-tag-accent {
    @apply ed-tag bg-ed-red text-ed-paper border-ed-red;
    @apply hover:bg-red-800;
  }

  /* ── Botones editoriales ── */
  .ed-btn {
    @apply inline-flex items-center gap-3 font-condensed font-bold text-xs uppercase tracking-widest;
    @apply px-8 py-3.5 border-2 border-ed-ink text-ed-ink;
    @apply hover:bg-ed-ink hover:text-ed-paper transition-all duration-150 cursor-pointer;
  }
  .ed-btn-accent {
    @apply ed-btn bg-ed-red border-ed-red text-ed-paper;
    @apply hover:bg-red-800 hover:border-red-800;
  }
  .ed-btn-ghost {
    @apply inline-flex items-center gap-2 font-condensed font-bold text-xs uppercase tracking-widest;
    @apply text-ed-ink border-b-2 border-ed-ink pb-0.5;
    @apply hover:text-ed-red hover:border-ed-red transition-colors duration-150 cursor-pointer;
  }

  /* ── Columnas de texto ── */
  .ed-columns-2 {
    @apply md:columns-2 gap-12;
  }
  .ed-columns-3 {
    @apply md:columns-3 gap-8;
  }

  /* ── Caption de imagen ── */
  .ed-caption {
    @apply font-sans-ed text-caption text-ed-gray mt-2 leading-relaxed;
  }

  /* ── Animaciones ── */
  .ed-reveal { @apply animate-ed-reveal; }
  .ed-slide  { @apply animate-ed-slide; }
}

@layer utilities {
  /* Texto en negativo (útil para headers sobre imagen) */
  .text-paper { @apply text-ed-paper; }

  /* Ratio de imágenes editorial comunes */
  .aspect-cinema { aspect-ratio: 21/9; }
  .aspect-portrait { aspect-ratio: 3/4; }
  .aspect-square-lg { aspect-ratio: 1/1; }
}
```

---

## HTML — Componentes Listos

### Navbar con separador de secciones

```html
<header>
  <!-- Franja superior de categorías -->
  <div class="bg-ed-ink text-ed-paper py-2 px-gutter">
    <div class="flex items-center gap-6 max-w-7xl mx-auto">
      <a href="#" class="font-condensed text-xs font-bold uppercase tracking-widest text-ed-gray-lt hover:text-ed-paper transition-colors">Política</a>
      <a href="#" class="font-condensed text-xs font-bold uppercase tracking-widest text-ed-gray-lt hover:text-ed-paper transition-colors">Cultura</a>
      <a href="#" class="font-condensed text-xs font-bold uppercase tracking-widest text-ed-gray-lt hover:text-ed-paper transition-colors">Tecnología</a>
      <a href="#" class="font-condensed text-xs font-bold uppercase tracking-widest text-ed-gray-lt hover:text-ed-paper transition-colors">Economía</a>
    </div>
  </div>
  <!-- Logo + navegación principal -->
  <nav class="ed-nav max-w-7xl mx-auto">
    <div class="font-sans-ed text-xs text-ed-gray font-medium hidden md:block">
      Lunes, 19 de Abril de 2026
    </div>
    <span class="ed-nav-logo tracking-[-0.03em]">La Revista</span>
    <div class="flex items-center gap-6">
      <a href="#" class="ed-nav-link">Suscribirse</a>
      <button class="ed-btn-accent text-xs px-5 py-2">Edición digital</button>
    </div>
  </nav>
</header>
```

### Hero editorial (artículo principal)

```html
<section class="max-w-7xl mx-auto px-gutter py-16">
  <div class="grid grid-cols-1 lg:grid-cols-5 gap-12 items-start">

    <!-- Columna de texto — 3/5 del ancho -->
    <div class="lg:col-span-3">
      <div class="ed-kicker">Cultura Digital</div>

      <h1 class="ed-headline-lg mb-6">
        El diseño que<br/>
        <em class="ed-headline-italic">nunca envejece</em><br/>
        y el que muere<br/>
        con su época
      </h1>

      <p class="ed-deck mb-8">
        Una exploración de los sistemas visuales que trascienden modas y de aquellos
        que quedan inevitablemente atados al momento que los vio nacer.
      </p>

      <div class="ed-byline mb-8">
        <span>Por <strong class="text-ed-ink font-medium">María Fernanda Roca</strong></span>
        <span class="text-ed-gray-lt">•</span>
        <span>8 minutos de lectura</span>
        <span class="text-ed-gray-lt">•</span>
        <span class="font-mono-ed">Nº 142</span>
      </div>

      <button class="ed-btn-ghost">Continuar leyendo →</button>
    </div>

    <!-- Imagen — 2/5 del ancho -->
    <div class="lg:col-span-2">
      <div class="aspect-portrait bg-ed-gray-lt overflow-hidden">
        <img src="..." alt="..." class="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700" />
      </div>
      <p class="ed-caption">Portada del número 142. Fotografía: Archivo editorial.</p>
    </div>

  </div>
</section>
```

### Grid de artículos (estilo portada de revista)

```html
<section class="max-w-7xl mx-auto px-gutter pb-20">
  <div class="ed-rule-thick"></div>

  <!-- Artículo principal (full width) -->
  <div class="grid grid-cols-1 md:grid-cols-12 gap-8 mb-16 pb-16 border-b border-ed-gray-lt">
    <div class="md:col-span-5 aspect-video bg-ed-gray-lt overflow-hidden">
      <img src="..." alt="" class="w-full h-full object-cover" />
    </div>
    <div class="md:col-span-7 flex flex-col justify-center">
      <div class="ed-kicker-gray">Entrevista</div>
      <h2 class="ed-headline-sm mb-4">
        "El software no es neutro: cada elección de diseño
        es una declaración política"
      </h2>
      <p class="ed-card-excerpt">
        Conversación con la diseñadora Valeria Amstutz sobre accesibilidad,
        poder y la responsabilidad de quienes dan forma a las interfaces.
      </p>
      <div class="ed-byline">
        <span>Entrevista: Juan Roccia</span>
        <span class="text-ed-gray-lt">•</span>
        <span>12 min</span>
      </div>
    </div>
  </div>

  <!-- Grid de 3 artículos secundarios -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-8">

    <div class="ed-card">
      <span class="ed-tag mb-3 inline-block">Ensayo</span>
      <h3 class="ed-card-title">La dictadura del scroll infinito y el fin de la lectura profunda</h3>
      <p class="ed-card-excerpt">Cada año leemos más palabras y entendemos menos...</p>
      <div class="ed-card-meta">7 min • Tecnología</div>
    </div>

    <div class="ed-card">
      <span class="ed-tag mb-3 inline-block">Opinión</span>
      <h3 class="ed-card-title">Por qué todos los logos modernos se parecen entre sí</h3>
      <p class="ed-card-excerpt">El mercado global aplana la identidad visual a mínimos compartidos...</p>
      <div class="ed-card-meta">5 min • Diseño</div>
    </div>

    <div class="ed-card">
      <span class="ed-tag-accent mb-3 inline-block">Imperdible</span>
      <h3 class="ed-card-title">Los tipógrafos que todavía diseñan fuentes a mano en 2026</h3>
      <p class="ed-card-excerpt">En un taller de Buenos Aires, cuatro artesanos resisten...</p>
      <div class="ed-card-meta">11 min • Cultura</div>
    </div>

  </div>
</section>
```

### Artículo completo (cuerpo de texto)

```html
<article class="max-w-7xl mx-auto px-gutter py-16">
  <div class="max-w-3xl mx-auto">

    <!-- Encabezado del artículo -->
    <div class="ed-kicker">Análisis</div>
    <h1 class="ed-headline-md mb-6">El minimalismo como ideología</h1>
    <div class="ed-deck mb-8">
      Cuando "menos es más" se convierte en dogma, el diseño pierde su capacidad de
      expresar complejidad, textura y contradicción humana.
    </div>
    <div class="ed-byline mb-12">
      <span>Por <strong>Carlos Mendieta</strong></span>
      <span class="text-ed-gray-lt">•</span>
      <time>14 de Abril, 2026</time>
      <span class="text-ed-gray-lt">•</span>
      <span>15 minutos</span>
    </div>

    <!-- Cuerpo del artículo -->
    <div class="article-body">
      <p>
        Hay algo paradójico en el triunfo del minimalismo: una estética nacida como
        reacción al exceso burgués se convirtió, en pocas décadas, en el lenguaje
        visual del lujo contemporáneo.
      </p>

      <!-- Pull quote -->
      <blockquote class="ed-pullquote">
        "El minimalismo no elimina el contenido, simplemente esconde
        el trabajo que costó reducirlo."
        <cite>— Dieter Rams, 1976</cite>
      </blockquote>

      <p>
        Los principios de Dieter Rams siguen siendo citados en cada pitch de diseño
        corporativo, en cada manual de marca de startup, en cada presentación de
        producto tecnológico...
      </p>
    </div>

  </div>
</article>
```

### Sección con número gigante decorativo

```html
<section class="relative max-w-7xl mx-auto px-gutter py-20 overflow-hidden">
  <!-- Número decorativo de fondo -->
  <div class="ed-section-num absolute -top-8 -left-4 select-none pointer-events-none">
    03
  </div>

  <div class="relative">
    <div class="ed-kicker">Sección 3</div>
    <h2 class="ed-headline-sm max-w-headline">Opinión y análisis</h2>
  </div>
</section>
```

---

## Patrones de Grid Editorial

```html
<!-- 2 columnas asimétricas (70/30) -->
<div class="grid grid-cols-10 gap-8">
  <div class="col-span-7"><!-- contenido principal --></div>
  <div class="col-span-3"><!-- sidebar --></div>
</div>

<!-- Artículo con imagen que sangra a la derecha -->
<div class="grid grid-cols-2">
  <div class="p-16"><!-- texto --></div>
  <div class="aspect-auto"><!-- imagen full bleed --></div>
</div>

<!-- 3 columnas de artículos iguales -->
<div class="grid grid-cols-3 divide-x divide-ed-gray-lt">
  <div class="px-6 first:pl-0 last:pr-0"><!-- artículo --></div>
  <div class="px-6"><!-- artículo --></div>
  <div class="px-6 first:pl-0 last:pr-0"><!-- artículo --></div>
</div>
```

---

## Anti-patrones a Evitar

- ❌ Más de 1-2 colores de acento — editorial es contenido, no decoración
- ❌ `rounded-xl`, `rounded-full` en cards — las cards editoriales tienen esquinas rectas
- ❌ Tipografía sans-serif como display — siempre serif para titulares principales
- ❌ Animaciones llamativas o bouncy — las transiciones son sutiles y funcionales
- ❌ Gradientes de color en fondos — editorial usa fondos planos (blanco, negro, crema)
- ❌ `font-normal` o `font-light` en titulares — siempre `font-bold` o `font-black`
- ❌ Centrar todos los textos — el texto editorial se alinea a la izquierda (excepto pull quotes)
- ❌ Padding/margin pequeños — editorial necesita espaciado generoso para respirar

---

## Casos de Uso Ideales

- Revistas digitales y newsletters visuales de calidad
- Blogs de largo plazo con contenido de profundidad
- Portfolios de escritores, periodistas, fotógrafos
- Medios de comunicación y periodismo de datos
- Landing pages de libros o publicaciones
- Sitios de agencias con trabajo que habla por sí mismo
- Portafolios de diseño que demuestran criterio tipográfico
