---
name: neobrutalism-tailwind
description: Diseño Neobrutalism implementado con Tailwind CSS. Usar cuando el usuario quiere interfaces con bordes duros negros, sombras offset sin blur, colores planos y tipografía pesada usando clases de Tailwind con configuración extendida. Incluye tailwind.config.js, componentes con @apply y HTML de ejemplo.
---

# SKILL: Neobrutalism con Tailwind CSS

## Concepto

Neobrutalism es el estilo más compatible con Tailwind porque sus reglas son directas:
- `border-2 border-black` → bordes duros ✅ nativo
- `rounded` o `rounded-sm` → radius mínimo ✅ nativo
- `bg-yellow-400`, `bg-blue-600` → colores planos ✅ nativo
- `font-black`, `uppercase`, `tracking-tight` → tipografía pesada ✅ nativo

Lo que **requiere config o @apply**:
- Sombras offset sin blur (no están en las shadows default de Tailwind)
- Colores específicos del estilo (crema, negro exacto `#0D0D0D`)
- Hover con `translate + shadow` combinados

---

## tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,jsx,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'neo-black':  '#0D0D0D',
        'neo-white':  '#FFFBF5',   // crema off-white
        'neo-yellow': '#FFE600',
        'neo-coral':  '#FF6B6B',
        'neo-mint':   '#00F5C4',
        'neo-blue':   '#0057FF',
        'neo-orange': '#FF8C00',
        'neo-pink':   '#FF3CAC',
        'neo-lime':   '#CCFF00',
        'neo-lavender': '#F0E6FF',
      },
      boxShadow: {
        // La firma del neobrutalism: offset sin blur
        'neo':     '4px 4px 0px #0D0D0D',
        'neo-sm':  '2px 2px 0px #0D0D0D',
        'neo-lg':  '6px 6px 0px #0D0D0D',
        'neo-xl':  '8px 8px 0px #0D0D0D',
        // Hover (reducido, se combina con translate)
        'neo-hover': '2px 2px 0px #0D0D0D',
        // Foco de input en azul
        'neo-focus': '4px 4px 0px #0057FF',
        // Variante dark (sobre fondo negro)
        'neo-light': '4px 4px 0px #FFFBF5',
      },
      borderWidth: {
        '3': '3px',
      },
      fontFamily: {
        'space': ['Space Grotesk', 'sans-serif'],
        'mono':  ['DM Mono', 'monospace'],
        'archivo': ['Archivo Black', 'sans-serif'],
      },
      letterSpacing: {
        'neo': '0.05em',
        'neo-wide': '0.08em',
      },
      transitionDuration: {
        '100': '100ms',
        '120': '120ms',
      },
    },
  },
  plugins: [],
}
```

---

## CSS Base (@layer)

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800&family=DM+Mono:wght@500&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-neo-white font-space text-neo-black;
    /* Para variante dark: @apply bg-neo-black text-neo-white; */
  }

  h1, h2, h3 {
    @apply font-black uppercase tracking-tight leading-none;
    letter-spacing: -0.02em;
  }
}

@layer components {
  /* Card base */
  .neo-card {
    @apply bg-neo-white border-2 border-neo-black shadow-neo rounded p-6;
    @apply transition-all duration-100 cursor-default;
  }
  .neo-card:hover {
    @apply shadow-neo-hover translate-x-0.5 translate-y-0.5;
  }

  /* Botón primario (amarillo) */
  .neo-btn {
    @apply bg-neo-yellow text-neo-black border-2 border-neo-black shadow-neo rounded;
    @apply px-5 py-2.5 font-bold text-sm uppercase tracking-neo cursor-pointer;
    @apply transition-all duration-[120ms] select-none;
  }
  .neo-btn:hover {
    @apply shadow-neo-hover translate-x-0.5 translate-y-0.5;
  }
  .neo-btn:active {
    @apply shadow-none translate-x-1 translate-y-1;
  }

  /* Botón outline */
  .neo-btn-outline {
    @apply bg-transparent text-neo-black border-2 border-neo-black shadow-neo rounded;
    @apply px-5 py-2.5 font-bold text-sm uppercase tracking-neo cursor-pointer;
    @apply transition-all duration-[120ms] select-none;
  }
  .neo-btn-outline:hover {
    @apply shadow-neo-hover translate-x-0.5 translate-y-0.5;
  }
  .neo-btn-outline:active {
    @apply shadow-none translate-x-1 translate-y-1;
  }

  /* Botón acento personalizable — usar bg-* inline */
  .neo-btn-accent {
    @apply border-2 border-neo-black shadow-neo rounded;
    @apply px-5 py-2.5 font-bold text-sm uppercase tracking-neo cursor-pointer;
    @apply transition-all duration-[120ms] select-none;
  }
  .neo-btn-accent:hover  { @apply shadow-neo-hover translate-x-0.5 translate-y-0.5; }
  .neo-btn-accent:active { @apply shadow-none translate-x-1 translate-y-1; }

  /* Input */
  .neo-input {
    @apply bg-white border-2 border-neo-black shadow-neo rounded;
    @apply px-4 py-2.5 text-base font-medium outline-none w-full;
    @apply transition-all duration-[120ms];
    @apply placeholder:text-gray-400;
  }
  .neo-input:focus {
    @apply shadow-neo-focus border-neo-blue;
  }

  /* Badge / Tag */
  .neo-badge {
    @apply inline-block bg-neo-yellow border-2 border-neo-black rounded;
    @apply px-2.5 py-0.5 text-xs font-bold uppercase tracking-neo-wide;
  }

  /* Navbar */
  .neo-navbar {
    @apply bg-neo-white border-b-2 border-neo-black;
    @apply flex items-center justify-between px-8 py-4;
  }

  /* Hero section */
  .neo-hero {
    @apply bg-neo-yellow border-b-3 border-neo-black;
    @apply px-8 py-24 relative;
  }

  /* Divider */
  .neo-divider {
    @apply border-0 border-t-3 border-neo-black my-8;
  }

  /* Highlight de texto */
  .neo-highlight {
    @apply bg-neo-yellow rounded-sm px-1;
  }

  /* Text outline decorativo */
  .neo-text-outline {
    color: transparent;
    -webkit-text-stroke: 2px #0D0D0D;
  }
}
```

