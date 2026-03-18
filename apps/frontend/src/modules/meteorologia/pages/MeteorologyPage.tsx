/**
 * Meteorologia Page - Standalone route component
 * Accessible at /meteorologia
 */

import React from 'react';
import { MeteorologyWidget } from '../components';

export const MeteorologyPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto p-6">
        <MeteorologyWidget standalone={true} />
      </div>
    </div>
  );
};
