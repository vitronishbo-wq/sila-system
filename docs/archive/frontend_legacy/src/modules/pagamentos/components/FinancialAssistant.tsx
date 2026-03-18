import React from 'react';

const FinancialAssistant: React.FC = () => {
  return (
    <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-400">Assistente Financeiro</p>
          <h3 className="text-lg font-semibold text-slate-900">Sugestões inteligentes</h3>
        </div>
        <span className="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">
          Em breve
        </span>
      </div>
      <p className="mt-3 text-sm text-slate-600">
        Insights automáticos sobre faturas, pagamentos e inadimplência estarão disponíveis aqui.
      </p>
    </div>
  );
};

export default FinancialAssistant;
