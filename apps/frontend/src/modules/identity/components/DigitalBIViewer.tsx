/**
 * Digital BI Viewer Component
 * View, download, verify, and manage digital BI documents
 */

import React, { useState } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { useDigitalBI, useBITemplates } from '../hooks';
import {
  isDigitalBIValid,
  getDaysUntilExpiry,
  isBIExpiringSoon,
  generateBIQRCodeData,
  parseBIQRCodeData,
} from '../utils';
import { DigitalBIDocument, DigitalBIIssueRequest } from '../types';
import { identityService } from '../services';

interface DigitalBIViewerProps {
  citizenId: string;
  citizenName: string;
  citizenNationalId: string;
  citizenBirthDate: string;
  onIssueRequest?: (request: DigitalBIIssueRequest) => void;
}

/**
 * DigitalBIViewer - Complete BI document management interface
 */
export const DigitalBIViewer: React.FC<DigitalBIViewerProps> = ({
  citizenId,
  citizenName,
  citizenNationalId,
  citizenBirthDate,
  onIssueRequest,
}) => {
  const { documents, loading, error, requestDigitalBI, revokeDigitalBI } =
    useDigitalBI(citizenId);
  const { templates: biTemplates } = useBITemplates();
  const [selectedDocument, setSelectedDocument] = useState<DigitalBIDocument | null>(null);
  const [viewMode, setViewMode] = useState<'list' | 'detail' | 'issue'>('list');
  const [issuanceLoading, setIssuanceLoading] = useState(false);
  const [issuanceError, setIssuanceError] = useState<string | null>(null);
  const [showRevocationDialog, setShowRevocationDialog] = useState(false);
  const [revocationReason, setRevocationReason] = useState('');
  const [revokingId, setRevokingId] = useState<string | null>(null);

  const handleIssueRequest = async (documentType: 'BI' | 'PASSPORT' | 'RESIDENCE_PERMIT', validityYears: number) => {
    setIssuanceLoading(true);
    setIssuanceError(null);

    try {
      const request: DigitalBIIssueRequest = {
        citizen_id: citizenId,
        document_type: documentType,
        validity_years: validityYears,
        include_mrz: true,
        include_nfc: true,
        template_version: biTemplates.length > 0 ? biTemplates[0].version : 'v1',
      };

      const response = await requestDigitalBI(request);

      if (onIssueRequest) {
        onIssueRequest(request);
      }

      setViewMode('list');
    } catch (err) {
      setIssuanceError(err instanceof Error ? err.message : 'Erro ao solicitar emissão');
    } finally {
      setIssuanceLoading(false);
    }
  };

  const handleDownload = async (documentId: string) => {
    try {
      const blob = await identityService.downloadDigitalBI(documentId);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `BI_${documentId}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      console.error('Download failed:', err);
    }
  };

  const handleRevoke = async () => {
    if (!selectedDocument || !revocationReason) return;

    setRevokingId(selectedDocument.id);
    try {
      await revokeDigitalBI(selectedDocument.id, revocationReason);
      setShowRevocationDialog(false);
      setSelectedDocument(null);
      setRevocationReason('');
    } catch (err) {
      console.error('Revocation failed:', err);
    } finally {
      setRevokingId(null);
    }
  };

  if (loading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="font-bold text-red-800 mb-2">Erro ao carregar documentos</h3>
        <p className="text-red-700 text-sm">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* List view */}
      {viewMode === 'list' && (
        <DocumentListView
          documents={documents}
          onSelectDocument={(doc) => {
            setSelectedDocument(doc);
            setViewMode('detail');
          }}
          onIssueNew={() => setViewMode('issue')}
        />
      )}

      {/* Detail view */}
      {viewMode === 'detail' && selectedDocument && (
        <DocumentDetailView
          document={selectedDocument}
          citizenName={citizenName}
          citizenNationalId={citizenNationalId}
          citizenBirthDate={citizenBirthDate}
          onBack={() => {
            setSelectedDocument(null);
            setViewMode('list');
          }}
          onDownload={() => handleDownload(selectedDocument.id)}
          onRevoke={() => setShowRevocationDialog(true)}
          onShowQR={() => setViewMode('detail')}
        />
      )}

      {/* Issue request form */}
      {viewMode === 'issue' && (
        <DocumentIssueForm
          citizenId={citizenId}
          isLoading={issuanceLoading}
          error={issuanceError}
          onSubmit={handleIssueRequest}
          onCancel={() => setViewMode('list')}
        />
      )}

      {/* Revocation dialog */}
      {showRevocationDialog && selectedDocument && (
        <RevocationDialog
          document={selectedDocument}
          reason={revocationReason}
          onReasonChange={setRevocationReason}
          onConfirm={handleRevoke}
          onCancel={() => {
            setShowRevocationDialog(false);
            setRevocationReason('');
          }}
          isLoading={revokingId === selectedDocument.id}
        />
      )}
    </div>
  );
};

// ============= SUB-COMPONENTS =============

/**
 * Loading state
 */
function LoadingState() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 2 }).map((_, i) => (
        <div key={i} className="h-32 bg-gray-100 rounded-lg animate-pulse" />
      ))}
    </div>
  );
}

/**
 * Document list view
 */
function DocumentListView({
  documents,
  onSelectDocument,
  onIssueNew,
}: {
  documents: DigitalBIDocument[];
  onSelectDocument: (doc: DigitalBIDocument) => void;
  onIssueNew: () => void;
}) {
  if (documents.length === 0) {
    return (
      <div>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-8 text-center mb-6">
          <div className="text-5xl mb-4">📋</div>
          <h3 className="font-bold text-lg text-blue-900 mb-2">Nenhum Documento BI Digital</h3>
          <p className="text-blue-800 text-sm mb-6">
            Você ainda não tem nenhum documento BI digital emitido. Solicite um novo documento.
          </p>
          <button
            onClick={onIssueNew}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 font-medium"
          >
            Solicitar Novo Documento
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold text-gray-900">Meus Documentos BI Digital</h3>
        <button
          onClick={onIssueNew}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 text-sm font-medium"
        >
          + Novo Documento
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {documents.map((doc) => (
          <DocumentCard
            key={doc.id}
            document={doc}
            onClick={() => onSelectDocument(doc)}
          />
        ))}
      </div>
    </div>
  );
}

/**
 * Single document card
 */
function DocumentCard({
  document,
  onClick,
}: {
  document: DigitalBIDocument;
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

  const statusColor = {
    PENDING: 'bg-yellow-100 text-yellow-800',
    ISSUED: 'bg-green-100 text-green-800',
    REVOKED: 'bg-red-100 text-red-800',
    EXPIRED: 'bg-gray-100 text-gray-800',
  }[document.status] || 'bg-gray-100 text-gray-800';

  return (
    <button
      onClick={onClick}
      className="p-6 bg-white rounded-lg shadow border-l-4 border-blue-500 hover:shadow-lg transition-shadow text-left"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="text-4xl">{statusIcon}</div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColor}`}>
          {document.status}
        </span>
      </div>

      <h4 className="font-bold text-lg text-gray-900 mb-2">{document.document_type}</h4>
      <p className="text-sm text-gray-600 mb-3">Nº: {document.document_number}</p>

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-600">Emitido:</span>
          <span className="font-medium">{formatDate(document.issue_date)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Expira:</span>
          <span className="font-medium">{formatDate(document.expiry_date)}</span>
        </div>
        {expiringSoon && daysUntilExpiry > 0 && (
          <div className="flex justify-between text-orange-600 font-medium bg-orange-50 p-2 rounded mt-2">
            <span>⚠️ Expira em:</span>
            <span>{daysUntilExpiry} dias</span>
          </div>
        )}
      </div>
    </button>
  );
}

/**
 * Document detail view
 */
function DocumentDetailView({
  document,
  citizenName,
  citizenNationalId,
  citizenBirthDate,
  onBack,
  onDownload,
  onRevoke,
}: {
  document: DigitalBIDocument;
  citizenName: string;
  citizenNationalId: string;
  citizenBirthDate: string;
  onBack: () => void;
  onDownload: () => void;
  onRevoke: () => void;
}) {
  const { isValid } = isDigitalBIValid(document);
  const daysUntilExpiry = getDaysUntilExpiry(document.expiry_date);
  const expiringSoon = isBIExpiringSoon(document.expiry_date);

  const qrPayload = {
    national_id_number: citizenNationalId,
    full_name: citizenName,
    birth_date: citizenBirthDate,
    document_id: document.id,
    issue_date: document.issue_date,
    expiry_date: document.expiry_date,
    signature: document.digital_signature?.signature_hex,
  };

  if (import.meta.env.DEV) {
    console.log('[DigitalBIViewer] QR payload', qrPayload);
  }

  const qrData = generateBIQRCodeData(qrPayload);

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-8 text-white">
        <button
          onClick={onBack}
          className="mb-4 text-blue-100 hover:text-white font-medium text-sm"
        >
          ← Voltar
        </button>
        <h2 className="text-3xl font-bold">{document.document_type}</h2>
        <p className="text-blue-100 mt-2">Nº {document.document_number}</p>
      </div>

      <div className="p-6 space-y-6">
        {/* Status banner */}
        {!isValid && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            <p className="font-medium">⚠️ Este documento não é válido</p>
            <p className="text-sm mt-1">Status: {document.status}</p>
          </div>
        )}

        {expiringSoon && daysUntilExpiry > 0 && (
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4 text-orange-700">
            <p className="font-medium">⚠️ O documento está a expirar</p>
            <p className="text-sm mt-1">Expira em {daysUntilExpiry} dias</p>
          </div>
        )}

        {/* Document info grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <InfoField label="Tipo de Documento" value={document.document_type} />
          <InfoField label="Número" value={document.document_number} />
          <InfoField label="Data de Emissão" value={formatDate(document.issue_date)} />
          <InfoField label="Data de Expiração" value={formatDate(document.expiry_date)} />
          <InfoField label="Estado" value={document.status} />
          <InfoField label="Validade" value={isValid ? 'Válido' : 'Inválido'} />
        </div>

        {/* NIDs and security features */}
        {document.mrz_data && (
          <div>
            <h4 className="font-bold text-gray-900 mb-3">Dados MRZ (Machine Readable Zone)</h4>
            <div className="bg-gray-50 p-4 rounded border border-gray-200 font-mono text-xs text-gray-600 break-all">
              {document.mrz_data}
            </div>
          </div>
        )}

        {document.nfc_data && (
          <div>
            <h4 className="font-bold text-gray-900 mb-3">Chip NFC (Contactless)</h4>
            <div className="grid grid-cols-2 gap-4">
              <InfoField label="Serial do Chip" value={document.nfc_data.chip_serial} />
              <InfoField label="Estado do Chip" value={document.nfc_data.chip_status} />
            </div>
          </div>
        )}

        {/* QR Code */}
        {(document.status === 'ISSUED' || document.qr_code_url) && (
          <div>
            <h4 className="font-bold text-gray-900 mb-3">Código QR</h4>
            <div className="bg-gray-50 p-6 rounded border border-gray-200 text-center">
              <div className="w-48 h-48 mx-auto mb-4 bg-white p-2 border border-gray-300 rounded">
                <QRCodeSVG value={qrData} size={176} level="H" includeMargin />
              </div>
              <p className="text-xs text-gray-600">
                Escaneie para validar a autenticidade e o status do documento offline.
              </p>
            </div>
          </div>
        )}

        {/* Digital signature */}
        {document.digital_signature && (
          <div>
            <h4 className="font-bold text-gray-900 mb-3">Assinatura Digital</h4>
            <div className="grid grid-cols-2 gap-4">
              <InfoField
                label="Certificado SN"
                value={document.digital_signature.certificate_sn}
              />
              <InfoField
                label="Assinado em"
                value={formatDateTime(document.digital_signature.signed_at)}
              />
            </div>
          </div>
        )}

        {/* Action buttons */}
        <div className="border-t pt-6 flex gap-3">
          {isValid && (
            <button
              onClick={onDownload}
              className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 font-medium"
            >
              📥 Descarregar PDF
            </button>
          )}
          {document.status === 'ISSUED' && (
            <button
              onClick={onRevoke}
              className="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 font-medium"
            >
              🚫 Revogar
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

/**
 * Document issue request form
 */
function DocumentIssueForm({
  citizenId,
  isLoading,
  error,
  onSubmit,
  onCancel,
}: {
  citizenId: string;
  isLoading: boolean;
  error: string | null;
  onSubmit: (type: 'BI' | 'PASSPORT' | 'RESIDENCE_PERMIT', validityYears: number) => void;
  onCancel: () => void;
}) {
  const [documentType, setDocumentType] = useState<'BI' | 'PASSPORT' | 'RESIDENCE_PERMIT'>('BI');
  const [validityYears, setValidityYears] = useState(10);

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-2xl font-bold mb-6">Solicitar Novo Documento</h3>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded text-red-700">
          {error}
        </div>
      )}

      <div className="space-y-6">
        {/* Document type selection */}
        <div>
          <label className="block font-medium text-gray-900 mb-3">Tipo de Documento</label>
          <div className="grid grid-cols-3 gap-3">
            {(['BI', 'PASSPORT', 'RESIDENCE_PERMIT'] as const).map((type) => (
              <button
                key={type}
                onClick={() => setDocumentType(type)}
                className={`p-4 rounded-lg border-2 transition-all text-center font-medium ${
                  documentType === type
                    ? 'border-blue-500 bg-blue-50 text-blue-900'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                {type === 'BI' ? '🪪 BI' : type === 'PASSPORT' ? '🛂 Passaporte' : '🏠 Residência'}
                <p className="text-xs mt-1">{type}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Validity period */}
        <div>
          <label htmlFor="validity" className="block font-medium text-gray-900 mb-3">
            Período de Validade
          </label>
          <div className="flex items-center gap-4">
            <input
              id="validity"
              type="range"
              min="1"
              max="20"
              value={validityYears}
              onChange={(e) => setValidityYears(parseInt(e.target.value))}
              className="flex-1"
            />
            <div className="text-right min-w-[100px]">
              <p className="text-2xl font-bold text-blue-600">{validityYears}</p>
              <p className="text-xs text-gray-600">anos</p>
            </div>
          </div>
        </div>

        {/* Document features */}
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <p className="font-medium text-blue-900 mb-3">O documento incluirá:</p>
          <ul className="space-y-2 text-sm text-blue-800">
            <li>✓ Dados de Zona de Leitura por Máquina (MRZ)</li>
            <li>✓ Chip NFC para contactless</li>
            <li>✓ Código QR para verificação rápida</li>
            <li>✓ Assinatura digital certificada</li>
          </ul>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex gap-3 mt-6 pt-6 border-t">
        <button
          onClick={onCancel}
          className="flex-1 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-medium"
        >
          Cancelar
        </button>
        <button
          onClick={() => onSubmit(documentType, validityYears)}
          disabled={isLoading}
          className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 font-medium disabled:opacity-50"
        >
          {isLoading ? 'Solicitando...' : 'Solicitar Documento'}
        </button>
      </div>
    </div>
  );
}

/**
 * Revocation dialog
 */
function RevocationDialog({
  document,
  reason,
  onReasonChange,
  onConfirm,
  onCancel,
  isLoading,
}: {
  document: DigitalBIDocument;
  reason: string;
  onReasonChange: (reason: string) => void;
  onConfirm: () => void;
  onCancel: () => void;
  isLoading: boolean;
}) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center rounded-lg">
      <div className="bg-white rounded-lg shadow-lg p-6 max-w-md w-full mx-4">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Revogar Documento</h3>

        <p className="text-gray-600 mb-4">
          Tem a certeza de que deseja revogar o documento{' '}
          <strong>{document.document_number}</strong>?
        </p>

        <div className="mb-4">
          <label htmlFor="reason" className="block font-medium text-gray-900 mb-2">
            Motivo da Revogação
          </label>
          <textarea
            id="reason"
            value={reason}
            onChange={(e) => onReasonChange(e.target.value)}
            placeholder="Descreva o motivo da revogação..."
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
          />
        </div>

        <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm mb-6">
          ⚠️ Esta ação não pode ser desfeita. O documento será marcado como revogado.
        </div>

        <div className="flex gap-3">
          <button
            onClick={onCancel}
            disabled={isLoading}
            className="flex-1 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-medium disabled:opacity-50"
          >
            Cancelar
          </button>
          <button
            onClick={onConfirm}
            disabled={isLoading || !reason}
            className="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 font-medium disabled:opacity-50"
          >
            {isLoading ? 'Revogando...' : 'Revogar'}
          </button>
        </div>
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
