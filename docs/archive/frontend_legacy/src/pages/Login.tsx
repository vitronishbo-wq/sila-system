import React, { useState } from 'react';
import { authService } from '../services/authService';
import { IMAGES, APP_VERSION } from '../constants';

interface LoginProps {
  onLoginSuccess: (token: string, redirectTo?: string) => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const { access_token, navigation } = await authService.login(formData);
      onLoginSuccess(access_token, navigation?.redirect_to);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao realizar login. Verifique as suas credenciais.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="sila-shell min-h-screen flex">
      <div className="hidden lg:flex lg:w-5/12 relative overflow-hidden border-r border-slate-200/80">
        <img
          src={IMAGES.GEO_LEVELS.PROVINCIAL}
          alt="Background institucional"
          className="absolute inset-0 w-full h-full object-cover object-[60%_50%] sm:object-[64%_50%] md:object-[67%_49%] lg:object-[70%_48%] xl:object-[72%_48%] scale-110 blur-[1.8px] brightness-[0.68] saturate-[0.68]"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-slate-950/94 via-slate-900/84 to-slate-800/80" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_15%_20%,rgba(250,204,21,0.12),transparent_38%)]" />
        <div className="absolute inset-0 bg-gradient-to-r from-slate-950/35 via-transparent to-slate-900/30" />
        <div className="relative z-10 w-full p-12 flex flex-col justify-between text-slate-100">
          <div className="space-y-8">
            <div className="inline-flex items-center gap-4 rounded-2xl border border-amber-300/40 bg-white/10 px-4 py-3 backdrop-blur-md">
              <img src={IMAGES.BRAND.INSIGNIA_ALT} alt="Brasão" className="w-10 h-10 object-contain" />
              <div>
                <p className="text-[10px] tracking-[0.26em] uppercase text-slate-200">República de Angola</p>
                <p className="text-sm font-semibold">Portal Institucional SILA</p>
              </div>
            </div>
            <h2 className="sila-display text-5xl leading-tight">
              Acesso Administrativo Seguro.
            </h2>
            <p className="text-slate-200/90 text-lg leading-relaxed max-w-md">
              Plataforma oficial para coordenação nacional, provincial e municipal de serviços públicos digitais.
            </p>
          </div>
          <div className="inline-flex items-center gap-4">
            <img src={IMAGES.BRAND.LOGO} alt="SILA Logotipo" className="h-8 opacity-85" />
            <p className="text-xs tracking-[0.18em] uppercase text-amber-200">Infraestrutura Digital de Estado</p>
          </div>
        </div>
      </div>

      <div className="w-full lg:w-7/12 flex items-center justify-center p-6 md:p-10">
        <div className="w-full max-w-xl sila-card rounded-3xl p-8 md:p-11">
          <div className="mb-8">
            <div className="flex items-center gap-4 mb-5">
              <img src={IMAGES.BRAND.INSIGNIA} alt="Insígnia SILA" className="h-9 w-9 object-contain" />
              <div>
                <p className="text-[11px] uppercase tracking-[0.18em] text-slate-500">Acesso à Plataforma</p>
                <p className="text-slate-800 font-semibold">SILA System • Administração</p>
              </div>
            </div>
            <h1 className="sila-display text-4xl text-slate-900 mb-2">Bem-vindo</h1>
            <p className="text-slate-600">Introduza as suas credenciais para aceder ao ecossistema institucional SILA.</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-5">
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-xl flex items-center gap-3 text-sm font-medium">
                <i className="fa-solid fa-circle-exclamation"></i>
                {error}
              </div>
            )}

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Email ou Nome de Utilizador</label>
              <div className="relative">
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl pl-12 sila-input"
                  placeholder="ex: central@sila.gov.ao"
                  required
                />
                <i className="fa-solid fa-user absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <label className="text-sm font-semibold text-slate-700">Palavra-passe</label>
                <a href="#" className="text-xs font-semibold text-slate-500 hover:text-slate-900">Esqueceu-se?</a>
              </div>
              <div className="relative">
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl pl-12 sila-input"
                  placeholder="••••••••"
                  required
                />
                <i className="fa-solid fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 rounded-xl font-semibold text-base transition-all active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 sila-btn-primary"
            >
              {isLoading ? (
                <i className="fa-solid fa-circle-notch fa-spin"></i>
              ) : (
                <>
                  <span>Entrar no Sistema</span>
                  <i className="fa-solid fa-arrow-right"></i>
                </>
              )}
            </button>
          </form>

          <div className="mt-8 text-center text-slate-500 text-xs">
            <p>Aceder como Cidadão? <a href="#/register" className="text-slate-900 font-semibold hover:underline">Crie uma conta aqui.</a></p>
            <div className="mt-6 flex justify-center gap-4 items-center">
              <img src={IMAGES.BRAND.INSIGNIA_ALT} alt="MAT" className="h-5 opacity-60" />
              <p className="border-l border-slate-300 pl-3">v{APP_VERSION}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
