---
name: frosted-glass-tailwind
description: Diseño Frosted Glass / Glassmorphism implementado con Tailwind CSS. Usar cuando el usuario quiere interfaces con efecto vidrio esmerilado usando clases de Tailwind, con configuración extendida para transparencias, backdrop-blur y gradientes de fondo. Incluye tailwind.config.js, componentes con @apply y HTML de ejemplo listo para usar.
---

# SKILL: Frosted Glass con Tailwind CSS

## Concepto

Tailwind tiene soporte nativo para casi todo el Glassmorphism:
- `backdrop-blur-*` → `backdrop-filter: blur()`
- `bg-white/10` → `background: rgba(255,255,255,0.1)`
- `border-white/25` → `border-color: rgba(255,255,255,0.25)`
- `rounded-2xl`, `rounded-3xl` → border-radius

Lo que **no cubre nativamente** y requiere config o CSS custom:
- Gradientes de fondo tipo mesh con múltiples stops
- `backdrop-filter: blur() saturate()` combinado
- Sombra inset + sombra externa en una misma utilidad
- Orbes de color de fondo (pseudo-elementos)

---

## tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,jsx,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Acentos de vidrio
        'glass-purple': '#a78bfa',
        'glass-teal':   '#34d399',
        'glass-pink':   '#f472b6',
        'glass-blue':   '#60a5fa',
      },
      backdropBlur: {
        xs: '4px',
        '2xl': '40px',
        '3xl': '60px',
      },
      backgroundImage: {
        'glass-gradient': 'linear-gradient(135deg, #1a1a4e 0%, #6c3fa0 40%, #00c9a7 100%)',
        'glass-gradient-dark': 'linear-gradient(135deg, #0f0c29, #302b63, #24243e)',
      },
      boxShadow: {
        'glass':    '0 8px 32px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.4)',
        'glass-sm': '0 4px 16px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.3)',
        'glass-lg': '0 16px 48px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.5)',
        'glow-purple': '0 0 20px rgba(167,139,250,0.4)',
        'glow-teal':   '0 0 20px rgba(52,211,153,0.4)',
      },
      fontFamily: {
        outfit: ['Outfit', 'sans-serif'],
        'dm-sans': ['DM Sans', 'sans-serif'],
      },
      animation: {
        'glass-reveal': 'glassReveal 0.5s cubic-bezier(0.16,1,0.3,1) forwards',
      },
      keyframes: {
        glassReveal: {
          '0%':   { opacity: '0', transform: 'translateY(20px) scale(0.97)' },
          '100%': { opacity: '1', transform: 'translateY(0) scale(1)' },
        },
      },
    },
  },
  plugins: [],
}
```

---

## CSS Base (@layer)

Agregar en el archivo CSS principal (ej: `globals.css` o `index.css`):

```css
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=DM+Sans:wght@400;500&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply font-dm-sans min-h-screen overflow-x-hidden;
    background: linear-gradient(135deg, #1a1a4e 0%, #6c3fa0 40%, #00c9a7 100%);
    position: relative;
  }

  /* Orbes de fondo — no hay equivalente en Tailwind puro */
  body::before {
    content: '';
    position: fixed;
    width: 500px; height: 500px;
    border-radius: 50%;
    background: #a855f7;
    top: -100px; left: -100px;
    filter: blur(80px);
    opacity: 0.5;
    z-index: 0;
    pointer-events: none;
  }
  body::after {
    content: '';
    position: fixed;
    width: 400px; height: 400px;
    border-radius: 50%;
    background: #06b6d4;
    bottom: -80px; right: -80px;
    filter: blur(80px);
    opacity: 0.5;
    z-index: 0;
    pointer-events: none;
  }
}

