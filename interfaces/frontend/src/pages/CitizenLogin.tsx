import React, { useState } from 'react';
import { citizenAuthService } from '../services/citizenAuthService';
import { IMAGES } from '../constants';

interface CitizenLoginProps {
  onLoginSuccess: (token: string) => void;
  onBackClick: () => void;
}

const CitizenLogin: React.FC<CitizenLoginProps> = ({ onLoginSuccess, onBackClick }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const token = await citizenAuthService.login(email, password);
      localStorage.setItem('citizen_token', token);
      localStorage.setItem('citizen_email', email);
      onLoginSuccess(token);
    } catch (err) {
      setError('Email ou senha inválida');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="sila-shell min-h-screen flex items-center justify-center p-6 md:p-10">
      <div className="max-w-5xl w-full grid lg:grid-cols-2 gap-8 items-stretch">
        <section className="relative rounded-[2rem] overflow-hidden min-h-[430px]">
          <img
            src={IMAGES.GEO_LEVELS.MUNICIPAL}
            alt="Cidadania Digital"
            className="absolute inset-0 w-full h-full object-cover object-[53%_49%] sm:object-[56%_48%] md:object-[60%_47%] lg:object-[63%_46%] xl:object-[65%_45%] scale-110 blur-[1.8px] brightness-[0.7] saturate-[0.7]"
          />
          <div className="absolute inset-0 bg-gradient-to-br from-[#0f172a]/94 via-[#172554]/80 to-[#c99a2e]/44" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_18%_18%,rgba(250,204,21,0.12),transparent_36%)]" />
          <div className="absolute inset-0 bg-gradient-to-r from-[#020817]/26 via-transparent to-[#020817]/26" />
          <div className="relative z-10 p-8 md:p-10 h-full flex flex-col justify-between text-white">
            <div className="inline-flex items-center gap-3 rounded-2xl bg-white/12 backdrop-blur-md border border-white/20 px-4 py-3 w-fit">
              <img src={IMAGES.BRAND.INSIGNIA_ALT} alt="Insígnia" className="w-8 h-8 object-contain" />
              <div>
                <p className="text-[10px] uppercase tracking-[0.22em] text-white/80">Governo Digital</p>
                <p className="font-semibold text-sm">Ficha Única do Cidadão</p>
              </div>
            </div>
            <div>
              <h1 className="sila-display text-4xl leading-tight mb-4">Aceda à sua identidade digital.</h1>
              <p className="text-white/90 leading-relaxed">
                Entre no seu espaço pessoal para consultar documentos, notificações e serviços essenciais de forma segura.
              </p>
            </div>
          </div>
        </section>

        <section className="sila-card rounded-[2rem] p-8 md:p-10">
          <div className="mb-8">
            <p className="text-[11px] uppercase tracking-[0.18em] text-slate-500 mb-2">Portal do Cidadão</p>
            <h2 className="sila-display text-4xl text-slate-900 mb-2">Entrar</h2>
            <p className="text-slate-600">Autentique-se com o seu email para continuar.</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seu.email@example.com"
                className="w-full px-4 py-3 rounded-xl sila-input"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Senha</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 rounded-xl sila-input"
                required
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm font-medium">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full px-4 py-3 rounded-xl font-semibold transition-all disabled:opacity-50 sila-btn-primary"
            >
              {isLoading ? 'A conectar...' : 'Entrar'}
            </button>
          </form>

          <button
            onClick={onBackClick}
            className="w-full mt-4 px-4 py-3 rounded-xl font-semibold transition-colors sila-btn-secondary"
          >
            Voltar
          </button>
        </section>
      </div>
    </div>
  );
};

export default CitizenLogin;
