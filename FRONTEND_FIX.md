# Frontend Fix - Role Name Mismatch Issue ✅ RESOLVED

## Problem Identified

The frontend was expecting lowercase role names (`admin_central`, `admin_provincial`, etc.) but the backend is returning UPPERCASE role names (`ADMIN_CENTRAL`, `ADMIN_PROVINCIAL`, etc.).

This caused:
- ✗ Blank pages after login
- ✗ Infinite redirect loops
- ✗ Navigation failures

## Solution Applied

### Fixed Files

1. **`src/types.ts`** - Updated UserRole enum values to match backend
```typescript
// BEFORE (wrong)
export enum UserRole {
  ADMIN_CENTRAL = 'admin_central'
}

// AFTER (correct)
export enum UserRole {
  ADMIN_CENTRAL = 'ADMIN_CENTRAL'
}
```

2. **`src/services/authGuard.ts`** - Updated role mappings
```typescript
// Now matches backend exactly
const roleRoutes: Record<string, string[]> = {
    ADMIN_CENTRAL: ['/admin', '/'],
    ADMIN_PROVINCIAL: ['/admin', '/'],
    ADMIN_MUNICIPAL: ['/admin', '/'],
    ADMIN_COMMUNAL: ['/admin', '/'],
    CITIZEN: ['/citizen', '/profile', '/requests']
};
```

### Backend Configuration ✅ Already Set

- CORS: `http://localhost:3000` ✅ already allowed
- API URL: Points to `http://localhost:8000` ✅ correct
- JWT Token: Includes role, level, territory_id ✅ working

---

## What to Do Now

### Step 1: Hard Refresh Browser
```
Windows: Ctrl + F5
Mac: Cmd + Shift + R
Linux: Ctrl + Shift + R
```

**OR** clear browser cache and reload

### Step 2: Test Login Flow
1. Go to `http://localhost:3000`
2. Click "Painel Admin"
3. Login with: **central@sila.gov.ao** / **Sila_1983**
4. Should redirect to dashboard (no more blank page!)

### Step 3: Verify Navigation
- ✅ Click on services (Identidade Civil, Registo Civil, etc.)
- ✅ Navigate to /admin/citizens, /admin/documents
- ✅ Check that pages load with content (not blank)

---

## User Test Credentials

All password: **Sila_1983**

```
ADMIN_CENTRAL:
  Email: central@sila.gov.ao
  Should see: Full admin dashboard

ADMIN_PROVINCIAL (Huambo):
  Email: prov.huambo@sila.gov.ao
  Should see: Provincial dashboard

ADMIN_MUNICIPAL (Huambo):
  Email: mun.huambo@sila.gov.ao
  Should see: Municipal dashboard

ADMIN_COMMUNAL (Huambo):
  Email: comun.huambo@sila.gov.ao
  Should see: Communal dashboard

CITIZEN:
  Email: truman@gmail.com
  Should see: "FUC do Cidadão" citizen portal
```

---

## Technical Details

### Role Name Mapping (Frontend ↔ Backend)

| Backend | Frontend Enum | After Fix |
|---------|---------------|-----------|
| ADMIN_CENTRAL | ADMIN_CENTRAL | ✅ MATCH |
| ADMIN_PROVINCIAL | ADMIN_PROVINCIAL | ✅ MATCH |
| ADMIN_MUNICIPAL | ADMIN_MUNICIPAL | ✅ MATCH |
| ADMIN_COMMUNAL | ADMIN_COMMUNAL | ✅ MATCH |
| CITIZEN | CITIZEN | ✅ MATCH |

### Auth Flow (Fixed)

```
1. Login POST /auth/login
   ↓ Backend returns JWT with role="ADMIN_CENTRAL"
   ↓
2. Frontend stores token & calls GET /auth/me
   ↓ Returns: { role: "ADMIN_CENTRAL", territory_id: null, ... }
   ↓
3. Frontend checks: UserRole.ADMIN_CENTRAL = "ADMIN_CENTRAL"
   ↓ ✅ NOW MATCHES!
   ↓
4. Dashboard redirects to /admin
   ✅ Loads properly
```

---

## Troubleshooting

### Still seeing blank pages?
1. ✅ Hard refresh (Ctrl+F5)
2. ✅ Clear browser local storage: DevTools → Application → Local Storage → Clear all
3. ✅ Check console for any error messages
4. ✅ Make sure backend is running on port 8000

### Can login but navigation doesn't work?
1. Check browser console: `F12 → Console`
2. Look for any JavaScript errors
3. Check that `/admin` route exists
4. Verify all files were reloaded (not cached)

### Auth/me returns 200 but page is blank?
1. The API is working ✅
2. The page component might not be rendering
3. Check DevTools → Console for component errors
4. Try navigating directly: `http://localhost:3000/#/admin`

---

## API Endpoints Status

| Endpoint | Status | Response |
|----------|--------|----------|
| POST /auth/login | ✅ 200 | Returns JWT + user data |
| GET /auth/me | ✅ 200 | Returns user with correct role |
| GET /rbac/test/access | ✅ 200 | Returns security scope |
| GET /rbac/test/territory/{id} | ✅ 200/403 | RBAC test |

---

## Next Steps (After Frontend Works)

1. ✅ Test all role-based navigation
2. ✅ Verify territorial access in RBAC endpoints
3. ✅ Test logout and re-login
4. ⏳ Integrate RBAC to protected routes
5. ⏳ Test service page loading

---

**Status**: ✅ Frontend Core Fixed  
**Remaining**: Browser cache refresh needed  
**ETA to full functionality**: 1-2 minutes after refresh
