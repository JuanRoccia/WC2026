---
name: cyberpunk-neon-tailwind
description: Diseño Cyberpunk / Neon implementado con Tailwind CSS. Usar cuando el usuario quiere interfaces con estética futurista oscura: fondos casi-negros, luces de neón (cyan, magenta, amarillo eléctrico), efectos de glitch, texto con glow, líneas de scan, y sensación de distopía tech. Ideal para gaming, crypto, herramientas para hackers/devs, portafolios tech agresivos y cualquier producto que quiera sentirse del futuro. Incluye tailwind.config.js completo, @layer components y HTML de ejemplo.
---

# SKILL: Cyberpunk / Neon con Tailwind CSS

## Concepto

**Cyberpunk/Neon** es la estética de la distopía tecnológica: ciudades nocturnas, pantallas viejas, hologramas y neón. Los elementos clave son el contraste extremo (negro profundo vs. luces brillantes), los glows de color, la tipografía monospace o futurista, y los detalles que sugieren tecnología de alta tensión.

Referentes: Cyberpunk 2077 UI, Mr. Robot interfaces, Tron Legacy, terminales de hacking en películas, plataformas de trading crypto de alta adrenalina.

**La firma del Cyberpunk/Neon:**
- Fondo negro profundo con matiz (nunca negro puro)
- 2-3 colores neón máximo: cyan `#00F5FF`, magenta `#FF0090`, amarillo `#FFE000`
- `text-shadow` y `box-shadow` tipo glow de color
- Tipografía monospace o con look de terminal/HUD
- Elementos decorativos: líneas diagonales, grids, scan lines, glitch

---

## tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,jsx,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'cyber': {
          // Fondos
          'void':    '#030308',   // negro con matiz azul muy oscuro
          'dark':    '#08090F',
          'surface': '#0D0E1A',
          'panel':   '#12132A',
          'overlay': '#1A1B35',

          // Neones — los protagonistas
          'cyan':    '#00F5FF',
          'magenta': '#FF0090',
          'yellow':  '#FFE000',
          'green':   '#00FF41',   // verde matrix

          // Versiones dim (para bordes y elementos secundarios)
          'cyan-dim':    '#007A80',
          'magenta-dim': '#80004A',
          'yellow-dim':  '#806000',
          'green-dim':   '#007A20',

          // Versiones glow (para box-shadow como color)
          'cyan-glow':    'rgba(0,245,255,0.4)',
          'magenta-glow': 'rgba(255,0,144,0.4)',
          'yellow-glow':  'rgba(255,224,0,0.4)',

          // Texto
          'text':        '#C8D0E8',   // blanco frío
          'text-dim':    '#5A6080',
          'text-muted':  '#2A2D45',
        },
      },

      boxShadow: {
        // Glows neón — la esencia del estilo
        'neon-cyan':    '0 0 10px #00F5FF, 0 0 30px rgba(0,245,255,0.5), 0 0 60px rgba(0,245,255,0.2)',
        'neon-magenta': '0 0 10px #FF0090, 0 0 30px rgba(255,0,144,0.5), 0 0 60px rgba(255,0,144,0.2)',
        'neon-yellow':  '0 0 10px #FFE000, 0 0 30px rgba(255,224,0,0.5), 0 0 60px rgba(255,224,0,0.2)',
        'neon-green':   '0 0 10px #00FF41, 0 0 30px rgba(0,255,65,0.5),  0 0 60px rgba(0,255,65,0.2)',

        // Glows más suaves para cards
        'cyber-card-cyan':    '0 0 1px #00F5FF, inset 0 0 30px rgba(0,245,255,0.05)',
        'cyber-card-magenta': '0 0 1px #FF0090, inset 0 0 30px rgba(255,0,144,0.05)',
        'cyber-card-yellow':  '0 0 1px #FFE000, inset 0 0 30px rgba(255,224,0,0.05)',

        // Hover intensificado
        'neon-cyan-lg':    '0 0 20px #00F5FF, 0 0 60px rgba(0,245,255,0.6), 0 0 100px rgba(0,245,255,0.3)',
        'neon-magenta-lg': '0 0 20px #FF0090, 0 0 60px rgba(255,0,144,0.6), 0 0 100px rgba(255,0,144,0.3)',

        // Sombra de botón (borde inferior para efecto 3D)
        'cyber-btn-cyan':    '0 4px 0 #007A80, 0 0 15px rgba(0,245,255,0.4)',
        'cyber-btn-magenta': '0 4px 0 #80004A, 0 0 15px rgba(255,0,144,0.4)',
        'cyber-btn-yellow':  '0 4px 0 #806000, 0 0 15px rgba(255,224,0,0.4)',
      },

      fontFamily: {
        'cyber':         ['Share Tech Mono', 'Courier New', 'monospace'],
        'cyber-display': ['Orbitron', 'sans-serif'],
        'cyber-body':    ['Rajdhani', 'sans-serif'],
      },

      backgroundImage: {
        // Grid de fondo estilo terminal
        'cyber-grid': `
          linear-gradient(rgba(0,245,255,0.03) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0,245,255,0.03) 1px, transparent 1px)
        `,
        // Scan lines
        'scan-lines': `repeating-linear-gradient(
          0deg,
          transparent,
          transparent 2px,
          rgba(0,0,0,0.15) 2px,
          rgba(0,0,0,0.15) 4px
        )`,
        // Gradiente diagonal neón (para acentos)
        'neon-gradient': 'linear-gradient(135deg, #00F5FF 0%, #FF0090 100%)',
        'neon-gradient-y': 'linear-gradient(180deg, #00F5FF 0%, #FF0090 100%)',
      },

      animation: {
        'glitch':     'glitch 0.4s steps(2) infinite',
        'flicker':    'flicker 3s step-start infinite',
        'scan':       'scan 4s linear infinite',
        'pulse-neon': 'pulseNeon 2s ease-in-out infinite',
        'type':       'type 2s steps(20) forwards',
        'blink':      'blink 1s step-end infinite',
      },
      keyframes: {
        glitch: {
          '0%':  { transform: 'translate(0)', clipPath: 'inset(0 0 100% 0)' },
          '20%': { transform: 'translate(-3px, 2px)', clipPath: 'inset(20% 0 60% 0)' },
          '40%': { transform: 'translate(3px, -2px)', clipPath: 'inset(60% 0 20% 0)' },
          '60%': { transform: 'translate(-2px, 0)', clipPath: 'inset(40% 0 40% 0)' },
          '80%': { transform: 'translate(2px, 2px)', clipPath: 'inset(80% 0 10% 0)' },
          '100%':{ transform: 'translate(0)', clipPath: 'inset(0 0 0 0)' },
        },
        flicker: {
          '0%, 95%, 100%':      { opacity: '1' },
          '96%, 98%':           { opacity: '0.4' },
          '97%':                { opacity: '0.8' },
        },
        scan: {
          '0%':   { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        pulseNeon: {
          '0%, 100%': { opacity: '1', filter: 'brightness(1)' },
          '50%':      { opacity: '0.8', filter: 'brightness(1.3)' },
        },
        blink: {
          '0%, 100%': { opacity: '1' },
          '50%':      { opacity: '0' },
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
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-cyber-void font-cyber-body text-cyber-text min-h-screen overflow-x-hidden;
    background-image:
      linear-gradient(rgba(0,245,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,245,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
  }

  /* Scan line overlay global — opcional */
  body::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
      0deg, transparent, transparent 2px,
      rgba(0,0,0,0.08) 2px, rgba(0,0,0,0.08) 4px
    );
    pointer-events: none;
    z-index: 9999;
  }

  h1, h2, h3 {
    @apply font-cyber-display text-cyber-text;
  }

  ::selection {
    background: rgba(0, 245, 255, 0.3);
    color: #fff;
  }
}

@layer components {

  /* ── Cards ── */
  .cyber-card {
    @apply bg-cyber-surface relative overflow-hidden;
    @apply border border-cyber-cyan-dim rounded-sm p-8;
    box-shadow: 0 0 1px #00F5FF, inset 0 0 30px rgba(0,245,255,0.04);
    transition: box-shadow 0.3s ease, border-color 0.3s ease;
  }
  /* Línea superior neón */
  .cyber-card::before {
    content: '';
    @apply absolute top-0 left-0 right-0 h-px;
    background: linear-gradient(90deg, transparent, #00F5FF, transparent);
    opacity: 0.6;
  }
  /* Esquina decorativa */
  .cyber-card::after {
    content: '';
    @apply absolute top-0 right-0 w-4 h-4 border-t border-r border-cyber-cyan;
    opacity: 0.8;
  }
  .cyber-card:hover {
    border-color: #00F5FF;
    box-shadow: 0 0 20px rgba(0,245,255,0.2), inset 0 0 40px rgba(0,245,255,0.06);
  }

  /* Variante magenta */
  .cyber-card-magenta {
    @apply cyber-card;
    border-color: #80004A;
    box-shadow: 0 0 1px #FF0090, inset 0 0 30px rgba(255,0,144,0.04);
  }
  .cyber-card-magenta::before { background: linear-gradient(90deg, transparent, #FF0090, transparent); }
  .cyber-card-magenta::after { @apply border-cyber-magenta; }
  .cyber-card-magenta:hover {
    border-color: #FF0090;
    box-shadow: 0 0 20px rgba(255,0,144,0.2), inset 0 0 40px rgba(255,0,144,0.06);
  }

  /* Variante yellow */
  .cyber-card-yellow {
    @apply cyber-card;
    border-color: #806000;
    box-shadow: 0 0 1px #FFE000, inset 0 0 30px rgba(255,224,0,0.04);
  }
  .cyber-card-yellow::before { background: linear-gradient(90deg, transparent, #FFE000, transparent); }
  .cyber-card-yellow::after { @apply border-cyber-yellow; }

  /* ── Botones ── */
  .cyber-btn {
    @apply relative inline-flex items-center justify-center gap-2 overflow-hidden;
    @apply px-8 py-3 font-cyber-display text-xs font-bold tracking-widest uppercase;
    @apply cursor-pointer select-none transition-all duration-200;
    clip-path: polygon(12px 0%, 100% 0%, calc(100% - 12px) 100%, 0% 100%);
  }

  .cyber-btn-cyan {
    @apply cyber-btn bg-transparent text-cyber-cyan border border-cyber-cyan-dim;
    box-shadow: 0 4px 0 #007A80, 0 0 15px rgba(0,245,255,0.3);
  }
  .cyber-btn-cyan:hover {
    @apply border-cyber-cyan bg-cyber-cyan text-cyber-void;
    box-shadow: 0 4px 0 #007A80, 0 0 30px rgba(0,245,255,0.6);
  }
  .cyber-btn-cyan:active {
    transform: translateY(4px);
    box-shadow: 0 0 0 #007A80, 0 0 15px rgba(0,245,255,0.3);
  }

  .cyber-btn-magenta {
    @apply cyber-btn bg-transparent text-cyber-magenta border border-cyber-magenta-dim;
    box-shadow: 0 4px 0 #80004A, 0 0 15px rgba(255,0,144,0.3);
  }
  .cyber-btn-magenta:hover {
    @apply border-cyber-magenta bg-cyber-magenta text-cyber-void;
    box-shadow: 0 4px 0 #80004A, 0 0 30px rgba(255,0,144,0.6);
  }
  .cyber-btn-magenta:active {
    transform: translateY(4px);
    box-shadow: 0 0 0 #80004A;
  }

  /* Botón sólido (CTA principal) */
  .cyber-btn-solid {
    @apply cyber-btn bg-cyber-cyan text-cyber-void font-black;
    clip-path: polygon(12px 0%, 100% 0%, calc(100% - 12px) 100%, 0% 100%);
    box-shadow: 0 4px 0 #007A80, 0 0 30px rgba(0,245,255,0.5);
  }
  .cyber-btn-solid:hover {
    box-shadow: 0 4px 0 #007A80, 0 0 50px rgba(0,245,255,0.8);
    filter: brightness(1.1);
  }
  .cyber-btn-solid:active {
    transform: translateY(4px);
    box-shadow: none;
  }

  /* Ghost — sólo texto con glow */
  .cyber-btn-ghost {
    @apply inline-flex items-center gap-2 font-cyber text-xs text-cyber-cyan;
    @apply cursor-pointer transition-all duration-200 uppercase tracking-widest;
    text-shadow: 0 0 8px rgba(0,245,255,0.8);
  }
  .cyber-btn-ghost:hover {
    text-shadow: 0 0 20px rgba(0,245,255,1);
  }

  /* ── Inputs ── */
  .cyber-input {
    @apply w-full bg-cyber-panel font-cyber text-cyber-cyan text-sm;
    @apply border-b-2 border-cyber-cyan-dim px-4 py-3 outline-none;
    @apply transition-all duration-200;
    @apply placeholder:text-cyber-text-dim;
    caret-color: #00F5FF;
  }
  .cyber-input:focus {
    border-color: #00F5FF;
    box-shadow: 0 2px 0 #00F5FF, 0 4px 15px rgba(0,245,255,0.3);
  }

  /* Input box completo */
  .cyber-input-box {
    @apply cyber-input border-2 border-cyber-cyan-dim rounded-none px-4 py-3;
    background: rgba(0, 245, 255, 0.03);
  }
  .cyber-input-box:focus {
    border-color: #00F5FF;
    background: rgba(0, 245, 255, 0.06);
    box-shadow: 0 0 15px rgba(0,245,255,0.15), inset 0 0 15px rgba(0,245,255,0.03);
  }

  /* ── Badge / Tag ── */
  .cyber-badge {
    @apply inline-flex items-center gap-1 px-3 py-1;
    @apply font-cyber text-xs uppercase tracking-widest;
    clip-path: polygon(6px 0%, 100% 0%, calc(100% - 6px) 100%, 0% 100%);
  }
  .cyber-badge-cyan    { @apply cyber-badge bg-transparent text-cyber-cyan border border-cyber-cyan-dim; }
  .cyber-badge-magenta { @apply cyber-badge bg-transparent text-cyber-magenta border border-cyber-magenta-dim; }
  .cyber-badge-yellow  { @apply cyber-badge bg-transparent text-cyber-yellow border border-cyber-yellow-dim; }
  .cyber-badge-solid   { @apply cyber-badge bg-cyber-cyan text-cyber-void font-bold; }

  /* ── Texto con glow ── */
  .neon-text-cyan    { color: #00F5FF; text-shadow: 0 0 10px #00F5FF, 0 0 30px rgba(0,245,255,0.5); }
  .neon-text-magenta { color: #FF0090; text-shadow: 0 0 10px #FF0090, 0 0 30px rgba(255,0,144,0.5); }
  .neon-text-yellow  { color: #FFE000; text-shadow: 0 0 10px #FFE000, 0 0 30px rgba(255,224,0,0.5); }
  .neon-text-green   { color: #00FF41; text-shadow: 0 0 10px #00FF41, 0 0 30px rgba(0,255,65,0.5); }

  /* ── Línea decorativa ── */
  .cyber-divider {
    @apply border-none h-px my-8;
    background: linear-gradient(90deg, transparent, #00F5FF 30%, #00F5FF 70%, transparent);
    box-shadow: 0 0 8px rgba(0,245,255,0.5);
  }

  /* ── Stat / Métrica ── */
  .cyber-stat {
    @apply cyber-card text-center;
  }
  .cyber-stat-value {
    @apply font-cyber-display text-4xl font-black neon-text-cyan;
  }
  .cyber-stat-label {
    @apply font-cyber text-cyber-text-dim text-xs uppercase tracking-widest mt-2;
  }

  /* ── Navbar ── */
  .cyber-nav {
    @apply fixed top-0 left-0 right-0 z-50 flex items-center justify-between;
    @apply bg-cyber-dark border-b border-cyber-cyan-dim px-8 py-4;
    box-shadow: 0 1px 0 #00F5FF, 0 4px 20px rgba(0,245,255,0.1);
  }

  /* ── Terminal / Code block ── */
  .cyber-terminal {
    @apply bg-cyber-surface border border-cyber-cyan-dim rounded-none p-6 font-cyber text-sm;
    box-shadow: 0 0 1px #00F5FF, inset 0 0 40px rgba(0,245,255,0.03);
  }
  .cyber-terminal-prompt::before {
    content: '> ';
    @apply text-cyber-cyan;
    text-shadow: 0 0 8px rgba(0,245,255,0.8);
  }

  /* ── Animaciones utilitarias ── */
  .cyber-flicker    { @apply animate-flicker; }
  .cyber-pulse      { @apply animate-pulse-neon; }
  .cyber-glitch     { @apply animate-glitch; }

  /* ── Scan line decorativa ── */
  .cyber-scan-line {
    @apply fixed left-0 right-0 h-px pointer-events-none z-50 animate-scan;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.4), transparent);
  }
}

@layer utilities {
  /* Clip-path estilo cyberpunk (ángulo cortado) */
  .clip-cyber-sm  { clip-path: polygon(8px 0%, 100% 0%, calc(100% - 8px) 100%, 0% 100%); }
  .clip-cyber-md  { clip-path: polygon(16px 0%, 100% 0%, calc(100% - 16px) 100%, 0% 100%); }
  .clip-cyber-lg  { clip-path: polygon(24px 0%, 100% 0%, calc(100% - 24px) 100%, 0% 100%); }
  .clip-corner-tr { clip-path: polygon(0 0, calc(100% - 20px) 0, 100% 20px, 100% 100%, 0 100%); }
  .clip-corner-all{ clip-path: polygon(16px 0%, calc(100% - 16px) 0%, 100% 16px, 100% calc(100% - 16px), calc(100% - 16px) 100%, 16px 100%, 0 calc(100% - 16px), 0 16px); }
}
```

---

## HTML — Componentes Listos

### Layout con scan line y grid

```html
<body class="bg-cyber-void font-cyber-body text-cyber-text min-h-screen">
  <!-- Scan line animada (opcional, decorativa) -->
  <div class="cyber-scan-line"></div>

  <!-- Contenido -->
  <div class="relative z-10">
    ...
  </div>
</body>
```

### Navbar

```html
<nav class="cyber-nav">
  <div class="flex items-center gap-3">
    <div class="w-2 h-2 bg-cyber-cyan rounded-full animate-pulse-neon shadow-neon-cyan"></div>
    <span class="font-cyber-display text-sm font-bold neon-text-cyan tracking-widest">SYS//NEXUS</span>
  </div>
  <div class="flex items-center gap-6">
    <a href="#" class="font-cyber text-xs text-cyber-text-dim hover:text-cyber-cyan uppercase tracking-widest transition-colors">Sistema</a>
    <a href="#" class="font-cyber text-xs text-cyber-text-dim hover:text-cyber-cyan uppercase tracking-widest transition-colors">Red</a>
    <a href="#" class="font-cyber text-xs text-cyber-text-dim hover:text-cyber-cyan uppercase tracking-widest transition-colors">Acceso</a>
    <button class="cyber-btn-solid text-xs px-6 py-2">INICIAR</button>
  </div>
</nav>
```

### Hero

```html
<section class="min-h-screen flex items-center px-8 md:px-20 pt-24">
  <div class="max-w-3xl">

    <!-- Badge de estado -->
    <div class="flex items-center gap-3 mb-8">
      <div class="w-2 h-2 bg-cyber-green rounded-full animate-pulse shadow-neon-green"></div>
      <span class="cyber-badge-cyan">SISTEMA EN LÍNEA // v4.2.1</span>
    </div>

    <!-- Título con glitch -->
    <h1 class="font-cyber-display text-6xl md:text-8xl font-black leading-none mb-4">
      <span class="neon-text-cyan block cyber-flicker">ACCESO</span>
      <span class="text-cyber-text block">AL FUTURO</span>
      <span class="neon-text-magenta block">AHORA.</span>
    </h1>

    <p class="font-cyber-body text-cyber-text-dim text-lg leading-relaxed max-w-lg mb-10">
      Protocolo de interfaz neural activado. Sistema distribuido con latencia &lt;2ms.
      Encriptación cuántica de extremo a extremo.
    </p>

    <!-- Terminal de código decorativa -->
    <div class="cyber-terminal mb-8 max-w-md">
      <div class="flex items-center gap-2 mb-3 pb-2 border-b border-cyber-cyan-dim">
        <div class="w-2 h-2 rounded-full bg-cyber-magenta"></div>
        <div class="w-2 h-2 rounded-full bg-cyber-yellow"></div>
        <div class="w-2 h-2 rounded-full bg-cyber-cyan"></div>
        <span class="font-cyber text-xs text-cyber-text-dim ml-2">terminal v2.1</span>
      </div>
      <p class="cyber-terminal-prompt text-cyber-text text-xs">conectar --servidor nexus-7</p>
      <p class="text-cyber-cyan text-xs mt-1">✓ Conexión establecida. Bienvenido, usuario.</p>
      <p class="cyber-terminal-prompt text-cyber-text text-xs mt-1">iniciar --protocolo alpha<span class="animate-blink text-cyber-cyan">_</span></p>
    </div>

    <div class="flex items-center gap-6">
      <button class="cyber-btn-solid text-sm px-10 py-4">ACCEDER AL SISTEMA</button>
      <button class="cyber-btn-ghost">explorar protocolos →</button>
    </div>
  </div>
</section>
```

### Grid de cards de datos

```html
<div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-8">

  <div class="cyber-card">
    <div class="cyber-badge-cyan mb-4">MÓDULO 01</div>
    <h3 class="font-cyber-display text-lg neon-text-cyan mb-3">ENCRIPTACIÓN</h3>
    <p class="font-cyber-body text-sm text-cyber-text-dim leading-relaxed">
      Protocolo AES-512 con verificación de integridad en tiempo real.
    </p>
    <div class="cyber-divider"></div>
    <div class="font-cyber text-xs text-cyber-cyan">STATUS: ACTIVO ■</div>
  </div>

  <div class="cyber-card-magenta">
    <div class="cyber-badge-magenta mb-4">MÓDULO 02</div>
    <h3 class="font-cyber-display text-lg neon-text-magenta mb-3">RED NEURAL</h3>
    <p class="font-cyber-body text-sm text-cyber-text-dim leading-relaxed">
      42 nodos activos procesando 1.2 millones de transacciones por segundo.
    </p>
    <div class="border-none h-px my-4" style="background: linear-gradient(90deg, transparent, #FF0090, transparent); box-shadow: 0 0 8px rgba(255,0,144,0.5)"></div>
    <div class="font-cyber text-xs text-cyber-magenta">CARGA: 87.4% ■</div>
  </div>

  <div class="cyber-card-yellow">
    <div class="cyber-badge-yellow mb-4">MÓDULO 03</div>
    <h3 class="font-cyber-display text-lg neon-text-yellow mb-3">ALERTA</h3>
    <p class="font-cyber-body text-sm text-cyber-text-dim leading-relaxed">
      3 anomalías detectadas en sector 7. Protocolo de contención activado.
    </p>
    <div class="border-none h-px my-4" style="background: linear-gradient(90deg, transparent, #FFE000, transparent); box-shadow: 0 0 8px rgba(255,224,0,0.5)"></div>
    <div class="font-cyber text-xs text-cyber-yellow animate-flicker">⚠ REVISIÓN REQUERIDA</div>
  </div>

</div>
```

### Stats / Dashboard

```html
<div class="grid grid-cols-2 md:grid-cols-4 gap-4 p-8">
  <div class="cyber-stat">
    <div class="cyber-stat-value">99.9%</div>
    <div class="cyber-stat-label">Uptime</div>
  </div>
  <div class="cyber-card-magenta text-center p-6">
    <div class="font-cyber-display text-3xl font-black neon-text-magenta">2ms</div>
    <div class="font-cyber text-cyber-text-dim text-xs uppercase tracking-widest mt-2">Latencia</div>
  </div>
  <div class="cyber-stat">
    <div class="cyber-stat-value neon-text-yellow">1.2M</div>
    <div class="cyber-stat-label">TPS</div>
  </div>
  <div class="cyber-card-magenta text-center p-6">
    <div class="font-cyber-display text-3xl font-black neon-text-green">42</div>
    <div class="font-cyber text-cyber-text-dim text-xs uppercase tracking-widest mt-2">Nodos</div>
  </div>
</div>
```

### Formulario de login

```html
<div class="cyber-card max-w-md mx-auto clip-corner-all">
  <!-- Header con icono -->
  <div class="flex items-center gap-3 mb-8">
    <div class="w-3 h-3 bg-cyber-cyan rounded-full shadow-neon-cyan animate-pulse"></div>
    <span class="font-cyber text-xs text-cyber-cyan uppercase tracking-widest">Autenticación requerida</span>
  </div>

  <h2 class="font-cyber-display text-2xl neon-text-cyan mb-8">ACCESO AL SISTEMA</h2>

  <div class="space-y-6">
    <div>
      <label class="font-cyber text-xs text-cyber-text-dim uppercase tracking-widest mb-2 block">
        ID de usuario
      </label>
      <input type="text" placeholder="usr_######" class="cyber-input-box w-full" />
    </div>
    <div>
      <label class="font-cyber text-xs text-cyber-text-dim uppercase tracking-widest mb-2 block">
        Clave de acceso
      </label>
      <input type="password" placeholder="••••••••••••" class="cyber-input-box w-full" />
    </div>
  </div>

  <button class="cyber-btn-solid w-full mt-8 py-4">AUTENTICAR →</button>

  <p class="font-cyber text-xs text-cyber-text-dim text-center mt-4">
    Conexión encriptada // Protocolo TLS 4.0
  </p>
</div>
```

---

## Anti-patrones a Evitar

- ❌ Fondos blancos o claros — cyberpunk SIEMPRE es oscuro
- ❌ `rounded-2xl` o `rounded-full` — los elementos son angulosos, no redondeados
- ❌ Más de 3 colores neón en una misma UI — sobrecarga visual
- ❌ Sombras grises neutras (`shadow-xl`) — siempre sombras de color
- ❌ Tipografías sans-serif comunes — usar monospace o futuristas
- ❌ Animaciones lentas y suaves — el cyberpunk tiene ritmo rápido y glitchy
- ❌ `border-radius` mayor a 4px en la mayoría de elementos
- ❌ Saturación baja en los neones — deben ser BRILLANTES, no pasteles

---

## Casos de Uso Ideales

- Plataformas de gaming y esports
- Dashboards de trading / crypto agresivos
- Portafolios de desarrolladores y hackers
- Tools de seguridad / pentesting
- Apps de ciencia ficción o worldbuilding
- Interfaces de control / monitoreo de sistemas
- Productos tech con público gamer o dev
