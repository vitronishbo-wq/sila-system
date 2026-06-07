import React from 'react';
import AdminObservabilitySection from '@/components/AdminObservability';
import ObservabilityOverview from '@/components/ObservabilityOverview';

const AdminObservability: React.FC = () => (
  <section className="space-y-8">
    <ObservabilityOverview />
    <AdminObservabilitySection />
  </section>
);

export default AdminObservability;
