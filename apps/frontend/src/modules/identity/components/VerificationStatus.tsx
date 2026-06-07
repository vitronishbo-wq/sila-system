/**
 * Verification Status Component
 * Real-time tracking of citizen verification workflows
 */

import React, { useState } from 'react';
import {
  useVerificationResults,
} from '@/modules/identity/hooks';
import type { VerificationResult, VerificationRequest } from '@/modules/identity/types';
import { identityService } from '@/modules/identity/services';

interface VerificationStatusProps {
  citizenId: string;
  verificationRequestId?: string;
}

/**
 * VerificationStatus - Workflow tracking and completion display
 */
export const VerificationStatus: React.FC<VerificationStatusProps> = ({
  citizenId,
  verificationRequestId,
}) => {
  const { results, loadingResults, error, refetch } = useVerificationResults(citizenId);
  const [selectedResult, setSelectedResult] = useState<VerificationResult | null>(null);
  const [statusCheckLoading, setStatusCheckLoading] = useState(false);
  const [requestStatus, setRequestStatus] = useState<VerificationRequest | null>(null);

  const handleCheckStatus = async (requestId: string) => {
    setStatusCheckLoading(true);
    try {
      const status = await identityService.getVerificationStatus(requestId);
      setRequestStatus(status);
    } catch (err) {
      console.error('Failed to check status:', err);
    } finally {
      setStatusCheckLoading(false);
    }
  };

  if (loadingResults) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="font-bold text-red-800 mb-2">Erro ao carregar verificações</h3>
        <p className="text-red-700 mb-4">{error.message}</p>
        <button
          onClick={() => refetch()}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 text-sm font-medium"
        >
          Tentar Novamente
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Pending verification check */}
      {verificationRequestId && !requestStatus && (
        <div className="bg-blue-50 border-l-4 border-blue-500 rounded-lg p-6">
          <h3 className="font-bold text-blue-900 mb-3">Verificação em Progresso</h3>
          <p className="text-blue-800 text-sm mb-4">
            Tem um pedido de verificação pendente. Clique para verificar o estado.
          </p>
          <button
            onClick={() => handleCheckStatus(verificationRequestId)}
            disabled={statusCheckLoading}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm font-medium disabled:opacity-50"
          >
            {statusCheckLoading ? 'Verificando...' : 'Verificar Estado'}
          </button>
        </div>
      )}

      {/* Request status details */}
      {requestStatus && (
        <RequestStatusPanel requestStatus={requestStatus} onClose={() => setRequestStatus(null)} />
      )}

      {/* Completed verifications */}
      {results.length > 0 ? (
        <div>
          <h3 className="text-xl font-bold mb-4">Histórico de Verificações</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {results.map((result) => (
              <VerificationResultCard
                key={result.verification_id}
                result={result}
                isSelected={selectedResult?.verification_id === result.verification_id}
                onClick={() => setSelectedResult(result)}
              />
            ))}
          </div>

          {/* Detailed view */}
          {selectedResult && (
            <VerificationDetailPanel
              result={selectedResult}
              onClose={() => setSelectedResult(null)}
            />
          )}
        </div>
      ) : (
        <EmptyState />
      )}
    </div>
  );
};

// ============= SUB-COMPONENTS =============

/**
 * Loading state skeleton
 */
function LoadingState() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="h-24 bg-gray-100 rounded-lg animate-pulse" />
      ))}
    </div>
  );
}

/**
 * Empty state
 */
function EmptyState() {
  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-12 text-center">
      <div className="text-4xl mb-4">📋</div>
      <h3 className="font-bold text-lg text-gray-900 mb-2">Nenhuma Verificação</h3>
      <p className="text-gray-600">
        Nenhuma verificação foi realizada ainda. Inicie um pedido para começar.
      </p>
    </div>
  );
}

/**
 * Verification result card for list view
 */
