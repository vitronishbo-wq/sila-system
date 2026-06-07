import React from 'react';
import type { LucideIcon } from 'lucide-react';
import CitizenAreaBanner from '@/components/Services/CitizenAreaBanner';

interface ServiceAction {
  title: string;
  description: string;
  cta: string;
  colorClass: string;
  icon: LucideIcon;
  onClick: () => void;
}

interface ServiceTimelineItem {
  step: number;
  title: string;
  days: string;
  desc: string;
}

interface ServiceLandingProps {
  title: string;
  subtitle: string;
  actions: ServiceAction[];
  requirements: string[];
  timeline: ServiceTimelineItem[];
  infoTitle: string;
  infoItems: string[];
}

export const ServiceLanding: React.FC<ServiceLandingProps> = ({
  title,
  subtitle,
  actions,
  requirements,
  timeline,
  infoTitle,
  infoItems
}) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">{title}</h1>
          <p className="text-slate-600">{subtitle}</p>
        </div>
      </div>

      <CitizenAreaBanner />

      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {actions.map((action) => (
            <button
              key={action.title}
              onClick={action.onClick}
              className="group bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 p-8 text-left border border-slate-200 hover:scale-105"
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`p-4 rounded-xl transition ${action.colorClass}`}>
                  <action.icon className="h-8 w-8 text-white" />
                </div>
                <span className="text-slate-400 group-hover:text-blue-600 transition">→</span>
              </div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">{action.title}</h2>
              <p className="text-slate-600 text-sm mb-4">{action.description}</p>
              <div className="flex items-center text-blue-600 text-sm font-semibold">
                {action.cta} <span className="ml-2">→</span>
              </div>
            </button>
          ))}
        </div>

        <div className="bg-white rounded-2xl shadow-md p-8 border border-slate-200 mb-8">
          <h3 className="font-bold text-gray-900 text-lg mb-4">Requisitos Importantes</h3>
          <ul className="space-y-2 text-slate-700 text-sm">
            {requirements.map((req) => (
              <li key={req} className="flex items-center gap-3">
                <span className="flex-shrink-0 w-1.5 h-1.5 bg-blue-600 rounded-full"></span>
                {req}
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-white rounded-2xl shadow-md p-8 border border-slate-200">
          <div className="flex items-center gap-3 mb-6">
            <span className="text-blue-600 font-bold">⏱</span>
            <h3 className="font-bold text-gray-900 text-lg">Processo de Atendimento</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {timeline.map((item) => (
              <div key={item.step} className="text-center p-4 rounded-xl bg-slate-50 hover:bg-blue-50 transition">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 text-blue-600 rounded-full font-bold mb-3 mx-auto">
                  {item.step}
                </div>
                <p className="font-semibold text-gray-900 text-sm mb-1">{item.title}</p>
                <p className="text-xs text-blue-600 font-semibold mb-1">{item.days}</p>
                <p className="text-xs text-slate-500">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-2xl p-6">
          <h4 className="font-bold text-blue-900 mb-3">{infoTitle}</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
            {infoItems.map((item) => (
              <p key={item}>• {item}</p>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ServiceLanding;
