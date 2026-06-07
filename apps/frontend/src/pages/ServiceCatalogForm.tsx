import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { API_URL } from '@/constants';
import CitizenAreaBanner from '@/components/Services/CitizenAreaBanner';

type CatalogField = {
  key: string;
  label: string;
  type?: string;
  required?: boolean;
  options?: string[];
  placeholder?: string;
  mask?: string;
  helper?: string;
  multiple?: boolean;
  depends_on?: {
    field: string;
    value: string | number | boolean;
  };
};

type CatalogItem = {
  code: string;
  name: string;
  category?: string;
  description?: string;
  price?: number;
};

type CatalogSchema = {
  version?: string;
  groups: Array<{
    key: string;
    label: string;
    fields: CatalogField[];
  }>;
  validations?: Array<{
    field: string;
    type: string;
    message: string;
  }>;
  dependencies?: Array<{
    field: string;
    value: string | number | boolean;
    requires: string[];
    message?: string;
  }>;
};

const buildHeaders = () => {
  const token = localStorage.getItem('citizen_token')
    || localStorage.getItem('access_token')
    || localStorage.getItem('token');
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return headers;
};

const ServiceCatalogForm: React.FC = () => {
  const { code } = useParams();
  const navigate = useNavigate();
  const [item, setItem] = useState<CatalogItem | null>(null);
  const [schema, setSchema] = useState<CatalogSchema | null>(null);
  const [formData, setFormData] = useState<Record<string, string | boolean | string[]>>({});
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const formTitle = useMemo(() => item?.name ?? code ?? 'Servico', [item, code]);

  useEffect(() => {
    if (!code) {
      setError('Servico nao encontrado');
      setIsLoading(false);
      return;
    }

    const loadForm = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const [itemRes, formRes] = await Promise.all([
          fetch(`${API_URL}service-catalog/${encodeURIComponent(code)}`, { headers: buildHeaders() }),
          fetch(`${API_URL}service-catalog/${encodeURIComponent(code)}/form`, { headers: buildHeaders() })
        ]);
        if (!itemRes.ok || !formRes.ok) {
          throw new Error('Falha ao carregar formulario');
        }
        const itemData = await itemRes.json();
        const formData = await formRes.json();
        setItem(itemData);
        setSchema(formData.schema || null);
      } catch (err) {
        console.error('Erro ao carregar formulario:', err);
        setError('Nao foi possivel carregar o formulario.');
      } finally {
        setIsLoading(false);
      }
    };

    loadForm();
  }, [code]);

  const handleChange = (key: string, value: string | boolean | string[]) => {
    setFieldErrors((prev) => {
      if (!prev[key]) return prev;
      const next = { ...prev };
      delete next[key];
      return next;
    });
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const applyMask = (value: string, mask?: string) => {
    if (!mask) return value;
    if (mask === 'nif') {
      return value.replace(/\D/g, '').slice(0, 10);
    }
    if (mask === 'bi') {
      return value.replace(/[^a-zA-Z0-9]/g, '').toUpperCase().slice(0, 14);
    }
    return value;
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!code) {
      return;
    }
    const validationErrors = validateSchema(schema, formData);
    if (Object.keys(validationErrors).length > 0) {
      setFieldErrors(validationErrors);
      setError('Existem campos obrigatorios por preencher.');
      return;
    }
    setError(null);
    try {
      const response = await fetch(`${API_URL}service-catalog/${encodeURIComponent(code)}/submit`, {
        method: 'POST',
        headers: buildHeaders(),
        body: JSON.stringify({ fields: formData })
      });
      if (!response.ok) {
        throw new Error('Falha ao submeter');
      }
      const data = await response.json();
      const orderId = data.order_id;
      if (orderId) {
        const uploadFields = (schema?.groups ?? [])
          .flatMap((group) => group.fields)
          .filter((field) => field.type === 'upload');
        if (uploadFields.length > 0) {
          const uploadKeys = uploadFields.map((field) => field.key).join(',');
          navigate(`/citizen/documents/upload?service=${encodeURIComponent(code)}&orderId=${orderId}&uploadFields=${encodeURIComponent(uploadKeys)}`);
          return;
        }
        navigate(`/citizen/payments?service=${encodeURIComponent(code)}&orderId=${orderId}`);
      } else {
        navigate('/citizen/portal');
      }
    } catch (err) {
      console.error('Erro ao submeter formulario:', err);
      setError('Nao foi possivel submeter o pedido.');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-100">
        <div className="text-sm text-slate-500">A carregar formulario...</div>
      </div>
    );
  }

  if (error || !item) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-100">
        <div className="bg-white rounded-xl shadow p-8 text-center">
          <p className="text-red-600">{error ?? 'Servico indisponivel'}</p>
          <button
            onClick={() => navigate('/citizen/portal')}
            className="mt-4 px-4 py-2 bg-slate-900 text-white rounded-lg"
          >
            Voltar ao portal
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="bg-white border-b border-slate-200">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <h1 className="text-3xl font-bold text-slate-900">{formTitle}</h1>
          <p className="text-sm text-slate-500">{item.description ?? 'Preencha o formulario para iniciar o pedido.'}</p>
        </div>
      </div>

      <CitizenAreaBanner />

      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto px-6 py-8 space-y-6">
        <div className="bg-white rounded-2xl shadow p-6 border border-slate-200 space-y-4">
          {error && (
            <div className="rounded-lg border border-red-200 bg-red-50 text-red-700 text-sm px-3 py-2">
              {error}
            </div>
          )}
          {(schema?.groups ?? []).map((group) => (
            <div key={group.key} className="space-y-4">
              <div className="text-sm font-semibold text-slate-700">{group.label}</div>
              {group.fields.map((field) => {
                const value = formData[field.key] ?? '';
                const label = field.required ? `${field.label} *` : field.label;
                if (field.depends_on) {
                  const dependencyValue = formData[field.depends_on.field];
                  if (dependencyValue !== field.depends_on.value) {
                    return null;
                  }
                }
                if (field.type === 'textarea') {
                  return (
                    <label key={field.key} className="block text-sm font-medium text-slate-700">
                      {label}
                      <textarea
                        value={String(value)}
                        onChange={(event) => handleChange(field.key, event.target.value)}
                        className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder={field.placeholder ?? ''}
                        rows={4}
                        required={field.required}
                      />
                      {fieldErrors[field.key] && (
                        <p className="text-xs text-red-600 mt-1">{fieldErrors[field.key]}</p>
                      )}
                      {field.helper && <p className="text-xs text-slate-400 mt-1">{field.helper}</p>}
                    </label>
                  );
                }
                if (field.type === 'select') {
                  return (
                    <label key={field.key} className="block text-sm font-medium text-slate-700">
                      {label}
                      <select
                        value={String(value)}
                        onChange={(event) => handleChange(field.key, event.target.value)}
                        className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required={field.required}
                      >
                        <option value="">Selecione...</option>
                        {(field.options ?? []).map((option) => (
                          <option key={option} value={option}>
                            {option}
                          </option>
                        ))}
                      </select>
                      {fieldErrors[field.key] && (
                        <p className="text-xs text-red-600 mt-1">{fieldErrors[field.key]}</p>
                      )}
                      {field.helper && <p className="text-xs text-slate-400 mt-1">{field.helper}</p>}
                    </label>
                  );
                }
                if (field.type === 'radio') {
                  return (
                    <div key={field.key} className="block text-sm font-medium text-slate-700">
                      <span className="block">{label}</span>
                      <div className="mt-2 flex flex-wrap gap-3">
                        {(field.options ?? []).map((option) => (
                          <label key={option} className="inline-flex items-center gap-2 text-sm text-slate-600">
                            <input
                              type="radio"
                              name={field.key}
                              value={option}
                              checked={value === option}
                              onChange={(event) => handleChange(field.key, event.target.value)}
                              required={field.required}
                            />
                            {option}
                          </label>
                        ))}
                      </div>
                      {fieldErrors[field.key] && (
                        <p className="text-xs text-red-600 mt-1">{fieldErrors[field.key]}</p>
                      )}
                      {field.helper && <p className="text-xs text-slate-400 mt-1">{field.helper}</p>}
                    </div>
                  );
                }
                if (field.type === 'checkbox') {
                  return (
                    <label key={field.key} className="flex items-start gap-3 text-sm text-slate-700">
                      <input
                        type="checkbox"
                        checked={Boolean(value)}
                        onChange={(event) => handleChange(field.key, event.target.checked)}
                        required={field.required}
                        className="mt-1"
                      />
                      <span>
                        {label}
                        {fieldErrors[field.key] && (
                          <span className="block text-xs text-red-600 mt-1">{fieldErrors[field.key]}</span>
                        )}
                        {field.helper && <span className="block text-xs text-slate-400 mt-1">{field.helper}</span>}
                      </span>
                    </label>
                  );
                }
                if (field.type === 'upload') {
                  return (
                    <label key={field.key} className="block text-sm font-medium text-slate-700">
                      {label}
                      <input
                        type="file"
                        multiple={Boolean(field.multiple)}
                        onChange={(event) => {
                          const files = Array.from(event.target.files ?? []);
                          const names = files.map((file) => file.name);
                          handleChange(field.key, names);
                        }}
                        className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm"
                        required={field.required}
                      />
                      {Array.isArray(value) && value.length > 0 && (
                        <p className="text-xs text-slate-500 mt-1">Selecionados: {value.join(', ')}</p>
                      )}
                      {fieldErrors[field.key] && (
                        <p className="text-xs text-red-600 mt-1">{fieldErrors[field.key]}</p>
                      )}
                      {field.helper && <p className="text-xs text-slate-400 mt-1">{field.helper}</p>}
                    </label>
                  );
                }
                const maskedValue = typeof value === 'string'
                  ? applyMask(value, field.mask ?? field.type)
                  : '';
                const inputType = field.type === 'number' ? 'number' : field.type === 'date' ? 'date' : 'text';
                return (
                  <label key={field.key} className="block text-sm font-medium text-slate-700">
                    {label}
                    <input
                      type={inputType}
                      value={maskedValue}
                      onChange={(event) => handleChange(field.key, applyMask(event.target.value, field.mask ?? field.type))}
                      inputMode={field.type === 'nif' ? 'numeric' : undefined}
                      className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder={field.placeholder ?? ''}
                      required={field.required}
                    />
                    {fieldErrors[field.key] && (
                      <p className="text-xs text-red-600 mt-1">{fieldErrors[field.key]}</p>
                    )}
                    {field.helper && <p className="text-xs text-slate-400 mt-1">{field.helper}</p>}
                  </label>
                );
              })}
            </div>
          ))}
        </div>

        <div className="flex items-center justify-between">
          <button
            type="button"
            onClick={() => navigate('/citizen/portal')}
            className="px-4 py-2 text-sm font-semibold text-slate-600 hover:text-slate-900"
          >
            Voltar
          </button>
          <button
            type="submit"
            className="px-5 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700"
          >
            Submeter pedido
          </button>
        </div>
      </form>
    </div>
  );
};

