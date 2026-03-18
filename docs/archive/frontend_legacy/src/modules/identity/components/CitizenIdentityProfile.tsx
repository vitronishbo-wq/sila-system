/**
 * Citizen Identity Profile Component
 * Unified view of citizen information, digital BI, and biometric status
 * 360° aggregation of all identity data
 */

import React, { useState } from 'react';
import {
  useCitizen,
  useDigitalBI,
  useBiometricTemplates,
  useVerificationResults,
} from '../hooks';
import {
  isDigitalBIValid,
  getDaysUntilExpiry,
  isBIExpiringSoon,
  formatAuditEvent,
} from '../utils';
import {
  CitizenProfile,
  DigitalBIDocument,
  BiometricTemplate,
  VerificationResult,
} from '../types';

interface CitizenIdentityProfileProps {
  citizenId: string;
}

/**
 * CitizenIdentityProfile - Main identity aggregation component
 * Orchestrates: useCitizen, useDigitalBI, useBiometricTemplates, useVerificationResults
 */
export const CitizenIdentityProfile: React.FC<CitizenIdentityProfileProps> = ({
  citizenId,
}) => {
  const { citizen, loading: citizenLoading, error: citizenError } = useCitizen(citizenId);
  const { documents, loading: docsLoading, error: docsError } = useDigitalBI(citizenId);
  const { templates, loading: biometricLoading, error: biometricError } =
    useBiometricTemplates(citizenId);
  const { results, loadingResults, error: verificationError } =
    useVerificationResults(citizenId);

  const [selectedBI, setSelectedBI] = useState<DigitalBIDocument | null>(null);
  const [activeTab, setActiveTab] = useState<
    'personal' | 'digital-bi' | 'biometric' | 'verification'
  >('personal');

  // Consolidated loading and error states
  const isLoading =
    citizenLoading || docsLoading || biometricLoading || loadingResults;
  const errors = [citizenError, docsError, biometricError, verificationError].filter(
    Boolean
  );

  if (isLoading) {
    return (
      <div className="space-y-4 p-6">
        <div className="h-32 bg-gradient-to-r from-gray-200 to-gray-100 rounded-lg animate-pulse" />
        <div className="grid grid-cols-3 gap-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-48 bg-gray-100 rounded-lg animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  if (errors.length > 0) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="font-bold text-red-800 mb-2">Erro ao carregar perfil</h3>
        <ul className="list-disc list-inside text-red-700 text-sm space-y-1">
          {errors.map((err, i) => (
            <li key={i}>{err}</li>
          ))}
        </ul>
      </div>
    );
  }

  if (!citizen) {
    return (
      <div className="p-6 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-800">
        Cidadão não encontrado.
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {/* Header with citizen basic info */}
      <CitizenHeader citizen={citizen} verificationLevel={results[0]?.verification_level} />

      {/* Tabs navigation */}
      <div className="flex space-x-1 border-b border-gray-200">
        {(['personal', 'digital-bi', 'biometric', 'verification'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors ${
              activeTab === tab
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-800'
            }`}
          >
            {tabLabel(tab)}
            {tab === 'digital-bi' && documents.length > 0 && (
              <span className="ml-2 bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full">
                {documents.length}
              </span>
            )}
            {tab === 'biometric' && templates.length > 0 && (
              <span className="ml-2 bg-green-100 text-green-800 text-xs px-2 py-0.5 rounded-full">
                {templates.length}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div>
        {activeTab === 'personal' && (
          <PersonalInfoTab citizen={citizen} />
        )}
        {activeTab === 'digital-bi' && (
          <DigitalBITab
            documents={documents}
            selectedBI={selectedBI}
            onSelectBI={setSelectedBI}
          />
        )}
        {activeTab === 'biometric' && (
          <BiometricTab templates={templates} />
        )}
        {activeTab === 'verification' && (
          <VerificationTab results={results} />
        )}
      </div>
    </div>
  );
};

// ============= SUB-COMPONENTS =============

/**
 * Header with citizen name and verification status badge
 */
function CitizenHeader({
  citizen,
  verificationLevel,
}: {
  citizen: CitizenProfile;
  verificationLevel?: string;
}) {
  const statusColor = {
    ACTIVE: 'bg-green-100 text-green-800',
    INACTIVE: 'bg-gray-100 text-gray-800',
    SUSPENDED: 'bg-yellow-100 text-yellow-800',
    DECEASED: 'bg-red-100 text-red-800',
  }[citizen.status] || 'bg-gray-100 text-gray-800';

  const verificationColor = {
    basic: 'bg-blue-100 text-blue-800',
    enhanced: 'bg-purple-100 text-purple-800',
    biometric: 'bg-green-100 text-green-800',
  }[citizen.verification_level] || 'bg-gray-100 text-gray-800';

  return (
    <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{citizen.full_name}</h1>
          <p className="text-gray-600 mt-1">
            {citizen.national_id_number} • {citizen.email}
          </p>
        </div>
        <div className="flex gap-2">
          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColor}`}>
            {citizen.status}
          </span>
          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${verificationColor}`}>
            {verificationLevel || citizen.verification_level.toUpperCase()}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
        <div>
          <p className="text-gray-500">Data de Nascimento</p>
          <p className="font-medium">{formatDate(citizen.birth_date)}</p>
        </div>
        <div>
          <p className="text-gray-500">Género</p>
          <p className="font-medium">{citizen.gender === 'M' ? 'Masculino' : 'Feminino'}</p>
        </div>
        <div>
          <p className="text-gray-500">NIF</p>
          <p className="font-medium">{citizen.nif}</p>
        </div>
        <div>
          <p className="text-gray-500">Localidade</p>
          <p className="font-medium">
            {citizen.municipality}, {citizen.province}
          </p>
        </div>
      </div>
    </div>
  );
}

/**
 * Personal information tab
 */
function PersonalInfoTab({ citizen }: { citizen: CitizenProfile }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="font-bold text-lg mb-4 border-b pb-3">Dados Pessoais</h3>
        <InfoField label="Nome Completo" value={citizen.full_name} />
        <InfoField label="Nº de Bilhete de Identidade" value={citizen.national_id_number} />
        <InfoField label="NIF" value={citizen.nif} />
        <InfoField label="Passaporte" value={citizen.passport_number || 'Não informado'} />
        <InfoField label="Data de Nascimento" value={formatDate(citizen.birth_date)} />
        <InfoField label="Género" value={citizen.gender === 'M' ? 'Masculino' : 'Feminino'} />
        <InfoField label="Estado Civil" value={citizen.marital_status} />
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="font-bold text-lg mb-4 border-b pb-3">Localização e Contacto</h3>
        <InfoField label="Província" value={citizen.province} />
        <InfoField label="Município" value={citizen.municipality} />
        <InfoField label="Telefone" value={citizen.phone} />
        <InfoField label="Email" value={citizen.email} />
        <InfoField label="Rua" value={citizen.street || 'Não informado'} />
        <InfoField label="Bairro" value={citizen.neighborhood || 'Não informado'} />
      </div>

      <div className="bg-white rounded-lg shadow p-6 md:col-span-2">
        <h3 className="font-bold text-lg mb-4 border-b pb-3">Auditoria</h3>
        <div className="grid grid-cols-2 gap-4">
          <InfoField label="Criado em" value={formatDateTime(citizen.created_at)} />
          <InfoField label="Atualizado em" value={formatDateTime(citizen.updated_at)} />
        </div>
      </div>
    </div>
  );
}

/**
 * Digital BI tab
 */
function DigitalBITab({
  documents,
  selectedBI,
  onSelectBI,
}: {
  documents: DigitalBIDocument[];
  selectedBI: DigitalBIDocument | null;
  onSelectBI: (doc: DigitalBIDocument | null) => void;
}) {
  if (documents.length === 0) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-8 text-center text-yellow-700">
        <p className="font-medium">Nenhum documento BI digital emitido</p>
        <p className="text-sm mt-1">Inicie um pedido de emissão para começar</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* List */}
      <div className="space-y-3">
        {documents.map((doc) => (
          <BIDocumentCard
            key={doc.id}
            document={doc}
            isSelected={selectedBI?.id === doc.id}
            onClick={() => onSelectBI(doc)}
          />
        ))}
      </div>

      {/* Detail */}
      {selectedBI && (
        <div className="md:col-span-2">
          <BIDocumentDetail document={selectedBI} />
        </div>
      )}
    </div>
  );
}

/**
 * BI Document card
 */
function BIDocumentCard({
  document,
  isSelected,
  onClick,
}: {
  document: DigitalBIDocument;
  isSelected: boolean;
  onClick: () => void;
}) {
  const { isValid } = isDigitalBIValid(document);
  const daysUntilExpiry = getDaysUntilExpiry(document.expiry_date);
  const expiringSoon = isBIExpiringSoon(document.expiry_date);

  const statusIcon = {
    PENDING: '⏳',
    ISSUED: '✅',
    REVOKED: '🚫',
    EXPIRED: '⛔',
  }[document.status] || '❓';

  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
        isSelected
          ? 'border-blue-500 bg-blue-50'
          : 'border-gray-200 bg-white hover:border-gray-300'
      }`}
    >
      <div className="flex items-start justify-between mb-2">
        <h4 className="font-bold text-gray-900">{document.document_type}</h4>
        <span className="text-xl">{statusIcon}</span>
      </div>
      <p className="text-sm text-gray-600">{document.document_number}</p>
      <p className="text-xs text-gray-500 mt-2">
        Válido até: {formatDate(document.expiry_date)}
      </p>
      {expiringSoon && daysUntilExpiry > 0 && (
        <p className="text-xs text-orange-600 font-medium mt-1">
          ⚠️ Expira em {daysUntilExpiry} dias
        </p>
      )}
    </button>
  );
}

/**
 * BI Document detail view
 */
function BIDocumentDetail({ document }: { document: DigitalBIDocument }) {
  const { isValid } = isDigitalBIValid(document);

  return (
    <div className="bg-white rounded-lg shadow p-6 space-y-6">
      <div>
        <h3 className="font-bold text-lg mb-4 border-b pb-3">
          Detalhes do Documento {document.document_type}
        </h3>

        <div className="grid grid-cols-2 gap-4">
          <InfoField label="Nº de Documento" value={document.document_number} />
          <InfoField label="Estado" value={document.status} />
          <InfoField label="Data de Emissão" value={formatDate(document.issue_date)} />
          <InfoField label="Data de Expiração" value={formatDate(document.expiry_date)} />
        </div>
      </div>

      {document.mrz_data && (
        <div className="bg-gray-50 p-4 rounded border border-gray-200">
          <p className="text-xs font-mono text-gray-600 break-all">{document.mrz_data}</p>
        </div>
      )}

      <div className="flex gap-2">
        {isValid && (
          <button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm font-medium">
            Descarregar
          </button>
        )}
        <button className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 text-sm font-medium">
          Ver QR Code
        </button>
      </div>
    </div>
  );
}

/**
 * Biometric tab
 */
function BiometricTab({ templates }: { templates: BiometricTemplate[] }) {
  if (templates.length === 0) {
    return (
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-8 text-center text-blue-700">
        <p className="font-medium">Nenhum template biométrico capturado</p>
        <p className="text-sm mt-1">Inicie uma inscrição biométrica para adicionar dados</p>
      </div>
    );
  }

  const biometricsByType = templates.reduce(
    (acc, template) => {
      if (!acc[template.biometric_type]) {
        acc[template.biometric_type] = [];
      }
      acc[template.biometric_type].push(template);
      return acc;
    },
    {} as Record<string, BiometricTemplate[]>
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {Object.entries(biometricsByType).map(([type, typeTemplates]) => (
        <BiometricTypeCard
          key={type}
          biometricType={type}
          templates={typeTemplates}
        />
      ))}
    </div>
  );
}

/**
 * Biometric type card
 */
function BiometricTypeCard({
  biometricType,
  templates,
}: {
  biometricType: string;
  templates: BiometricTemplate[];
}) {
  const icon = {
    FINGERPRINT: '👆',
    FACE_RECOGNITION: '😊',
    IRIS: '👁️',
    VOICE: '🎤',
  }[biometricType] || '📱';

  const avgQuality =
    templates.reduce((sum, t) => sum + t.quality_score, 0) / templates.length;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h4 className="font-bold text-lg">
          <span className="mr-2">{icon}</span>
          {formatBiometricType(biometricType)}
        </h4>
        <span className="text-xs font-semibold bg-green-100 text-green-800 px-2 py-1 rounded">
          {templates.length} template{templates.length !== 1 ? 's' : ''}
        </span>
      </div>

      <div className="space-y-3">
        {templates.map((template, idx) => (
          <div
            key={template.id}
            className="flex justify-between items-center p-3 bg-gray-50 rounded border border-gray-200"
          >
            <div className="flex-1">
              <p className="text-sm text-gray-600">Template {idx + 1}</p>
              <p className="text-xs text-gray-500 mt-1">
                Capturado em {formatDateTime(template.capture_date)}
              </p>
            </div>
            <div className="text-right">
              <div className="text-lg font-bold text-blue-600">
                {template.quality_score}%
              </div>
              <p className="text-xs text-gray-500">Qualidade</p>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t">
        <p className="text-sm text-gray-600">
          Qualidade Média:{' '}
          <span className="font-bold text-blue-600">{Math.round(avgQuality)}%</span>
        </p>
      </div>
    </div>
  );
}

/**
 * Verification tab
 */
function VerificationTab({ results }: { results: VerificationResult[] }) {
  if (results.length === 0) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center text-gray-700">
        <p className="font-medium">Nenhuma verificação realizada</p>
        <p className="text-sm mt-1">Inicie um processo de verificação para ver histórico</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {results.map((result) => (
        <VerificationResultCard key={result.verification_id} result={result} />
      ))}
    </div>
  );
}

/**
 * Verification result card
 */
function VerificationResultCard({ result }: { result: VerificationResult }) {
  const levelColor = {
    BASIC: 'bg-blue-100 text-blue-800',
    ENHANCED: 'bg-purple-100 text-purple-800',
    BIOMETRIC: 'bg-green-100 text-green-800',
  }[result.verification_level] || 'bg-gray-100 text-gray-800';

  const confidenceColor =
    result.confidence_score >= 90
      ? 'text-green-600'
      : result.confidence_score >= 70
        ? 'text-yellow-600'
        : 'text-red-600';

  return (
    <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h4 className="font-bold text-lg">{result.verification_type}</h4>
          <p className="text-sm text-gray-600">ID: {result.verification_id}</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${levelColor}`}>
          {result.verification_level}
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <InfoField label="Data" value={formatDateTime(result.verified_at)} />
        <InfoField label="Verificado por" value={result.verified_by} />
        <InfoField label="Validade" value={result.expiry_date ? formatDate(result.expiry_date) : 'Sem limite'} />
        <div>
          <p className="text-gray-500 text-sm">Confiança</p>
          <p className={`font-bold text-lg ${confidenceColor}`}>
            {result.confidence_score}%
          </p>
        </div>
      </div>

      {result.audit_trail && result.audit_trail.length > 0 && (
        <div className="mt-4 pt-4 border-t">
          <p className="text-sm font-medium text-gray-700 mb-2">Trilha de Auditoria</p>
          <div className="space-y-1 text-xs text-gray-600 max-h-32 overflow-y-auto">
            {result.audit_trail.map((event, idx) => (
              <p key={idx}>{formatAuditEvent(event)}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ============= UTILITY FUNCTIONS =============

function tabLabel(tab: string): string {
  const labels = {
    personal: 'Dados Pessoais',
    'digital-bi': 'Bilhete de Identidade Digital',
    biometric: 'Biometria',
    verification: 'Verificação',
  };
  return labels[tab as keyof typeof labels] || tab;
}

function formatBiometricType(type: string): string {
  const types = {
    FINGERPRINT: 'Impressão Digital',
    FACE_RECOGNITION: 'Reconhecimento Facial',
    IRIS: 'Íris',
    VOICE: 'Voz',
  };
  return types[type as keyof typeof types] || type;
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('pt-MZ', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

function formatDateTime(dateString: string): string {
  return new Date(dateString).toLocaleString('pt-MZ', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

interface InfoFieldProps {
  label: string;
  value: string;
}

function InfoField({ label, value }: InfoFieldProps) {
  return (
    <div className="mb-3">
      <p className="text-sm text-gray-500 font-medium">{label}</p>
      <p className="text-gray-900 font-medium">{value}</p>
    </div>
  );
}
