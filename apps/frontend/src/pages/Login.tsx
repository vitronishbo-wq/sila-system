import React, { useState } from 'react';
import { authService } from '@/services/authService';
import { ASSETS, APP_VERSION } from '@/constants';

interface LoginProps {
  onLoginSuccess?: (token: string) => void;
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

      const { access_token } = await authService.login(formData);
      if (onLoginSuccess) {
        onLoginSuccess(access_token);
      } else {
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('token', access_token);
        window.location.hash = '/admin';
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao realizar login. Verifique as suas credenciais.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex font-inter">
      {/* Left Side: Subtle Visual */}
      <div className="hidden lg:flex lg:w-1/3 relative overflow-hidden">
        <img
          src={ASSETS.BANDEIRA}
          alt="Background"
          className="absolute inset-0 w-full h-full object-cover opacity-20 filter blur-sm"
        />
        <div className="relative z-10 w-full p-12 flex flex-col justify-end text-slate-800">
          <div className="mb-8">
            <img src={ASSETS.BRASAO} alt="Brasão" className="w-16 mb-4 opacity-90" />
            <h2 className="text-2xl font-semibold tracking-tight mb-2">SILA-System</h2>
            <p className="text-sm opacity-80 max-w-xs">Sistema Integrado de Administração Local para uma governação moderna e eficiente.</p>
          </div>
          <div className="flex gap-3 items-center">
            <div className="w-10 h-0.5 bg-yellow-500"></div>
            <p className="text-xs font-medium tracking-widest uppercase text-yellow-500">República de Angola</p>
          </div>
        </div>
      </div>

      {/* Right Side: Login Form */}
      <div className="w-full lg:w-2/3 flex items-center justify-center p-8 bg-gray-50">
        <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-10">
          <div className="mb-6 text-center lg:text-left">
            <h1 className="text-2xl font-bold text-slate-900 mb-1">Bem-vindo</h1>
            <p className="text-xs uppercase tracking-[0.2em] text-slate-500 font-semibold">Painel Administrativo</p>
            <p className="text-gray-500 text-sm mt-2">Introduza as suas credenciais para administrar os serviços do SILA.</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-5">
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 text-red-600 rounded-lg flex items-center gap-3 text-sm font-medium">
                <i className="fa-solid fa-circle-exclamation"></i>
                {error}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Email ou Nome de Utilizador</label>
              <div className="relative">
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full px-4 py-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-slate-100 focus:border-slate-900 outline-none transition-all pl-12"
                  placeholder="ex: central@sila.gov.ao"
                  required
                />
                <i className="fa-solid fa-user absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <label className="text-sm font-medium text-slate-700">Palavra-passe</label>
                <a href="#" className="text-xs font-medium text-slate-500 hover:text-slate-900">Esqueceu-se?</a>
              </div>
              <div className="relative">
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-slate-100 focus:border-slate-900 outline-none transition-all pl-12"
                  placeholder="••••••••"
                  required
                />
                <i className="fa-solid fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 bg-slate-900 text-white rounded-lg font-semibold text-base hover:bg-slate-800 transition-all shadow-md active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
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

          <div className="mt-8 text-center text-gray-400 text-xs">
            <p>Aceder como Cidadão? <a href="#/citizen/login" className="text-slate-900 font-medium hover:underline">Entrar na FUC.</a></p>
            <div className="mt-6 flex justify-center gap-4 items-center">
              <img src={ASSETS.BRASAO} alt="MAT" className="h-5 opacity-50 grayscale" />
              <p className="border-l pl-3">v{APP_VERSION}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
