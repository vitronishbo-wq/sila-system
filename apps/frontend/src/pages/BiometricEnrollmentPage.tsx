import React, { useEffect, useState } from 'react';
import CitizenAreaBanner from '@/components/Services/CitizenAreaBanner';
import { BiometricEnrollment } from '@/modules/identity/components';
import type { BiometricTemplate } from '@/modules/identity/types';
import { citizenAuthService } from '@/services/citizenAuthService';

const BiometricEnrollmentPage: React.FC = () => {
  const [citizenId, setCitizenId] = useState<string | null>(null);
  const [profileLoading, setProfileLoading] = useState(true);
  const [profileError, setProfileError] = useState<string | null>(null);
  const [lastTemplate, setLastTemplate] = useState<BiometricTemplate | null>(null);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        setProfileLoading(true);
        const profile = await citizenAuthService.getProfile();
        setCitizenId(profile.id);
        setProfileError(null);
      } catch (err) {
        console.error('Erro ao carregar perfil do cidadão:', err);
        setProfileError('Não foi possível carregar o perfil do cidadão.');
      } finally {
        setProfileLoading(false);
      }
    };

    loadProfile();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Inscrição Biométrica</h1>
          <p className="text-slate-600">Registre seus dados biométricos de forma segura para autenticação.</p>
        </div>
      </div>

      <CitizenAreaBanner />

      <div className="max-w-4xl mx-auto px-6 py-12">
        {profileLoading && (
          <div className="rounded-xl border border-slate-200 bg-white p-6 text-sm text-slate-600 shadow-sm">
            A carregar o seu perfil...
          </div>
        )}

        {!profileLoading && profileError && (
          <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-sm text-red-700">
            {profileError}
          </div>
        )}

        {!profileLoading && !profileError && citizenId && (
          <div className="space-y-4">
            {lastTemplate && (
              <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800">
                Biometria registrada com sucesso: {lastTemplate.biometric_type}.
              </div>
            )}
            <BiometricEnrollment
              citizenId={citizenId}
              onSuccess={(template) => setLastTemplate(template)}
              onCancel={() => setLastTemplate(null)}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default BiometricEnrollmentPage;
