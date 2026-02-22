import { ReactNode } from 'react';

interface ChartWrapperProps {
  title: string;
  children: ReactNode;
}

export function ChartWrapper({ title, children }: ChartWrapperProps) {
  return (
    <div style={{
      marginTop: '4rem',
      background: 'white',
      padding: '2.5rem',
      borderRadius: '18px',
      boxShadow: '0 12px 28px rgba(0,0,0,.1)'
    }}>
      <h3 style={{ marginBottom: '1.5rem' }}>
        {title}
      </h3>
      {children}
    </div>
  );
}
