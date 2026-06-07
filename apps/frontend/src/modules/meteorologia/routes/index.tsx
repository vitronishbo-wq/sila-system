/**
 * Meteorologia Routes - Module routing configuration
 */

import type { RouteObject } from 'react-router-dom';
import { MeteorologyPage } from '@/modules/meteorologia/pages/MeteorologyPage';

export const meteorologiaRoutes: RouteObject[] = [
  {
    path: 'meteorologia',
    element: <MeteorologyPage />,
  },
];