@layer components {
  /* Card normal */
  .glass-card {
    @apply bg-white/[0.12] backdrop-blur-xl border border-white/25 rounded-2xl p-8;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.4);
    /* saturate() no tiene clase Tailwind — necesita inline o CSS */
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    backdrop-filter: blur(20px) saturate(180%);
  }

  /* Variante sutil (fondo de sección) */
  .glass-card-subtle {
    @apply bg-white/[0.06] backdrop-blur-md border border-white/10 rounded-2xl;
    -webkit-backdrop-filter: blur(10px);
  }

  /* Variante fuerte (modales) */
  .glass-card-strong {
    @apply bg-white/[0.2] backdrop-blur-2xl border border-white/30 rounded-2xl;
    box-shadow: 0 16px 48px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.5);
    -webkit-backdrop-filter: blur(30px) saturate(200%);
  }

  /* Dark glass overlay */
  .glass-dark {
    @apply bg-black/35 backdrop-blur-xl border border-white/10 rounded-2xl;
  }

  /* Navbar flotante */
  .glass-nav {
    @apply fixed top-4 left-1/2 -translate-x-1/2 w-[90%] max-w-4xl z-50;
    @apply bg-white/[0.08] backdrop-blur-2xl border border-white/15 rounded-full px-6 py-3;
    -webkit-backdrop-filter: blur(24px);
  }

  /* Botón principal */
  .glass-btn {
    @apply bg-violet-400/30 border border-violet-400/50 text-white;
    @apply px-6 py-2.5 rounded-full cursor-pointer transition-all duration-300;
    @apply hover:-translate-y-0.5 hover:bg-violet-400/50 hover:shadow-glow-purple;
    @apply backdrop-blur-sm font-medium text-sm;
  }

  /* Botón secundario (outline) */
  .glass-btn-outline {
    @apply bg-transparent border border-white/30 text-white/80;
    @apply px-6 py-2.5 rounded-full cursor-pointer transition-all duration-300;
    @apply hover:bg-white/10 hover:border-white/50 hover:text-white;
  }

  /* Input */
  .glass-input {
    @apply w-full bg-white/[0.07] border border-white/20 text-white rounded-xl;
    @apply px-4 py-3 outline-none transition-all duration-200;
    @apply placeholder:text-white/40;
    @apply focus:border-violet-400/70 focus:bg-white/10;
  }

  /* Badge */
  .glass-badge {
    @apply inline-flex items-center bg-white/10 border border-white/20;
    @apply rounded-full px-3 py-1 text-xs text-white/80 font-medium;
    @apply backdrop-blur-sm;
  }

  /* Stat card */
  .glass-stat {
    @apply glass-card text-center;
  }
}

@layer utilities {
  /* Fallback para navegadores sin backdrop-filter */
  @supports not (backdrop-filter: blur(1px)) {
    .glass-card,
    .glass-card-subtle,
    .glass-card-strong {
      @apply bg-indigo-950/85;
    }
  }
}
```

---

## HTML — Componentes Listos

### Layout base

```html
<!-- En el body se aplican los orbes automáticamente via ::before/::after -->
<div class="relative z-10 min-h-screen">
  <!-- contenido aquí -->
</div>
```

### Navbar flotante

```html
<nav class="glass-nav flex items-center justify-between">
  <span class="font-outfit font-bold text-white text-lg tracking-tight">Brand</span>
  <div class="flex items-center gap-6">
    <a href="#" class="text-white/70 hover:text-white text-sm transition-colors">Inicio</a>
    <a href="#" class="text-white/70 hover:text-white text-sm transition-colors">Producto</a>
    <a href="#" class="text-white/70 hover:text-white text-sm transition-colors">Precios</a>
    <button class="glass-btn text-sm">Empezar</button>
  </div>
</nav>
```

### Card principal

```html
<div class="glass-card animate-glass-reveal">
  <div class="flex items-center gap-3 mb-4">
    <div class="glass-badge">⚡ Nuevo</div>
  </div>
  <h2 class="font-outfit font-bold text-2xl text-white mb-2">
    Título de la card
  </h2>
  <p class="text-white/60 text-sm leading-relaxed mb-6">
    Descripción del contenido. El texto secundario tiene opacidad reducida.
  </p>
  <div class="flex gap-3">
    <button class="glass-btn">Acción principal</button>
    <button class="glass-btn-outline">Ver más</button>
  </div>
</div>
```

### Grid de cards

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-8">
  <div class="glass-card">...</div>
  <div class="glass-card">...</div>
  <div class="glass-card">...</div>
</div>
```

### Formulario / Login

