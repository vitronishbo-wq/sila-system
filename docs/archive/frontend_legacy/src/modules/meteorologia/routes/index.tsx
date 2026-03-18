/**
 * Meteorologia Routes
 * React Router v6 route definitions for weather monitoring module
 */

import type { RouteObject } from "react-router-dom";
import { MeteorologyPage } from "../pages/MeteorologyPage";

export const meteorologiaRoutes: RouteObject[] = [
  {
    path: "meteorologia",
    element: <MeteorologyPage />,
  },
];
