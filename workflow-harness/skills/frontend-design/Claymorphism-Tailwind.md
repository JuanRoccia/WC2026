---
name: claymorphism-tailwind
description: Diseño Claymorphism implementado con Tailwind CSS. Usar cuando el usuario quiere interfaces con estética de plastilina / clay 3D: colores pastel saturados, sombras de color (no grises), bordes gruesos del mismo color más oscuro, efecto de inflado y sensación de juguete físico. Ideal para apps infantiles, productos creativos, onboarding, landing pages playful y cualquier UI que quiera sentirse cálida y amigable. Incluye tailwind.config.js completo, @layer components y HTML de ejemplo.
---

# SKILL: Claymorphism con Tailwind CSS

## Concepto

**Claymorphism** simula objetos hechos de plastilina o arcilla: formas infladas, colores pastel saturados, sombras de color (nunca gris neutro), y bordes que tienen el mismo matiz del elemento pero más oscuro. El resultado es táctil, 3D y extremadamente amigable.

Referentes: Notion avatars, apps de finanzas para jóvenes (Revolut Kids), onboarding de Duolingo, ilustraciones de Shapefest.

**La firma del Claymorphism:**
- Sombra de color (mismo hue del elemento, más oscuro, sin blur exagerado)
- `border` del mismo hue pero saturado y oscuro — no negro
- Forma ligeramente "inflada" (border-radius muy generoso, 24px+)
- Colores: pasteles MUY saturados, no lavados
- Fondo claro o blanco para que los elementos "floten"

---

## tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,jsx,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Paleta clay — pasteles saturados, no lavados
        'clay': {
          // Variantes de cada color: base (el elemento) + shadow (la sombra de color)
          'blue':        '#7EB8FF',
          'blue-shadow': '#3A7FD5',
          'blue-border': '#4A90E8',

          'purple':        '#C084FC',
          'purple-shadow': '#7C3AED',
          'purple-border': '#9333EA',

          'pink':        '#F9A8D4',
          'pink-shadow': '#DB2777',
          'pink-border': '#EC4899',

          'green':        '#6EE7B7',
          'green-shadow': '#059669',
          'green-border': '#10B981',

          'yellow':        '#FDE68A',
          'yellow-shadow': '#D97706',
          'yellow-border': '#F59E0B',

          'coral':        '#FCA5A5',
          'coral-shadow': '#DC2626',
          'coral-border': '#EF4444',

          'teal':        '#67E8F9',
          'teal-shadow': '#0891B2',
          'teal-border': '#06B6D4',

          'lavender':        '#DDD6FE',
          'lavender-shadow': '#6D28D9',
          'lavender-border': '#7C3AED',

          // Fondos
          'bg':         '#F8F4FF',  // lavanda muy suave
          'bg-alt':     '#FFF8F0',  // crema
          'bg-white':   '#FFFFFF',
        },
      },

      boxShadow: {
        // Sombras de COLOR — la firma del claymorphism
        // Formato: offset-x offset-y blur spread color
        'clay-blue':    '0 8px 0 0 #3A7FD5, 0 10px 20px rgba(58,127,213,0.3)',
        'clay-purple':  '0 8px 0 0 #7C3AED, 0 10px 20px rgba(124,58,237,0.3)',
        'clay-pink':    '0 8px 0 0 #DB2777, 0 10px 20px rgba(219,39,119,0.3)',
        'clay-green':   '0 8px 0 0 #059669, 0 10px 20px rgba(5,150,105,0.3)',
        'clay-yellow':  '0 8px 0 0 #D97706, 0 10px 20px rgba(217,119,6,0.3)',
        'clay-coral':   '0 8px 0 0 #DC2626, 0 10px 20px rgba(220,38,38,0.3)',
        'clay-teal':    '0 8px 0 0 #0891B2, 0 10px 20px rgba(8,145,178,0.3)',
        'clay-lavender':'0 8px 0 0 #6D28D9, 0 10px 20px rgba(109,40,217,0.3)',

        // Pressed (hundido — reducir offset)
        'clay-pressed': '0 2px 0 0 currentColor',

        // Card flotante blanca
        'clay-card':    '0 10px 0 0 #D1C4E9, 0 14px 30px rgba(109,40,217,0.12)',
        'clay-card-hover': '0 14px 0 0 #B39DDB, 0 18px 36px rgba(109,40,217,0.18)',
      },

      borderRadius: {
        'clay':    '20px',
        'clay-lg': '28px',
        'clay-xl': '36px',
        'clay-2xl':'48px',
      },

      fontFamily: {
        'clay':         ['Nunito', 'sans-serif'],       // redondeada y amigable
        'clay-display': ['Righteous', 'sans-serif'],    // display playful
        'clay-alt':     ['Fredoka One', 'cursive'],     // alternativa más fun
      },

      animation: {
        'clay-bounce':  'clayBounce 0.3s cubic-bezier(0.68,-0.55,0.27,1.55)',
        'clay-float':   'clayFloat 3s ease-in-out infinite',
        'clay-wobble':  'clayWobble 0.5s ease',
        'clay-pop':     'clayPop 0.25s cubic-bezier(0.68,-0.55,0.27,1.55)',
      },
      keyframes: {
        clayBounce: {
          '0%':   { transform: 'translateY(0) scale(1)' },
          '40%':  { transform: 'translateY(-8px) scale(1.05)' },
          '100%': { transform: 'translateY(0) scale(1)' },
        },
        clayFloat: {
          '0%, 100%': { transform: 'translateY(0px) rotate(-1deg)' },
          '50%':      { transform: 'translateY(-12px) rotate(1deg)' },
        },
        clayWobble: {
          '0%':  { transform: 'rotate(0deg)' },
          '20%': { transform: 'rotate(-5deg) scale(1.05)' },
          '40%': { transform: 'rotate(5deg)' },
          '60%': { transform: 'rotate(-3deg)' },
          '80%': { transform: 'rotate(2deg)' },
          '100%':{ transform: 'rotate(0deg)' },
        },
        clayPop: {
          '0%':   { transform: 'scale(1)' },
          '50%':  { transform: 'scale(0.92) translateY(6px)' },
          '100%': { transform: 'scale(1) translateY(0)' },
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
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Righteous&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-clay-bg font-clay text-gray-700 min-h-screen;
  }
  h1, h2, h3 {
    @apply font-clay-display text-gray-800;
  }
}