---

## HTML — Componentes Listos

### Navbar

```html
<nav class="neo-navbar">
  <span class="font-black text-xl uppercase tracking-tight">MiApp</span>
  <div class="flex items-center gap-4">
    <a href="#" class="font-bold text-sm uppercase hover:underline">Producto</a>
    <a href="#" class="font-bold text-sm uppercase hover:underline">Precios</a>
    <button class="neo-btn text-xs">Empezar →</button>
  </div>
</nav>
```

### Hero Section

```html
<section class="neo-hero">
  <!-- Marca de esquina decorativa -->
  <div class="absolute top-0 right-0 w-4 h-4 bg-neo-yellow border-2 border-neo-black"></div>

  <div class="max-w-4xl">
    <span class="neo-badge mb-6 inline-block">✦ Nuevo lanzamiento</span>
    <h1 class="text-6xl md:text-8xl font-black uppercase leading-none tracking-tight mb-6">
      La herramienta<br/>
      <span class="neo-text-outline">que necesitás</span>
    </h1>
    <p class="text-lg font-medium text-gray-700 max-w-lg mb-8">
      Una descripción directa y sin rodeos de lo que hace el producto.
    </p>
    <div class="flex items-center gap-4 flex-wrap">
      <button class="neo-btn text-base px-8 py-3">Probar gratis</button>
      <button class="neo-btn-outline text-base px-8 py-3">Ver demo</button>
    </div>
  </div>
</section>
```

### Grid de Cards

```html
<!-- Grid con bordes fusionados — estilo neobrutalist -->
<div class="grid grid-cols-1 md:grid-cols-3">
  <div class="border-2 border-neo-black p-6 -m-px">
    <div class="neo-badge mb-4">Feature 01</div>
    <h3 class="text-xl font-black uppercase mb-2">Velocidad real</h3>
    <p class="text-gray-600 font-medium text-sm">Sin límites artificiales ni capas de abstracción innecesarias.</p>
  </div>
  <div class="border-2 border-neo-black p-6 -m-px bg-neo-yellow">
    <div class="neo-badge mb-4">Feature 02</div>
    <h3 class="text-xl font-black uppercase mb-2">Sin vendor lock</h3>
    <p class="text-gray-700 font-medium text-sm">Tu data es tuya. Siempre. Sin excepciones.</p>
  </div>
  <div class="border-2 border-neo-black p-6 -m-px">
    <div class="neo-badge mb-4">Feature 03</div>
    <h3 class="text-xl font-black uppercase mb-2">Open source</h3>
    <p class="text-gray-600 font-medium text-sm">Código abierto, auditado y listo para producción.</p>
  </div>
</div>
```

### Card standalone