```html
<div class="glass-card-strong max-w-md mx-auto p-10">
  <h2 class="font-outfit font-bold text-3xl text-white mb-1">Iniciar sesión</h2>
  <p class="text-white/50 text-sm mb-8">Bienvenido de nuevo</p>

  <div class="space-y-4">
    <div>
      <label class="text-white/60 text-xs uppercase tracking-widest mb-2 block">Email</label>
      <input type="email" placeholder="tu@email.com" class="glass-input" />
    </div>
    <div>
      <label class="text-white/60 text-xs uppercase tracking-widest mb-2 block">Contraseña</label>
      <input type="password" placeholder="••••••••" class="glass-input" />
    </div>
  </div>

  <button class="glass-btn w-full justify-center mt-6 py-3">
    Ingresar
  </button>
</div>
```

### Stat / Métrica

```html
<div class="glass-stat">
  <div class="text-4xl font-outfit font-bold text-white mb-1">$12.4K</div>
  <div class="text-white/40 text-xs uppercase tracking-widest">Ingresos del mes</div>
  <div class="mt-3 flex items-center justify-center gap-1 text-emerald-400 text-sm">
    <span>↑</span>
    <span>+18.2%</span>
  </div>
</div>
```

### Modal

```html
<!-- Overlay -->
<div class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
  <!-- Modal -->
  <div class="glass-card-strong max-w-lg w-full">
    <div class="flex items-center justify-between mb-6">
      <h3 class="font-outfit font-bold text-xl text-white">Confirmar acción</h3>
      <button class="text-white/40 hover:text-white transition-colors text-xl">✕</button>
    </div>
    <p class="text-white/60 mb-8">¿Estás seguro que querés continuar con esta operación?</p>
    <div class="flex gap-3 justify-end">
      <button class="glass-btn-outline">Cancelar</button>
      <button class="glass-btn">Confirmar</button>
    </div>
  </div>
</div>
```

---

## Clases de Tailwind Nativas más Usadas

| Efecto | Clase Tailwind |
|--------|---------------|
| `background: rgba(255,255,255,0.1)` | `bg-white/10` |
| `background: rgba(255,255,255,0.12)` | `bg-white/[0.12]` |
| `border-color: rgba(255,255,255,0.25)` | `border-white/25` |
| `backdrop-filter: blur(8px)` | `backdrop-blur-sm` |
| `backdrop-filter: blur(12px)` | `backdrop-blur-md` |
| `backdrop-filter: blur(16px)` | `backdrop-blur-xl` |
| `backdrop-filter: blur(24px)` | `backdrop-blur-2xl` |
| `border-radius: 20px` | `rounded-2xl` |
| `border-radius: 9999px` | `rounded-full` |
| `color: rgba(255,255,255,0.7)` | `text-white/70` |
| `color: rgba(255,255,255,0.45)` | `text-white/45` |

---

## ⚠️ Limitaciones de Tailwind para Glassmorphism

| Necesidad | Solución |
|-----------|---------|
| `backdrop-filter: blur() saturate()` combinado | Usar `style=""` inline o CSS custom |
| `inset` box-shadow + outer box-shadow | Definir en `extend.boxShadow` del config |
| Orbes de fondo con `::before` / `::after` | Solo en CSS (Tailwind no genera pseudo-elementos con contenido dinámico) |
| Animación de blur en `@keyframes` | Solo en CSS custom (`backdrop-filter` no es animable en Tailwind) |

---

## Anti-patrones a Evitar

- ❌ `bg-white` o `bg-black` como base — sin alpha el vidrio no se ve
- ❌ `backdrop-blur-none` dentro de un container con `backdrop-blur` — anida mal
- ❌ `shadow-xl` de Tailwind (tiene color gris genérico) — usar `shadow-glass` del config
- ❌ Olvidar el `-webkit-backdrop-filter` — Safari no lo soporta sin prefijo
- ❌ `z-index` sin `position: relative` en el contenedor padre — el blur no se aplica

---

## Casos de Uso Ideales

- Dashboards financieros / crypto
- Landing pages de productos tech
- Paneles de autenticación (login / register)
- Widgets de métricas y KPIs sobre imagen de fondo
- Apps de música / streaming
- Portfolios creativos
