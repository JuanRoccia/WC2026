# Skill: Rendimiento y Optimización

## Descripción

Habilidades para optimizar el rendimiento de la aplicación, tanto en frontend como backend.

---

## 🚀 Temas Cubiertos

### 1. Optimización de Queries Drizzle

```typescript
// ❌ Malo: N+1 queries
const properties = await db.select().from(propertiesTable);
for (const prop of properties) {
  const agency = await db.select().from(agenciesTable)
    .where(eq(agenciesTable.id, prop.agencyId));
}

// ✅ Bueno: Con relaciones
const propertiesWithAgencies = await db.select({
  property: propertiesTable,
  agency: agenciesTable,
})
  .from(propertiesTable)
  .leftJoin(agenciesTable, eq(propertiesTable.agencyId, agenciesTable.id));
```

### 2. Pagination Eficiente

```typescript
// ✅ Usar cursor-based en lugar de offset
const getProperties = async (cursor?: number, limit = 20) => {
  return db.select()
    .from(propertiesTable)
    .where(cursor ? gt(propertiesTable.id, cursor) : undefined)
    .limit(limit)
    .orderBy(asc(propertiesTable.id));
};
```

### 3. React Optimizations

```typescript
// ✅ useMemo para cálculos costosos
const filteredProperties = useMemo(() => {
  return properties.filter(p => 
    p.price >= minPrice && p.price <= maxPrice
  );
}, [properties, minPrice, maxPrice]);

// ✅ useCallback para callbacks
const handlePropertyClick = useCallback((id: string) => {
  navigate(`/property/${id}`);
}, [navigate]);

// ✅ React.memo para componentes
const PropertyCard = memo(({ property }) => (
  <Card>{property.title}</Card>
));
```

### 4. TanStack Query Optimizations

```typescript
// ✅ Configurar stale times apropiados
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutos
      gcTime: 10 * 60 * 1000,   // 10 minutos
    },
  },
});

// ✅ Prefetching
const prefetchProperty = async (id: string) => {
  await queryClient.prefetchQuery({
    queryKey: ['property', id],
    queryFn: () => fetchProperty(id),
  });
};
```

### 5. Lazy Loading

```typescript
// ✅ Lazy load de rutas
const AdminDashboard = lazy(() => import('./pages/admin-dashboard'));

<Suspense fallback={<Loading />}>
  <AdminDashboard />
</Suspense>

// ✅ Lazy load de imágenes
<img loading="lazy" src={prop.imageUrl} alt={prop.title} />
```

---

## 📊 Métricas a Monitorear

| Métrica | Meta |
|---------|------|
| TTFB | < 200ms |
| FCP | < 1.5s |
| LCP | < 2.5s |
| TTI | < 3.5s |
| API Response | < 500ms |

---

## ✅ Checklist de Optimización

### Backend
- [ ] Queries con JOINs apropiados
- [ ] Índices en campos filtrados
- [ ] Pagination implementada
- [ ] Conexiones a DB con timeout

### Frontend
- [ ] useMemo/useCallback donde aplica
- [ ] Lazy loading de rutas
- [ ] Imágenes optimizadas
- [ ] TanStack Query con stale times

---

## 🔧 Herramientas

- React DevTools Profiler
- Chrome Lighthouse
- React Query DevTools

---

*Skill creado: 17 de Marzo de 2026*
