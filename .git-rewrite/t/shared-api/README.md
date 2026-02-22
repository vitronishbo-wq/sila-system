# @sila/shared-api

This package provides typed API clients, hooks and utilities to integrate with Sila backend.

Usage:

```ts
import { useAuth, useApi } from '@sila/shared-api';

const { user, login } = useAuth();
const client = useApi();
```

This package is meant to be consumed by the frontend app (Vite + React + TypeScript). It exposes functions for authentication, user fetching and general API requests. Configure `VITE_API_BASE_URL` in your frontend app.
