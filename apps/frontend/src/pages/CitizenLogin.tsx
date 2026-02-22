import React, { useState } from 'react';
import { citizenAuthService } from '../services/citizenAuthService';

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
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">FUC - Cidadão</h1>
        <p className="text-gray-600 mb-6">Aceda à sua Ficha Única do Cidadão</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="seu.email@example.com"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-slate-900 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Senha</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-slate-900 focus:border-transparent"
              required
            />
          </div>

          {error && (
            <div className="bg-red-100 text-red-700 px-4 py-2 rounded-lg text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full px-4 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 disabled:opacity-50"
          >
            {isLoading ? 'A conectar...' : 'Entrar'}
          </button>
        </form>

        <button
          onClick={onBackClick}
          className="w-full mt-4 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
        >
          Voltar
        </button>
      </div>
    </div>
  );
};

export default CitizenLogin;