@layer components {

  /* ── Cards ── */
  .clay-card {
    @apply bg-white rounded-clay-lg p-8;
    @apply border-[3px] border-purple-200;
    box-shadow: 0 10px 0 0 #D1C4E9, 0 14px 30px rgba(109,40,217,0.12);
    transition: box-shadow 0.15s ease, transform 0.15s ease;
  }
  .clay-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 0 0 #B39DDB, 0 18px 36px rgba(109,40,217,0.18);
  }

  /* Cards de color */
  .clay-card-blue   { @apply bg-clay-blue   border-[3px] rounded-clay-lg p-8; border-color: #4A90E8; box-shadow: 0 8px 0 0 #3A7FD5, 0 12px 24px rgba(58,127,213,0.25); }
  .clay-card-purple { @apply bg-clay-purple border-[3px] rounded-clay-lg p-8; border-color: #9333EA; box-shadow: 0 8px 0 0 #7C3AED, 0 12px 24px rgba(124,58,237,0.25); }
  .clay-card-green  { @apply bg-clay-green  border-[3px] rounded-clay-lg p-8; border-color: #10B981; box-shadow: 0 8px 0 0 #059669, 0 12px 24px rgba(5,150,105,0.25); }
  .clay-card-yellow { @apply bg-clay-yellow border-[3px] rounded-clay-lg p-8; border-color: #F59E0B; box-shadow: 0 8px 0 0 #D97706, 0 12px 24px rgba(217,119,6,0.25); }
  .clay-card-pink   { @apply bg-clay-pink   border-[3px] rounded-clay-lg p-8; border-color: #EC4899; box-shadow: 0 8px 0 0 #DB2777, 0 12px 24px rgba(219,39,119,0.25); }
  .clay-card-coral  { @apply bg-clay-coral  border-[3px] rounded-clay-lg p-8; border-color: #EF4444; box-shadow: 0 8px 0 0 #DC2626, 0 12px 24px rgba(220,38,38,0.25); }

  /* ── Botones ── */
  .clay-btn {
    @apply inline-flex items-center justify-center gap-2;
    @apply px-7 py-3 font-bold text-sm text-white rounded-clay;
    @apply cursor-pointer select-none transition-all duration-100;
    @apply border-[3px];
  }
  .clay-btn:active {
    transform: translateY(6px);
  }

  /* Variantes de color de botón */
  .clay-btn-purple {
    @apply clay-btn bg-clay-purple text-white;
    border-color: #9333EA;
    box-shadow: 0 6px 0 0 #7C3AED;
  }
  .clay-btn-purple:active { box-shadow: 0 1px 0 0 #7C3AED; }

  .clay-btn-blue {
    @apply clay-btn bg-clay-blue text-white;
    border-color: #4A90E8;
    box-shadow: 0 6px 0 0 #3A7FD5;
  }
  .clay-btn-blue:active { box-shadow: 0 1px 0 0 #3A7FD5; }

  .clay-btn-green {
    @apply clay-btn bg-clay-green text-white;
    border-color: #10B981;
    box-shadow: 0 6px 0 0 #059669;
  }
  .clay-btn-green:active { box-shadow: 0 1px 0 0 #059669; }

  .clay-btn-yellow {
    @apply clay-btn bg-clay-yellow text-gray-800;
    border-color: #F59E0B;
    box-shadow: 0 6px 0 0 #D97706;
  }
  .clay-btn-yellow:active { box-shadow: 0 1px 0 0 #D97706; }

  .clay-btn-coral {
    @apply clay-btn bg-clay-coral text-white;
    border-color: #EF4444;
    box-shadow: 0 6px 0 0 #DC2626;
  }
  .clay-btn-coral:active { box-shadow: 0 1px 0 0 #DC2626; }

  /* Botón outline blanco (para usar sobre cards de color) */
  .clay-btn-outline {
    @apply clay-btn bg-white text-gray-700;
    border-color: #D1C4E9;
    box-shadow: 0 6px 0 0 #B39DDB;
  }
  .clay-btn-outline:active { box-shadow: 0 1px 0 0 #B39DDB; }

  /* ── Inputs ── */
  .clay-input {
    @apply w-full bg-white rounded-clay px-5 py-3.5;
    @apply font-clay text-gray-700 text-sm font-semibold;
    @apply border-[3px] border-purple-200 outline-none;
    @apply transition-all duration-150;
    @apply placeholder:text-gray-300 placeholder:font-medium;
    box-shadow: 0 4px 0 0 #D1C4E9;
  }
  .clay-input:focus {
    border-color: #C084FC;
    box-shadow: 0 4px 0 0 #9333EA;
  }

  /* ── Badge / Tag ── */
  .clay-badge {
    @apply inline-flex items-center gap-1.5 rounded-full px-4 py-1.5;
    @apply text-xs font-bold border-[2px];
  }
  .clay-badge-purple { @apply clay-badge bg-clay-purple text-purple-800; border-color: #9333EA; }
  .clay-badge-blue   { @apply clay-badge bg-clay-blue text-blue-800;     border-color: #4A90E8; }
  .clay-badge-green  { @apply clay-badge bg-clay-green text-green-800;   border-color: #10B981; }
  .clay-badge-yellow { @apply clay-badge bg-clay-yellow text-yellow-800; border-color: #F59E0B; }
  .clay-badge-pink   { @apply clay-badge bg-clay-pink text-pink-800;     border-color: #EC4899; }

  /* ── Avatar / Icono Clay ── */
  .clay-avatar {
    @apply rounded-clay-xl border-[3px] flex items-center justify-center font-bold;
  }

  /* ── Pill de navegación ── */
  .clay-nav-pill {
    @apply bg-white rounded-clay-xl border-[3px] border-purple-100;
    @apply px-6 py-3 flex items-center gap-6;
    box-shadow: 0 6px 0 0 #D1C4E9, 0 8px 20px rgba(109,40,217,0.1);
  }

  /* ── Tooltip clay ── */
  .clay-tooltip {
    @apply bg-gray-800 text-white text-xs font-bold rounded-clay px-3 py-1.5;
    @apply border-[2px] border-gray-700;
    box-shadow: 0 4px 0 0 #1F2937;
  }

  /* ── Progress bar ── */
  .clay-progress-track {
    @apply bg-purple-100 rounded-full h-4 overflow-hidden;
    @apply border-[2px] border-purple-200;
    box-shadow: inset 0 2px 4px rgba(109,40,217,0.15);
  }
  .clay-progress-fill {
    @apply h-full rounded-full;
    background: linear-gradient(90deg, #C084FC, #818CF8);
    box-shadow: 0 2px 6px rgba(124,58,237,0.4);
    transition: width 0.5s cubic-bezier(0.68,-0.55,0.27,1.55);
  }

  /* ── Animaciones ── */
  .clay-float   { @apply animate-clay-float; }
  .clay-wobble  { @apply animate-clay-wobble; }
  .clay-pop     { @apply animate-clay-pop; }
}
```

---

## HTML — Componentes Listos

### Navbar pill flotante

```html
<nav class="clay-nav-pill fixed top-4 left-1/2 -translate-x-1/2 z-50 w-fit">
  <span class="font-clay-display text-lg text-purple-600">🎨 ClayApp</span>
  <div class="flex items-center gap-4 ml-4">
    <a href="#" class="font-bold text-sm text-gray-500 hover:text-purple-600 transition-colors">Inicio</a>
    <a href="#" class="font-bold text-sm text-gray-500 hover:text-purple-600 transition-colors">Galería</a>
    <button class="clay-btn-purple text-xs px-5 py-2">Empezar →</button>
  </div>
</nav>
```

### Hero

```html
<section class="min-h-screen flex items-center justify-center px-8 py-20 text-center">
  <!-- Elementos flotantes decorativos -->
  <div class="clay-card-blue w-16 h-16 rounded-clay-2xl absolute top-32 left-16 animate-clay-float flex items-center justify-center text-2xl" style="animation-delay: 0s">🌊</div>
  <div class="clay-card-yellow w-14 h-14 rounded-clay-2xl absolute top-48 right-20 animate-clay-float flex items-center justify-center text-xl" style="animation-delay: 0.8s">⭐</div>
  <div class="clay-card-coral w-12 h-12 rounded-clay-xl absolute bottom-32 left-32 animate-clay-float flex items-center justify-center text-lg" style="animation-delay: 1.5s">🎯</div>

  <div class="relative">
    <div class="clay-badge-purple mb-6">✨ Versión 2.0 disponible</div>
    <h1 class="font-clay-display text-6xl md:text-8xl text-gray-800 mb-4 leading-none">
      Creá sin<br/>
      <span class="text-purple-500">límites</span>
    </h1>
    <p class="font-clay text-lg text-gray-500 font-semibold max-w-lg mx-auto mb-10">
      La plataforma más divertida para equipos creativos. Simple, rápida y sin complicaciones.
    </p>
    <div class="flex items-center justify-center gap-4 flex-wrap">
      <button class="clay-btn-purple text-base px-10 py-4">Probar gratis 🚀</button>
      <button class="clay-btn-outline text-base px-10 py-4">Ver demo</button>
    </div>
  </div>
</section>
```

### Grid de feature cards

```html
<div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-8">

  <div class="clay-card-blue text-white">
    <div class="text-4xl mb-4">⚡</div>
    <h3 class="font-clay-display text-xl mb-2">Ultra rápido</h3>
    <p class="font-clay text-sm text-blue-100 font-semibold leading-relaxed">
      Cargá tus proyectos en milisegundos. Sin esperas, sin frustraciones.
    </p>
  </div>

  <div class="clay-card-yellow">
    <div class="text-4xl mb-4">🎨</div>
    <h3 class="font-clay-display text-xl mb-2 text-yellow-800">Personalizable</h3>
    <p class="font-clay text-sm text-yellow-700 font-semibold leading-relaxed">
      Hacé que tu espacio de trabajo sea único con miles de opciones.
    </p>
  </div>

  <div class="clay-card-green text-white">
    <div class="text-4xl mb-4">🤝</div>
    <h3 class="font-clay-display text-xl mb-2">Colaborativo</h3>
    <p class="font-clay text-sm text-green-100 font-semibold leading-relaxed">
      Trabajá en tiempo real con tu equipo desde cualquier lugar.
    </p>
  </div>

</div>
```

### Card de producto / pricing

```html
<div class="clay-card max-w-sm mx-auto relative">
  <!-- Badge flotante -->
  <div class="absolute -top-4 left-1/2 -translate-x-1/2">
    <span class="clay-badge-coral">⭐ Más popular</span>
  </div>

  <div class="clay-avatar bg-clay-purple w-16 h-16 text-2xl text-white mb-6 border-purple-600">
    🚀
  </div>

  <h3 class="font-clay-display text-2xl text-gray-800 mb-1">Pro</h3>
  <div class="font-clay-display text-5xl text-purple-500 mb-1">$12<span class="text-xl text-gray-400">/mes</span></div>
  <p class="font-clay text-sm text-gray-400 font-semibold mb-6">Facturado anualmente</p>

  <ul class="space-y-3 mb-8">
    <li class="flex items-center gap-3 font-clay font-semibold text-sm text-gray-600">
      <span class="clay-badge-green text-xs px-2 py-0.5">✓</span> Proyectos ilimitados
    </li>
    <li class="flex items-center gap-3 font-clay font-semibold text-sm text-gray-600">
      <span class="clay-badge-green text-xs px-2 py-0.5">✓</span> 50 GB de almacenamiento
    </li>
    <li class="flex items-center gap-3 font-clay font-semibold text-sm text-gray-600">
      <span class="clay-badge-green text-xs px-2 py-0.5">✓</span> Soporte prioritario 24/7
    </li>
    <li class="flex items-center gap-3 font-clay font-semibold text-sm text-gray-600">
      <span class="clay-badge-green text-xs px-2 py-0.5">✓</span> API completa
    </li>
  </ul>

  <button class="clay-btn-purple w-full py-4 text-base">Elegir Pro 💜</button>
</div>
```

### Formulario de registro

```html
<div class="clay-card max-w-md mx-auto">
  <div class="clay-avatar bg-clay-purple w-14 h-14 text-2xl text-white mb-6 border-purple-600">👋</div>
  <h2 class="font-clay-display text-3xl text-gray-800 mb-1">Crear cuenta</h2>
  <p class="font-clay text-sm text-gray-400 font-semibold mb-8">¡Gratis para siempre, sin tarjeta!</p>

  <div class="space-y-4">
    <div>
      <label class="font-clay font-bold text-xs text-gray-500 uppercase tracking-wider mb-2 block">Tu nombre</label>
      <input type="text" placeholder="Juan García" class="clay-input" />
    </div>
    <div>
      <label class="font-clay font-bold text-xs text-gray-500 uppercase tracking-wider mb-2 block">Email</label>
      <input type="email" placeholder="juan@ejemplo.com" class="clay-input" />
    </div>
    <div>
      <label class="font-clay font-bold text-xs text-gray-500 uppercase tracking-wider mb-2 block">Contraseña</label>
      <input type="password" placeholder="••••••••" class="clay-input" />
    </div>
  </div>

  <button class="clay-btn-purple w-full mt-6 py-4 text-base">Crear cuenta gratis 🎉</button>
  <p class="text-center font-clay text-xs text-gray-400 font-semibold mt-4">
    ¿Ya tenés cuenta? <a href="#" class="text-purple-500 hover:underline font-bold">Ingresar</a>
  </p>
</div>
```

### Progress / Stats

```html
<div class="clay-card max-w-md">
  <h3 class="font-clay-display text-xl text-gray-800 mb-6">Tu progreso 📈</h3>

  <div class="space-y-5">
    <div>
      <div class="flex justify-between font-clay font-bold text-sm text-gray-600 mb-2">
        <span>Proyectos completados</span><span class="text-purple-500">72%</span>
      </div>
      <div class="clay-progress-track">
        <div class="clay-progress-fill" style="width: 72%"></div>
      </div>
    </div>
    <div>
      <div class="flex justify-between font-clay font-bold text-sm text-gray-600 mb-2">
        <span>Almacenamiento usado</span><span class="text-blue-500">38%</span>
      </div>
      <div class="clay-progress-track" style="border-color: #BAE6FD; background: #E0F2FE;">
        <div class="clay-progress-fill" style="width: 38%; background: linear-gradient(90deg, #7EB8FF, #60A5FA);"></div>
      </div>
    </div>
  </div>

  <div class="grid grid-cols-3 gap-4 mt-8">
    <div class="clay-card-purple text-center text-white py-4 px-2">
      <div class="font-clay-display text-2xl">14</div>
      <div class="font-clay text-xs font-bold opacity-80">Proyectos</div>
    </div>
    <div class="clay-card-green text-center text-white py-4 px-2">
      <div class="font-clay-display text-2xl">3.2k</div>
      <div class="font-clay text-xs font-bold opacity-80">Archivos</div>
    </div>
    <div class="clay-card-yellow text-center text-yellow-800 py-4 px-2">
      <div class="font-clay-display text-2xl">98%</div>
      <div class="font-clay text-xs font-bold opacity-70">Uptime</div>
    </div>
  </div>
</div>
```

---

## Reglas de Composición

### Fondo
```html
<!-- Opción 1: liso suave -->
<body class="bg-clay-bg">

<!-- Opción 2: gradiente pastel -->
<body style="background: linear-gradient(135deg, #F8F4FF 0%, #FFF0F9 50%, #F0FFF4 100%)">

<!-- Opción 3: puntos decorativos -->
<body class="bg-clay-bg" style="background-image: radial-gradient(circle, #D1C4E9 1px, transparent 1px); background-size: 30px 30px;">
```

### Elementos decorativos flotantes
```html
<!-- Siempre usar animate-clay-float con animation-delay para que no vayan en sincronía -->
<div class="absolute w-20 h-20 clay-card-blue rounded-clay-2xl animate-clay-float flex items-center justify-center text-3xl"
     style="top: 10%; left: 5%; animation-delay: 0s">🌊</div>
<div class="absolute w-16 h-16 clay-card-yellow rounded-clay-2xl animate-clay-float flex items-center justify-center text-2xl"
     style="top: 20%; right: 8%; animation-delay: 1s">⭐</div>
```

---

## Referencia Rápida

| Propiedad | Clase |
|-----------|-------|
| Border-radius inflado | `rounded-clay` / `rounded-clay-lg` / `rounded-clay-xl` (config) |
| Sombra de color | `shadow-clay-purple` etc. (config) |
| Fuente redondeada | `font-clay` (Nunito) |
| Fuente display playful | `font-clay-display` (Righteous) |
| Flotación | `animate-clay-float` |
| Wobble en hover | `hover:animate-clay-wobble` |
| Press effect | `:active` con `translateY(6px)` y shadow reducida |

---

## Anti-patrones a Evitar

- ❌ Sombras grises neutras (`shadow-xl` de Tailwind) — siempre sombras de COLOR
- ❌ `rounded-none` o `rounded-sm` — los elementos clay siempre son inflados
- ❌ Colores apagados o desaturados — el clay necesita saturación alta
- ❌ Tipografías serias o serif — usar fuentes redondeadas y amigables
- ❌ Animaciones lineales — usar `cubic-bezier(0.68,-0.55,0.27,1.55)` (elástico)
- ❌ Fondos oscuros — claymorphism vive en fondos claros o pasteles muy suaves
- ❌ Bordes negros — los bordes son siempre del mismo matiz del elemento, más oscuros

---

## Casos de Uso Ideales

- Apps para niños y jóvenes
- Onboarding y tutoriales interactivos
- Plataformas educativas (EdTech)
- Apps de salud y bienestar gamificadas
- Landing pages de productos creativos y SaaS jóvenes
- E-commerce de productos artesanales o creativos
- Dashboards de productividad para equipos creativos
