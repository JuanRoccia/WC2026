---
name: softui-neumorphism-tailwind
description: Diseño Soft UI / Neumorphism implementado con Tailwind CSS. Usar cuando el usuario quiere interfaces con sensación táctil y de relieve usando sombras simétricas con Tailwind. El neumorphism requiere sombras custom en tailwind.config.js ya que Tailwind no tiene las sombras duales nativas. Incluye config completo, componentes con @apply y HTML de ejemplo.
---

# SKILL: Soft UI / Neumorphism con Tailwind CSS

## Concepto

El Neumorphism es el estilo que **más depende de configuración custom** en Tailwind porque:
- Las sombras duales simétricas no existen en el sistema nativo de Tailwind
- El color de fondo base necesita estar extendido en el config
- Las sombras inset tampoco tienen shortcuts nativos en Tailwind v3

Sin embargo, una vez configurado, los componentes quedan muy limpios y reutilizables.

---

## tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,jsx,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Color base del neumorphism — el fondo y los elementos son el MISMO color
        'neu': {
          'base':    '#E0E5EC',   // gris azulado clásico (el más usado)
          'dark':    '#B8BEC8',   // para sombra oscura
          'light':   '#FFFFFF',   // para sombra clara
          'surface': '#D0D5DC',   // variante levemente más oscura
        },
        // Variantes de paleta base (elegir una por proyecto)
        'neu-beige': {
          'base':  '#ECE8E1',
          'dark':  '#C4BFB8',
          'light': '#FFFFFF',
        },
        'neu-mint': {
          'base':  '#E0EDE8',
          'dark':  '#B8C5BE',
          'light': '#FFFFFF',
        },
        'neu-dark': {
          'base':  '#2D3047',
          'dark':  '#1E2130',
          'light': '#3C4060',
        },
        // Acentos (máximo 1-2 por proyecto)
        'neu-accent': {
          'blue':   '#5B8BF5',
          'green':  '#3DAA7A',
          'coral':  '#E07B54',
          'purple': '#9B59B6',
        },
        // Texto — nunca negro puro en neumorphism
        'neu-text': {
          'primary':   '#374151',
          'secondary': '#6B7280',
          'muted':     '#9CA3AF',
        },
      },

      boxShadow: {
        // ══ SOMBRAS CONVEXAS (elemento que sobresale) ══
        'neu':     '8px 8px 16px #B8BEC8, -8px -8px 16px #FFFFFF',
        'neu-sm':  '4px 4px 8px #B8BEC8, -4px -4px 8px #FFFFFF',
        'neu-lg':  '12px 12px 24px #A8AEB8, -12px -12px 24px #FFFFFF',
        'neu-xl':  '18px 18px 36px #A0A6B0, -18px -18px 36px #FFFFFF',

        // ══ SOMBRAS CÓNCAVAS (elemento hundido / pressed) ══
        'neu-inset':    'inset 6px 6px 12px #B8BEC8, inset -6px -6px 12px #FFFFFF',
        'neu-inset-sm': 'inset 4px 4px 8px #B8BEC8, inset -4px -4px 8px #FFFFFF',
        'neu-inset-lg': 'inset 8px 8px 16px #A8AEB8, inset -8px -8px 16px #FFFFFF',

        // ══ SOMBRA DE BOTÓN ACTIVO / PRESIONADO ══
        'neu-pressed': 'inset 4px 4px 8px #B8BEC8, inset -4px -4px 8px #FFFFFF',

        // ══ VARIANTE DARK MODE ══
        'neu-dark':       '8px 8px 16px #1E2130, -8px -8px 16px #3C4060',
        'neu-dark-inset': 'inset 6px 6px 12px #1E2130, inset -6px -6px 12px #3C4060',

        // ══ CON ACENTO (botón activo de color) ══
        'neu-accent': '5px 5px 12px #B8BEC8, -3px -3px 8px #FFFFFF, inset 2px 2px 4px rgba(255,255,255,0.3)',

        // ══ FOCUS (ring de acento) ══
        'neu-focus': 'inset 4px 4px 8px #B8BEC8, inset -4px -4px 8px #FFFFFF, 0 0 0 3px rgba(91,139,245,0.2)',
      },

      fontFamily: {
        'neu': ['Nunito', 'sans-serif'],
        'neu-display': ['Poppins', 'sans-serif'],
      },

      animation: {
        'neu-reveal': 'neuReveal 0.4s ease forwards',
      },
      keyframes: {
        neuReveal: {
          '0%':   { opacity: '0', transform: 'scale(0.97)', boxShadow: 'none' },
          '100%': { opacity: '1', transform: 'scale(1)' },
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
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700&family=Poppins:wght@400;500;600&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-neu-base font-neu text-neu-text-secondary min-h-screen;
  }

  h1, h2, h3 {
    @apply font-neu-display font-semibold text-neu-text-primary;
  }

  /* Quitar outline nativo y reemplazar por neu-focus */
  *:focus {
    outline: none;
  }
}

