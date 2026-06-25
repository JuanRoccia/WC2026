# Skill: Seguridad

## Descripción

Habilidades relacionadas con la seguridad de la aplicación, incluyendo protección contra vulnerabilidades comunes, headers de seguridad, rate limiting, y mejores prácticas de autenticación.

---

## 🛡️ Temas Cubiertos

### 1. Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

// Rate limiter para login
export const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 5, // 5 intentos
  message: { error: 'Demasiados intentos de login. Intenta en 15 minutos.' },
  standardHeaders: true,
  legacyHeaders: false,
});

// Rate limiter para API
export const apiLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minuto
  max: 100, // 100 requests
  message: { error: 'Too many requests' },
});
```

### 2. Helmet.js

```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
  },
}));
```

### 3. Cookies Seguras

```typescript
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 24 * 60 * 60 * 1000, // 24 horas
  },
  store: PostgreSQLStore,
  resave: false,
  saveUninitialized: false,
}));
```

### 4. Validación con Zod

```typescript
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(8, 'Mínimo 8 caracteres')
    .regex(/[A-Z]/, 'Debe tener mayúscula')
    .regex(/[a-z]/, 'Debe tener minúscula')
    .regex(/[0-9]/, 'Debe tener número'),
});
```

### 5. Headers de Seguridad

```typescript
// X-Frame-Options
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  next();
});
```

---

## ✅ Checklist de Seguridad

- [ ] Rate limiting en rutas sensibles
- [ ] Helmet.js configurado
- [ ] Cookies con httpOnly, secure, sameSite
- [ ] Validación de entrada robusta
- [ ] Logging de eventos de seguridad
- [ ] No exposición de datos sensibles en errores

---

## 📚 Recursos

- [express-rate-limit](https://github.com/express-rate-limit/express-rate-limit)
- [helmet](https://helmetjs.github.io/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

*Skill creado: 17 de Marzo de 2026*
