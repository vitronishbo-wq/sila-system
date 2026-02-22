import React, { useState, useEffect } from 'react';
import { citizenAuthService } from '../services/citizenAuthService';

interface CitizenProfile {
  id: string;
  full_name: string;
  birth_date: string;
  gender: string;
  vital_status: string;
  id_number?: string;
  nif?: string;
}

interface CitizenPortalProps {
  onLogout: () => void;
}

const CitizenPortal: React.FC<CitizenPortalProps> = ({ onLogout }) => {
  const [profile, setProfile] = useState<CitizenProfile | null>(null);
  const [events, setEvents] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'profile' | 'events'>('profile');

  useEffect(() => {
    loadCitizenData();
  }, []);

  const loadCitizenData = async () => {
    setIsLoading(true);
    try {
      const [profileData, eventsData] = await Promise.all([
        citizenAuthService.getProfile(),
        citizenAuthService.getEvents()
      ]);
      setProfile(profileData);
      setEvents(eventsData);
    } catch (err) {
      console.error('Failed to load citizen data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-slate-900 mb-4"></div>
          <p className="text-gray-600">A carregar o seu perfil...</p>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow text-center">
          <p className="text-red-600 mb-4">Erro ao carregar o perfil</p>
          <button onClick={onLogout} className="px-4 py-2 bg-red-600 text-white rounded">
            Voltar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-slate-900">Minha FUC</h1>
          <button
            onClick={onLogout}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-semibold"
            title="Terminar sessão"
          >
            Sair
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Navegação de abas */}
        <div className="flex border-b mb-8 bg-white rounded-t-lg">
          <button
            onClick={() => setActiveTab('profile')}
            className={`px-6 py-3 font-medium transition-all ${
              activeTab === 'profile'
                ? 'text-slate-900 border-b-2 border-slate-900 bg-slate-50'
                : 'text-gray-600 hover:text-cursor-pointer hover:text-gray-900'
            }`}
            title="Ver informações pessoais"
          >
            👤 Perfil
          </button>
          <button
            onClick={() => setActiveTab('events')}
            className={`px-6 py-3 font-medium transition-all ${
              activeTab === 'events'
                ? 'text-slate-900 border-b-2 border-slate-900 bg-slate-50'
                : 'text-gray-600 hover:text-cursor-pointer hover:text-gray-900'
            }`}
            title="Ver eventos e atividades"
          >
            📋 Eventos
          </button>
        </div>

        {/* Conteúdo */}
        {activeTab === 'profile' && (
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold mb-6">Dados Pessoais</h2>
            <div className="grid grid-cols-2 gap-8">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Nome Completo</label>
                <p className="text-lg">{profile.full_name || 'Não informado'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Data de Nascimento</label>
                <p className="text-lg">
                  {profile.birth_date ? new Date(profile.birth_date).toLocaleDateString('pt-PT') : 'Não informado'}
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Género</label>
                <p className="text-lg">
                  {profile.gender ? (profile.gender === 'M' ? 'Masculino' : 'Feminino') : 'Não informado'}
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Estado Civil</label>
                <p className="text-lg">
                  {profile.vital_status ? (profile.vital_status === 'ALIVE' ? 'Vivo' : 'Falecido') : 'Não informado'}
                </p>
              </div>
              {profile.id_number && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Número BI</label>
                  <p className="text-lg">{profile.id_number}</p>
                </div>
              )}
              {profile.nif && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">NIF</label>
                  <p className="text-lg">{profile.nif}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'events' && (
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold mb-6">Histórico de Eventos</h2>
            {events.length === 0 ? (
              <p className="text-gray-500">Nenhum evento registado</p>
            ) : (
              <div className="space-y-4">
                {events.map((event: any) => (
                  <div key={event.id} className="border-l-4 border-slate-900 pl-4 py-2">
                    <p className="font-semibold">{event.event_type}</p>
                    <p className="text-sm text-gray-600">{new Date(event.created_at).toLocaleDateString('pt-PT')}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default CitizenPortal;