function VerificationResultCard({
  result,
  isSelected,
  onClick,
}: {
  result: VerificationResult;
  isSelected: boolean;
  onClick: () => void;
}) {
  const typeIcon = {
    DOCUMENT: '📄',
    BIOMETRIC: '👤',
    ADDRESS: '🏠',
    COMBINED: '📦',
  }[result.verification_type] || '✓';

  const levelColor = {
    BASIC: 'bg-blue-100 text-blue-800',
    ENHANCED: 'bg-purple-100 text-purple-800',
    BIOMETRIC: 'bg-green-100 text-green-800',
  }[result.verification_level] || 'bg-gray-100 text-gray-800';

  const resultStatus = result.is_verified ? '✅ Verificado' : '❌ Falhou';

  return (
    <button
      onClick={onClick}
      className={`text-left p-4 rounded-lg border-2 transition-all ${
        isSelected
          ? 'border-blue-500 bg-blue-50'
          : 'border-gray-200 bg-white hover:border-gray-300'
      }`}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{typeIcon}</span>
          <div>
            <h4 className="font-bold text-gray-900">{result.verification_type}</h4>
            <p className="text-xs text-gray-600">{result.verification_id}</p>
          </div>
        </div>
        <span className={`px-2 py-1 rounded text-xs font-semibold ${levelColor}`}>
          {result.verification_level}
        </span>
      </div>

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-600">Estado:</span>
          <span className="font-medium">{resultStatus}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Data:</span>
          <span className="font-medium">{formatDate(result.verified_at)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Confiança:</span>
          <span className={`font-bold ${getConfidenceColor(result.confidence_score)}`}>
            {result.confidence_score}%
          </span>
        </div>
      </div>
    </button>
  );
}

/**
 * Request status panel showing pending verification details
 */
function RequestStatusPanel({
  requestStatus,
  onClose,
}: {
  requestStatus: VerificationRequest;
  onClose: () => void;
}) {
  const statusProgressMap = {
    PENDING: { step: 1, label: 'Pendente', color: 'bg-yellow-100 text-yellow-800' },
    IN_PROGRESS: { step: 2, label: 'Em Progresso', color: 'bg-blue-100 text-blue-800' },
    COMPLETED: { step: 3, label: 'Concluído', color: 'bg-green-100 text-green-800' },
    FAILED: { step: 3, label: 'Falhou', color: 'bg-red-100 text-red-800' },
    REJECTED: { step: 3, label: 'Rejeitado', color: 'bg-red-100 text-red-800' },
  };

  const progress = statusProgressMap[requestStatus.status] ?? statusProgressMap.PENDING;

  return (
    <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-bold text-gray-900">Estado do Pedido</h3>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-gray-700 text-xl font-bold"
        >
          ✕
        </button>
      </div>

      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          {['Pendente', 'Em Progresso', 'Concluído'].map((step, idx) => (
            <div
              key={step}
              className={`flex items-center ${idx < 2 ? 'flex-1' : ''}`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm 
                ${
                  idx < progress.step
                    ? 'bg-green-500'
                    : idx === progress.step - 1
                      ? 'bg-blue-500'
                      : 'bg-gray-300'
                }`}
              >
                {idx < progress.step ? '✓' : idx + 1}
              </div>
              {idx < 2 && (
                <div
                  className={`flex-1 h-1 mx-2 ${
                    idx < progress.step - 1 ? 'bg-green-500' : 'bg-gray-300'
                  }`}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div>
          <p className="text-gray-600 text-sm font-medium">Tipo de Verificação</p>
          <p className="text-gray-900 font-semibold">{requestStatus.verification_type}</p>
        </div>
        <div>
          <p className="text-gray-600 text-sm font-medium">Estado Atual</p>
          <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${progress.color}`}>
            {progress.label}
          </span>
        </div>
        <div>
          <p className="text-gray-600 text-sm font-medium">Solicitado em</p>
          <p className="text-gray-900">{formatDateTime(requestStatus.requested_at)}</p>
        </div>
        {requestStatus.completed_at && (
          <div>
            <p className="text-gray-600 text-sm font-medium">Completado em</p>
            <p className="text-gray-900">{formatDateTime(requestStatus.completed_at)}</p>
          </div>
        )}
      </div>

      {requestStatus.rejection_reason && (
        <div className="bg-red-50 border border-red-200 rounded p-4 text-red-700 text-sm">
          <p className="font-medium mb-1">Motivo da Rejeição:</p>
          <p>{requestStatus.rejection_reason}</p>
        </div>
      )}

      {requestStatus.status === 'IN_PROGRESS' && (
        <div className="bg-blue-50 border border-blue-200 rounded p-4 text-blue-700 text-sm mt-4">
          <p className="font-medium">⏳ Sua verificação está sendo processada.</p>
          <p className="mt-1">Será notificado quando a revisão estiver concluída.</p>
        </div>
      )}
    </div>
  );
}

/**
 * Detailed verification result panel
 */
function VerificationDetailPanel({
  result,
  onClose,
}: {
  result: VerificationResult;
  onClose: () => void;
}) {
  return (
    <div className="mt-6 bg-white rounded-lg shadow p-6 border-t-4 border-blue-500">
      <div className="flex justify-between items-start mb-6">
        <h3 className="text-xl font-bold text-gray-900">Detalhes da Verificação</h3>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-gray-700 text-xl font-bold"
        >
          ✕
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <InfoField label="ID da Verificação" value={result.verification_id} />
        <InfoField label="Tipo" value={result.verification_type} />
        <InfoField label="Nível de Verificação" value={result.verification_level} />
        <InfoField label="Verificado por" value={result.verified_by} />
        <InfoField label="Data de Verificação" value={formatDateTime(result.verified_at)} />
        {result.expiry_date && (
          <InfoField label="Válido até" value={formatDate(result.expiry_date)} />
        )}
      </div>

      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 mb-6">
        <p className="text-gray-600 text-sm font-medium mb-2">Pontuação de Confiança</p>
        <div className="flex items-baseline gap-4">
          <div className="text-5xl font-bold text-blue-600">{result.confidence_score}%</div>
          <div className="flex-1">
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className={`h-3 rounded-full transition-all ${getConfidenceBarColor(
                  result.confidence_score
                )}`}
                style={{ width: `${result.confidence_score}%` }}
              />
            </div>
            <p className="text-xs text-gray-600 mt-2">
              {getConfidenceLevel(result.confidence_score)}
            </p>
          </div>
        </div>
      </div>

      {result.audit_trail && result.audit_trail.length > 0 && (
        <div>
          <h4 className="font-bold text-gray-900 mb-3">Trilha de Auditoria</h4>
          <div className="space-y-2">
            {result.audit_trail.map((event, idx) => (
              <AuditEventItem key={idx} event={event} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Audit event item
 */
function AuditEventItem({ event }: { event: any }) {
  const statusIcon = event.status === 'SUCCESS' ? '✓' : '✕';
  const statusColor =
    event.status === 'SUCCESS' ? 'text-green-600' : 'text-red-600';

  return (
    <div className="flex gap-4 p-3 bg-gray-50 rounded border border-gray-200">
      <span className={`text-lg font-bold ${statusColor}`}>{statusIcon}</span>
      <div className="flex-1 min-w-0">
        <p className="font-medium text-gray-900">{event.action}</p>
        <p className="text-xs text-gray-600">
          {event.event_type} • {formatDateTime(event.timestamp)}
        </p>
      </div>
    </div>
  );
}

// ============= UTILITY FUNCTIONS =============

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

function getConfidenceColor(score: number): string {
  return score >= 90 ? 'text-green-600' : score >= 70 ? 'text-yellow-600' : 'text-red-600';
}

function getConfidenceBarColor(score: number): string {
  return score >= 90 ? 'bg-green-500' : score >= 70 ? 'bg-yellow-500' : 'bg-red-500';
}

function getConfidenceLevel(score: number): string {
  return score >= 90
    ? '🟢 Confiança muito alta'
    : score >= 70
      ? '🟡 Confiança adequada'
      : '🔴 Confiança baixa';
}

interface InfoFieldProps {
  label: string;
  value: string;
}

function InfoField({ label, value }: InfoFieldProps) {
  return (
    <div>
      <p className="text-gray-600 text-sm font-medium">{label}</p>
      <p className="text-gray-900 font-semibold mt-1">{value}</p>
    </div>
  );
}
