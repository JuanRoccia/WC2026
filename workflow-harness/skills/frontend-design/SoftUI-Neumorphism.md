---
name: softui-neumorphism-design
description: Diseño web con estética Soft UI / Neumorphism. Usar cuando el usuario quiere interfaces con sensación táctil y de relieve, sombras internas y externas simétricas, paleta neutra monocromática y apariencia de elementos que emergen o se hunden del fondo. Ideal para apps de salud, dashboards de productividad, wearables, apps de bienestar, controles de audio/smart home y cualquier UI que quiera sentirse "física" y touchable.
---

# SKILL: Soft UI / Neumorphism Design

## Concepto

El **Neumorphism** (New + Skeuomorphism) simula materiales físicos moldeados desde el fondo: los elementos parecen extruidos o hundidos en la superficie. Se logra con sombras simétricas de dos colores (una clara, una oscura) sobre un fondo de color neutro. El resultado es suave, táctil y casi "presionable".

Referentes: dribbble shots de Michal Malewicz, apps de salud iOS, interfaces de smart home, controles de audio analógico.

**⚠️ Advertencia de uso**: Neumorphism tiene problemas de accesibilidad (bajo contraste). Siempre complementar con indicadores de estado claros y asegurar WCAG AA donde sea crítico.

---

## Reglas de Diseño

### Principios Fundamentales
1. **El fondo y los elementos son del MISMO color base** — el efecto viene solo de las sombras
2. **Dos sombras opuestas**: una clara arriba-izquierda, una oscura abajo-derecha
3. **Sin bordes duros** — si hay borde, es del mismo tono que el fondo
4. **Paleta monocromática** — máximo 1-2 acentos de color para estados activos
5. **Border-radius generoso** — los elementos son suaves y redondeados (12px–50px)
6. **Gradientes mínimos** — si se usan, son sutilísimos dentro del mismo tono

---

## Sistema de Sombras (el corazón del estilo)

```css
/* Fórmula base: bg = #E0E5EC (gris azulado suave) */

:root {
  --bg: #E0E5EC;
  --bg-dark: #C8CDD8;  /* bg oscurecido ~15% */
  --bg-light: #FFFFFF; /* bg aclarado */
  
  /* Sombras convexas (elemento que sobresale) */
  --shadow-raised:
    8px 8px 16px #B8BEC8,
    -8px -8px 16px #FFFFFF;
  
  /* Sombras cóncavas (elemento hundido / pressed) */
  --shadow-inset:
    inset 6px 6px 12px #B8BEC8,
    inset -6px -6px 12px #FFFFFF;
  
  /* Variante suave (elementos pequeños) */
  --shadow-sm:
    4px 4px 8px #B8BEC8,
    -4px -4px 8px #FFFFFF;
  
  /* Variante grande (cards principales) */
  --shadow-lg:
    12px 12px 24px #A8AEB8,
    -12px -12px 24px #FFFFFF;
}

/* Cómo calcular las sombras para cualquier color de fondo:
   - Sombra oscura: mismo hue, saturación similar, lightness -15 a -20%
   - Sombra clara: mismo hue, lightness +15 a +20% (o blanco)
   - Offset X e Y: iguales (simetría es clave)
   - Blur: 2x el offset */
```

---

## Paletas de Color Base

| Nombre | Bg | Sombra Oscura | Sombra Clara | Acento |
|--------|-----|--------------|--------------|--------|
| Gris Azulado (clásico) | `#E0E5EC` | `#B8BEC8` | `#FFFFFF` | `#6C8EF5` |
| Beige Cálido | `#ECE8E1` | `#C4BFB8` | `#FFFFFF` | `#E07B54` |
| Verde Menta | `#E0EDE8` | `#B8C5BE` | `#FFFFFF` | `#3DAA7A` |
| Malva Suave | `#EDE0EC` | `#C5B8C4` | `#FFFFFF` | `#9B59B6` |
| Dark Soft UI | `#2D3047` | `#1E2130` | `#3C4060` | `#5B8BF5` |

```css
/* Ejemplo de aplicación */
body {
  background: #E0E5EC;
  min-height: 100vh;
}
```

---

## Tipografía

La tipografía en Soft UI debe ser suave y redondeada, sin agresividad:

```html
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
```

```css
body {
  font-family: 'Nunito', sans-serif;
  color: #6B7280;        /* gris medio — nunca negro puro */
}

h1, h2, h3 {
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  color: #4B5563;
}

/* El texto nunca es negro puro — siempre con un tinte del color bg */
.text-primary   { color: #374151; }
.text-secondary { color: #6B7280; }
.text-muted     { color: #9CA3AF; }
```

---

## Componentes Clave

### Card Base (convexo)
```css
.neu-card {
  background: #E0E5EC;
  border-radius: 20px;
  padding: 2rem;
  box-shadow:
    8px 8px 16px #B8BEC8,
    -8px -8px 16px #FFFFFF;
}
```

### Botón (convexo por defecto, cóncavo al presionar)
```css
.neu-btn {
  background: #E0E5EC;
  border: none;
  border-radius: 50px;
  padding: 0.75rem 2rem;
  font-weight: 600;
  color: #6B7280;
  cursor: pointer;
  box-shadow:
    5px 5px 10px #B8BEC8,
    -5px -5px 10px #FFFFFF;
  transition: all 0.15s ease;
  outline: none;
}

.neu-btn:hover {
  color: #4B5563;
}

.neu-btn:active,
.neu-btn.active {
  box-shadow:
    inset 4px 4px 8px #B8BEC8,
    inset -4px -4px 8px #FFFFFF;
  color: #374151;
}
```

