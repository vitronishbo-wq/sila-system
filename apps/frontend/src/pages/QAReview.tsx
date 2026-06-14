import React, { useEffect, useState } from 'react';

type IndexFile = { pages: string[]; files?: string[] };

const QAReview: React.FC = () => {
  const [pages, setPages] = useState<string[]>([]);
  const [selected, setSelected] = useState<string | null>(null);

  useEffect(() => {
    fetch('/qa-viewer/index.json')
      .then((r) => r.json())
      .then((data: IndexFile) => setPages(data.pages || []))
      .catch(() => setPages([]));
  }, []);

  return (
    <div className="p-6 min-h-screen bg-slate-900 text-white">
      <h1 className="text-2xl font-bold mb-4">QA Viewer</h1>
      <div className="flex gap-4">
        <div className="w-64 bg-slate-800 p-3 rounded overflow-auto">
          <ul className="space-y-2">
            {pages.length === 0 && <li>Nenhuma página QA encontrada</li>}
            {pages.map((p) => (
              <li key={p}>
                <button
                  className={`w-full text-left px-2 py-1 rounded hover:bg-slate-700 ${selected === p ? 'bg-slate-700' : ''}`}
                  onClick={() => setSelected(p)}
                >
                  {p}
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div className="flex-1 bg-white rounded overflow-hidden">
          {selected ? (
            <iframe title="qa-viewer" src={`/qa-viewer/${selected}`} className="w-full h-[80vh]" />
          ) : (
            <div className="p-6 text-slate-700">Selecione uma página para visualizar o QA</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default QAReview;
