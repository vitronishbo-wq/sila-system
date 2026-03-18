/**
 * Meteorologia Routes - Module routing configuration
 */

import React from 'react';
import type { RouteObject } from 'react-router-dom';
import { MeteorologyPage } from '../pages/MeteorologyPage';

export const meteorologiaRoutes: RouteObject[] = [
  {
    path: 'meteorologia',
    element: <MeteorologyPage />,
  },
];
