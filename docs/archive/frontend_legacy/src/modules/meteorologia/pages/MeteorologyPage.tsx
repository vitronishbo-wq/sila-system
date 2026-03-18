/**
 * MeteorologyPage
 * Standalone route component for weather monitoring dashboard
 */

import React from "react";
import { MeteorologyWidget } from "../components";

export function MeteorologyPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto p-6">
        <MeteorologyWidget standalone={true} />
      </div>
    </div>
  );
}