export default ServiceCatalogForm;

function validateSchema(
  this: void,
  schema?: CatalogSchema | null,
  data?: Record<string, string | boolean | string[]>
): Record<string, string> {
  if (!schema || !data) {
    return {};
  }
  const errors: Record<string, string> = {};
  const isVisible = (field: CatalogField) => {
    if (!field.depends_on) return true;
    return data[field.depends_on.field] === field.depends_on.value;
  };

  const allFields = schema.groups.flatMap((group) => group.fields);
  for (const field of allFields) {
    if (!isVisible(field)) continue;
    const value = data[field.key];
    if (field.required) {
      if (field.type === 'checkbox' && !value) {
        errors[field.key] = 'Campo obrigatorio.';
      } else if (field.type === 'upload' && (!Array.isArray(value) || value.length === 0)) {
        errors[field.key] = 'Campo obrigatorio.';
      } else if (value === undefined || value === '') {
        errors[field.key] = 'Campo obrigatorio.';
      }
    }
  }

  const validations = schema.validations ?? [];
  for (const rule of validations) {
    const value = data[rule.field];
    if (rule.type === 'required_true' && !value) {
      errors[rule.field] = rule.message;
    }
    if (rule.type === 'required_if') {
      const dependsOn = (rule as any).depends_on;
      const expected = (rule as any).value;
      if (data[dependsOn] === expected && (!value || value === '')) {
        errors[rule.field] = rule.message;
      }
    }
    if (rule.type === 'regex' && typeof value === 'string') {
      const pattern = (rule as any).pattern || (rule as any).value;
      if (pattern && !(new RegExp(pattern).test(value))) {
        errors[rule.field] = rule.message;
      }
    }
    if (rule.type === 'min' && typeof value === 'string') {
      const min = Number((rule as any).min);
      if (!Number.isNaN(min) && Number(value) < min) {
        errors[rule.field] = rule.message;
      }
    }
    if (rule.type === 'max' && typeof value === 'string') {
      const max = Number((rule as any).max);
      if (!Number.isNaN(max) && Number(value) > max) {
        errors[rule.field] = rule.message;
      }
    }
    if (rule.type === 'range' && typeof value === 'string') {
      const min = Number((rule as any).min);
      const max = Number((rule as any).max);
      const numeric = Number(value);
      if (!Number.isNaN(numeric) && ((Number.isFinite(min) && numeric < min) || (Number.isFinite(max) && numeric > max))) {
        errors[rule.field] = rule.message;
      }
    }
    if (rule.type === 'min_files') {
      const min = Number((rule as any).min);
      const files = Array.isArray(value) ? value.length : 0;
      if (!Number.isNaN(min) && files < min) {
        errors[rule.field] = rule.message;
      }
    }
  }

  const dependencies = schema.dependencies ?? [];
  for (const dep of dependencies) {
    if (data[dep.field] === dep.value) {
      for (const required of dep.requires) {
        const targetValue = data[required];
        if (!targetValue || (Array.isArray(targetValue) && targetValue.length === 0)) {
          errors[required] = dep.message || 'Campo obrigatorio.';
        }
      }
    }
  }

  return errors;
}