@layer components {

  /* ── Cards ── */
  .neu-card {
    @apply bg-neu-base rounded-2xl p-8 shadow-neu;
  }
  .neu-card-sm {
    @apply bg-neu-base rounded-xl p-6 shadow-neu-sm;
  }
  .neu-card-lg {
    @apply bg-neu-base rounded-3xl p-10 shadow-neu-lg;
  }

  /* Card hundida (contenedor cóncavo) */
  .neu-well {
    @apply bg-neu-base rounded-2xl p-8 shadow-neu-inset;
  }

  /* ── Botones ── */
  /* Base convexo */
  .neu-btn {
    @apply bg-neu-base border-none rounded-full;
    @apply px-8 py-3 font-semibold text-sm text-neu-text-secondary;
    @apply cursor-pointer shadow-neu transition-all duration-150;
    @apply hover:text-neu-text-primary;
    @apply active:shadow-neu-pressed active:scale-[0.98];
  }

  /* Acento (CTA, estado activo) */
  .neu-btn-accent {
    @apply border-none rounded-full;
    @apply px-8 py-3 font-semibold text-sm text-white;
    @apply cursor-pointer shadow-neu-accent transition-all duration-200;
    background: linear-gradient(145deg, #7098F8, #5B8BF5);
  }
  .neu-btn-accent:hover {
    box-shadow: 6px 6px 14px #B0B6C0, -4px -4px 10px #FFFFFF, inset 2px 2px 4px rgba(255,255,255,0.3);
  }
  .neu-btn-accent:active {
    @apply scale-[0.98];
  }

  /* Icono (cuadrado redondeado) */
  .neu-icon-btn {
    @apply bg-neu-base w-12 h-12 rounded-2xl shadow-neu-sm;
    @apply flex items-center justify-center cursor-pointer;
    @apply transition-all duration-150 text-neu-text-secondary;
    @apply hover:text-neu-text-primary active:shadow-neu-inset-sm;
  }

  /* ── Inputs ── */
  .neu-input {
    @apply w-full bg-neu-base border-none rounded-xl;
    @apply px-4 py-3.5 text-neu-text-primary text-sm;
    @apply shadow-neu-inset-sm transition-shadow duration-200;
    @apply placeholder:text-neu-text-muted;
  }
  .neu-input:focus {
    box-shadow: inset 4px 4px 10px #B0B6C0, inset -4px -4px 10px #FFFFFF, 0 0 0 3px rgba(91,139,245,0.2);
  }

  /* Textarea */
  .neu-textarea {
    @apply neu-input resize-none;
  }

  /* ── Toggle / Switch ── */
  .neu-toggle-track {
    @apply relative w-14 h-7 rounded-full cursor-pointer;
    @apply bg-neu-base shadow-neu-inset-sm transition-all duration-300;
  }
  .neu-toggle-knob {
    @apply absolute w-[22px] h-[22px] rounded-full top-[3px] left-[3px];
    @apply bg-neu-base shadow-neu-sm transition-transform duration-300;
  }
  /* Estado ON — agregar clase .on al track */
  .neu-toggle-track.on {
    background: linear-gradient(145deg, #6490F6, #5B8BF5);
  }
  .neu-toggle-track.on .neu-toggle-knob {
    @apply translate-x-7;
  }

  /* ── Progress bar ── */
  .neu-progress {
    @apply bg-neu-base rounded-full h-2.5 shadow-neu-inset-sm overflow-hidden;
  }
  .neu-progress-fill {
    @apply h-full rounded-full transition-all duration-500;
    background: linear-gradient(90deg, #7098F8, #5B8BF5);
    box-shadow: 2px 0 8px rgba(91, 139, 245, 0.4);
  }

  /* ── Slider ── */
  .neu-slider {
    @apply w-full appearance-none bg-neu-base rounded-full h-2.5 cursor-pointer;
    box-shadow: inset 3px 3px 6px #B8BEC8, inset -3px -3px 6px #FFFFFF;
  }
  .neu-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    @apply w-5 h-5 rounded-full bg-neu-base cursor-pointer;
    box-shadow: 3px 3px 6px #B8BEC8, -2px -2px 5px #FFFFFF;
  }

  /* ── Icono / Avatar container ── */
  .neu-icon {
    @apply bg-neu-base rounded-2xl shadow-neu-sm;
    @apply flex items-center justify-center;
  }

  /* ── Badge ── */
  .neu-badge {
    @apply inline-flex items-center rounded-full px-3 py-1;
    @apply text-xs font-semibold text-neu-text-secondary;
    @apply bg-neu-base shadow-neu-sm;
  }

  /* ── Animación reveal ── */
  .neu-reveal {
    @apply animate-neu-reveal;
  }

  /* ── Separador ── */
  .neu-divider {
    @apply my-8 border-none h-px;
    background: linear-gradient(90deg, transparent, #B8BEC8 30%, #B8BEC8 70%, transparent);
  }
}
```

---

## HTML — Componentes Listos

### Layout base

```html
<body class="bg-neu-base font-neu text-neu-text-secondary min-h-screen p-8">
  <div class="max-w-4xl mx-auto space-y-8">
    ...
  </div>
</body>
```

### Card principal

```html
<div class="neu-card neu-reveal">
  <div class="flex items-center gap-4 mb-6">
    <div class="neu-icon w-12 h-12 text-neu-accent-blue">
      <!-- icono SVG o emoji -->
      🎯
    </div>
    <div>
      <h3 class="font-neu-display font-semibold text-neu-text-primary">Objetivo del mes</h3>
      <p class="text-xs text-neu-text-muted">Actualizado hace 2h</p>
    </div>
  </div>

  <!-- Barra de progreso -->
  <div class="mb-2 flex justify-between text-xs font-semibold">
    <span class="text-neu-text-secondary">Progreso</span>
    <span class="text-neu-accent-blue">72%</span>
  </div>
  <div class="neu-progress mb-6">
    <div class="neu-progress-fill" style="width: 72%"></div>
  </div>

  <div class="flex gap-3">
    <button class="neu-btn flex-1 text-center">Ver detalles</button>
    <button class="neu-btn-accent flex-1 text-center">Continuar</button>
  </div>
</div>
```

### Formulario

```html
<div class="neu-card max-w-md mx-auto">
  <h2 class="font-neu-display text-2xl font-semibold text-neu-text-primary mb-2">
    Nuevo registro
  </h2>
  <p class="text-neu-text-muted text-sm mb-8">Completá los campos para continuar</p>

  <div class="space-y-6">
    <div>
      <label class="block text-xs font-semibold text-neu-text-secondary mb-2 uppercase tracking-wider">
        Nombre
      </label>
      <input type="text" placeholder="Tu nombre" class="neu-input" />
    </div>
    <div>
      <label class="block text-xs font-semibold text-neu-text-secondary mb-2 uppercase tracking-wider">
        Email
      </label>
      <input type="email" placeholder="tu@email.com" class="neu-input" />
    </div>
    <div>
      <label class="block text-xs font-semibold text-neu-text-secondary mb-2 uppercase tracking-wider">
        Notas
      </label>
      <textarea rows="3" placeholder="Observaciones..." class="neu-textarea"></textarea>
    </div>
  </div>

  <div class="neu-divider"></div>

  <div class="flex gap-3">
    <button class="neu-btn flex-1">Cancelar</button>
    <button class="neu-btn-accent flex-1">Guardar</button>
  </div>
</div>
```

### Panel de controles (Audio/Smart home)

```html
<div class="neu-card max-w-sm mx-auto">
  <h3 class="font-neu-display font-semibold text-neu-text-primary mb-6">Controles</h3>

  <!-- Iconos de acción -->
  <div class="flex justify-around mb-8">
    <button class="neu-icon-btn text-xl">⏮</button>
    <button class="neu-icon-btn w-16 h-16 rounded-full text-xl text-neu-accent-blue shadow-neu">▶</button>
    <button class="neu-icon-btn text-xl">⏭</button>
  </div>

  <!-- Slider de volumen -->
  <div class="mb-6">
    <div class="flex justify-between text-xs text-neu-text-muted mb-3">
      <span>Volumen</span>
      <span>75%</span>
    </div>
    <input type="range" value="75" class="neu-slider w-full" />
  </div>

  <!-- Toggle -->
  <div class="flex items-center justify-between">
    <span class="text-sm font-semibold text-neu-text-secondary">Modo noche</span>
    <div class="neu-toggle-track on" onclick="this.classList.toggle('on')">
      <div class="neu-toggle-knob"></div>
    </div>
  </div>
</div>
```

### Dashboard de métricas

```html
<div class="grid grid-cols-2 md:grid-cols-4 gap-6">
  <!-- Stat card -->
  <div class="neu-card text-center py-6">
    <div class="text-3xl font-neu-display font-bold text-neu-accent-blue mb-1">142</div>
    <div class="text-xs text-neu-text-muted uppercase tracking-wider">Usuarios</div>
  </div>
  <div class="neu-card text-center py-6">
    <div class="text-3xl font-neu-display font-bold text-neu-accent-green mb-1">$4.2K</div>
    <div class="text-xs text-neu-text-muted uppercase tracking-wider">Ingresos</div>
  </div>
  <div class="neu-card text-center py-6">
    <div class="text-3xl font-neu-display font-bold text-neu-accent-blue mb-1">98%</div>
    <div class="text-xs text-neu-text-muted uppercase tracking-wider">Uptime</div>
  </div>
  <div class="neu-card text-center py-6">
    <div class="text-3xl font-neu-display font-bold text-neu-accent-coral mb-1">12</div>
    <div class="text-xs text-neu-text-muted uppercase tracking-wider">Alertas</div>
  </div>
</div>
```

### Lista de items hundida (well / cóncava)

```html
<div class="neu-well space-y-3">
  <div class="flex items-center gap-4 bg-neu-base rounded-xl p-4 shadow-neu-sm">
    <div class="neu-icon w-10 h-10 text-sm">📋</div>
    <div class="flex-1">
      <div class="font-semibold text-neu-text-primary text-sm">Tarea pendiente</div>
      <div class="text-xs text-neu-text-muted">Vence mañana</div>
    </div>
    <span class="neu-badge">Alta prioridad</span>
  </div>
  <div class="flex items-center gap-4 bg-neu-base rounded-xl p-4 shadow-neu-sm">
    <div class="neu-icon w-10 h-10 text-sm">✅</div>
    <div class="flex-1">
      <div class="font-semibold text-neu-text-primary text-sm">Tarea completada</div>
      <div class="text-xs text-neu-text-muted">Ayer a las 14:30</div>
    </div>
  </div>
</div>
```

---

## Referencia Rápida: Clases Custom vs Nativas

| Necesidad | Solución |
|-----------|---------|
| Card convexo | `shadow-neu` (config) |
| Card cóncavo | `shadow-neu-inset` (config) |
| Botón presionado | `shadow-neu-pressed` (config) |
| Fondo base | `bg-neu-base` (config) |
| Texto principal | `text-neu-text-primary` (config) |
| Border-radius suave | `rounded-2xl` o `rounded-3xl` ✅ nativo |
| Tipografía suave | `font-neu` o `font-neu-display` (config) |
| Transición press | `transition-all duration-150` ✅ nativo |
| Scale en active | `active:scale-[0.98]` ✅ nativo |

---

## ⚠️ Limitaciones de Tailwind para Neumorphism

| Necesidad | Solución |
|-----------|---------|
| Doble sombra (clara + oscura) | **Siempre en `extend.boxShadow`** — no hay forma nativa |
| Sombra inset dual | Ídem — `extend.boxShadow` |
| Slider `::webkit-slider-thumb` | Solo en CSS puro (Tailwind no genera pseudo-elementos de input) |
| Gradiente en botón acento | `style=""` inline o `@layer components` |
| Cambiar sombras por paleta | Redefinir en config para cada variante de color |

---

## Variante Dark Neumorphism

Para modo oscuro, redefinir las sombras con los colores de `neu-dark`:

```js
// En tailwind.config.js, agregar:
boxShadow: {
  // ... sombras existentes
  'neu-dark':          '8px 8px 16px #1E2130, -8px -8px 16px #3C4060',
  'neu-dark-inset':    'inset 6px 6px 12px #1E2130, inset -6px -6px 12px #3C4060',
  'neu-dark-sm':       '4px 4px 8px #1E2130, -4px -4px 8px #3C4060',
  'neu-dark-pressed':  'inset 4px 4px 8px #1E2130, inset -4px -4px 8px #3C4060',
}
```

```html
<!-- Dark mode: cambiar bg y shadows -->
<body class="bg-neu-dark-base">
  <div class="bg-neu-dark-base rounded-2xl p-8 shadow-neu-dark">
    ...
  </div>
</body>
```

---

## Anti-patrones a Evitar

- ❌ `shadow-xl` nativo de Tailwind (tiene blur pero sin el par dual claro/oscuro)
- ❌ `bg-white` o `bg-gray-100` — la sombra dual no se ve en colores extremos
- ❌ `border-*` — el neumorphism no usa bordes visibles
- ❌ `text-black` o `text-gray-900` — reducir el contraste con `text-neu-text-*`
- ❌ Olvidar aplicar la misma sombra base al fondo Y a los elementos
- ❌ `rounded-none` — los elementos siempre necesitan border-radius generoso

---

## Casos de Uso Ideales

- Apps de salud, meditación y bienestar
- Interfaces de smart home y wearables
- Controles de audio / reproductores de música
- Dashboards de productividad personal
- Apps de finanzas personales (tracking de gastos)
- Paneles de configuración (settings UI)
- Apps de fitness y tracking de ejercicio