### Botón con Acento de Color (estado activo)
```css
.neu-btn-accent {
  background: linear-gradient(145deg, #7098F8, #5B8BF5);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 0.75rem 2rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow:
    5px 5px 12px #B8BEC8,
    -3px -3px 8px #FFFFFF,
    inset 2px 2px 4px rgba(255,255,255,0.3);
  transition: all 0.2s ease;
}

.neu-btn-accent:hover {
  box-shadow:
    6px 6px 14px #B0B6C0,
    -4px -4px 10px #FFFFFF,
    inset 2px 2px 4px rgba(255,255,255,0.3);
}
```

### Input / Campo de texto
```css
.neu-input {
  background: #E0E5EC;
  border: none;
  border-radius: 12px;
  padding: 0.85rem 1.2rem;
  color: #374151;
  font-size: 0.95rem;
  outline: none;
  box-shadow:
    inset 4px 4px 8px #B8BEC8,
    inset -4px -4px 8px #FFFFFF;
  transition: box-shadow 0.2s;
  width: 100%;
}

.neu-input::placeholder { color: #9CA3AF; }

.neu-input:focus {
  box-shadow:
    inset 4px 4px 10px #B0B6C0,
    inset -4px -4px 10px #FFFFFF,
    0 0 0 3px rgba(91, 139, 245, 0.2);
}
```

### Toggle / Switch
```css
.neu-toggle {
  width: 56px;
  height: 28px;
  background: #E0E5EC;
  border-radius: 50px;
  box-shadow:
    inset 3px 3px 6px #B8BEC8,
    inset -3px -3px 6px #FFFFFF;
  position: relative;
  cursor: pointer;
  transition: all 0.3s;
}

.neu-toggle .knob {
  position: absolute;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #E0E5EC;
  top: 3px; left: 3px;
  box-shadow:
    3px 3px 6px #B8BEC8,
    -2px -2px 5px #FFFFFF;
  transition: transform 0.3s ease;
}

.neu-toggle.on {
  background: linear-gradient(145deg, #6490F6, #5B8BF5);
}
.neu-toggle.on .knob {
  transform: translateX(28px);
}
```

### Slider / Knob de audio
```css
.neu-slider {
  -webkit-appearance: none;
  background: #E0E5EC;
  border-radius: 50px;
  height: 8px;
  box-shadow:
    inset 3px 3px 6px #B8BEC8,
    inset -3px -3px 6px #FFFFFF;
  outline: none;
}

.neu-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #E0E5EC;
  box-shadow:
    3px 3px 6px #B8BEC8,
    -2px -2px 5px #FFFFFF;
  cursor: pointer;
}
```

### Icono / Avatar container
```css
.neu-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: #E0E5EC;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    6px 6px 12px #B8BEC8,
    -6px -6px 12px #FFFFFF;
}
```

---

## Indicador de Progreso

```css
.neu-progress-track {
  background: #E0E5EC;
  border-radius: 50px;
  height: 10px;
  box-shadow:
    inset 3px 3px 6px #B8BEC8,
    inset -3px -3px 6px #FFFFFF;
  overflow: hidden;
}

.neu-progress-fill {
  height: 100%;
  border-radius: 50px;
  background: linear-gradient(90deg, #6490F6, #5B8BF5);
  box-shadow: 2px 0 8px rgba(91, 139, 245, 0.4);
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## Animaciones

El Soft UI usa transiciones suaves y contenidas:

```css
/* Transición de pressed state */
.neu-pressable {
  transition: box-shadow 0.15s ease, transform 0.1s ease;
}

.neu-pressable:active {
  transform: scale(0.98);
  box-shadow:
    inset 4px 4px 8px #B8BEC8,
    inset -4px -4px 8px #FFFFFF;
}

/* Aparición de cards */
@keyframes softReveal {
  from {
    opacity: 0;
    transform: scale(0.97);
    box-shadow: none;
  }
  to {
    opacity: 1;
    transform: scale(1);
    box-shadow: 8px 8px 16px #B8BEC8, -8px -8px 16px #FFFFFF;
  }
}
```

---

## Anti-patrones a Evitar

- ❌ Usar sobre fondo blanco puro o negro — las sombras no funcionan en extremos
- ❌ Texto negro `#000000` sobre el fondo neutro — demasiado contraste agresivo
- ❌ Mezclar neumorphism con bordes duros o sombras con offset (neobrutalism) — estilos incompatibles
- ❌ Saturación alta en el bg — destruye el efecto sutil (el bg debe ser casi neutro)
- ❌ Elementos sin suficiente separación — el efecto necesita espacio para verse correctamente
- ❌ Usarlo en elementos de texto críticos sin contraste adicional — problema de accesibilidad

---

## Casos de Uso Ideales

- Apps de salud, meditación y bienestar (Calm, Headspace-like)
- Interfaces de smart home y wearables
- Controles de audio / reproductores de música
- Dashboards de productividad personal
- Apps de finanzas personales (tracking de gastos)
- Paneles de configuración (settings UI)
- Apps de fitness y tracking de ejercicio