```html
<div class="neo-card max-w-sm">
  <div class="flex items-start justify-between mb-4">
    <span class="neo-badge">Pro</span>
    <span class="font-black text-2xl">$29/mes</span>
  </div>
  <h3 class="text-xl font-black uppercase mb-3">Plan Profesional</h3>
  <ul class="space-y-2 mb-6">
    <li class="flex items-center gap-2 font-medium text-sm">
      <span class="text-neo-black font-black">✓</span> Proyectos ilimitados
    </li>
    <li class="flex items-center gap-2 font-medium text-sm">
      <span class="text-neo-black font-black">✓</span> Soporte prioritario
    </li>
    <li class="flex items-center gap-2 font-medium text-sm">
      <span class="text-neo-black font-black">✓</span> API completa
    </li>
  </ul>
  <button class="neo-btn w-full text-center justify-center">Elegir plan</button>
</div>
```

### Formulario

```html
<div class="neo-card max-w-md">
  <h2 class="text-2xl font-black uppercase mb-6">Contacto</h2>
  <div class="space-y-4">
    <div>
      <label class="block font-bold text-xs uppercase tracking-neo mb-1.5">Nombre</label>
      <input type="text" placeholder="Tu nombre" class="neo-input" />
    </div>
    <div>
      <label class="block font-bold text-xs uppercase tracking-neo mb-1.5">Email</label>
      <input type="email" placeholder="tu@email.com" class="neo-input" />
    </div>
    <div>
      <label class="block font-bold text-xs uppercase tracking-neo mb-1.5">Mensaje</label>
      <textarea rows="4" placeholder="Tu mensaje..." class="neo-input resize-none"></textarea>
    </div>
  </div>
  <button class="neo-btn w-full mt-5 py-3 text-base">Enviar →</button>
</div>
```

### Tabla de datos

```html
<div class="border-2 border-neo-black rounded overflow-hidden shadow-neo">
  <table class="w-full">
    <thead class="bg-neo-black text-neo-white">
      <tr>
        <th class="px-4 py-3 text-left text-xs uppercase tracking-neo font-bold">Nombre</th>
        <th class="px-4 py-3 text-left text-xs uppercase tracking-neo font-bold">Estado</th>
        <th class="px-4 py-3 text-left text-xs uppercase tracking-neo font-bold">Monto</th>
      </tr>
    </thead>
    <tbody>
      <tr class="border-t-2 border-neo-black hover:bg-neo-yellow/30 transition-colors">
        <td class="px-4 py-3 font-bold text-sm">InmoGestion Pro</td>
        <td class="px-4 py-3"><span class="neo-badge text-xs">Activo</span></td>
        <td class="px-4 py-3 font-black">$1.200</td>
      </tr>
      <tr class="border-t-2 border-neo-black hover:bg-neo-yellow/30 transition-colors">
        <td class="px-4 py-3 font-bold text-sm">BuscoInmuebles</td>
        <td class="px-4 py-3"><span class="neo-badge bg-neo-mint text-xs">Trial</span></td>
        <td class="px-4 py-3 font-black">$0</td>
      </tr>
    </tbody>
  </table>
</div>
```

---

## Referencia Rápida: Clases Nativas de Tailwind para Neobrutalism

| Propiedad | Clase Tailwind |
|-----------|---------------|
| `border: 2px solid #000` | `border-2 border-black` o `border-neo-black` |
| `border: 3px solid #000` | `border-[3px] border-black` |
| `border-radius: 4px` | `rounded` o `rounded-sm` |
| `border-radius: 0` | `rounded-none` |
| `font-weight: 900` | `font-black` |
| `text-transform: uppercase` | `uppercase` |
| `letter-spacing: -0.02em` | `tracking-tight` |
| `letter-spacing: 0.05em` | `tracking-neo` (config) |
| Color amarillo plano | `bg-neo-yellow` o `bg-yellow-400` |
| Translate hover | `hover:translate-x-0.5 hover:translate-y-0.5` |

---

## Anti-patrones a Evitar

- ❌ `shadow-xl` o `shadow-lg` de Tailwind (tienen blur — incompatible con el estilo)
- ❌ `rounded-xl`, `rounded-2xl` (demasiado suave para neobrutalism)
- ❌ `bg-opacity-*` o colores con alpha — neobrutalism usa colores 100% sólidos
- ❌ `transition-all duration-500` — las transiciones deben ser cortas (100-150ms)
- ❌ `font-normal` o `font-light` en títulos — siempre `font-bold` o `font-black`
- ❌ Más de 2 colores de acento — sobrecarga visual

---

## Casos de Uso Ideales

- Landing pages de startups / indie projects
- Tools y utilidades para desarrolladores
- Portfolios de diseñadores que quieren destacar
- SaaS con personalidad irreverente
- Webs de productos digitales (templates, plugins)
- Dashboards internos con estética de "herramienta real"
