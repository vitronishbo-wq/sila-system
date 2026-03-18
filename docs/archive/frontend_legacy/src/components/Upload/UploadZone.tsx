import { useCallback, useEffect } from "react";
import { useDropzone } from "react-dropzone";
import { useDocumentUpload } from "@/hooks/useDocumentUpload";
import { showGlobalToast } from "@/utils/globalToast";
import { UploadCloud as UploadIcon, Loader2, CheckCircle, AlertCircle, Trash2 } from "lucide-react";

const MAX_SIZE = 20 * 1024 * 1024; // 20MB (conformado com o hook)

// Fallback para notificações se toast provider não estiver disponível
const notifyUser = (type: 'success' | 'error', message: string) => {
    showGlobalToast?.({ type, message });
};

export const UploadZone = ({ onUploadSuccess }: { onUploadSuccess?: (data: any) => void }) => {
    const { uploads, uploadFiles, cancelUpload } = useDocumentUpload();
    const isUploading = uploads.some(u => u.status === 'uploading' || u.status === 'processing');

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        if (acceptedFiles.length === 0) return;
        // Dispara upload paralelo de múltiplos ficheiros
        await uploadFiles(acceptedFiles);
    }, [uploadFiles]);

    // Feedback quando upload conclui (sucesso ou erro)
    useEffect(() => {
        uploads
            .filter(u => u.status === 'success')
            .forEach(u => {
                notifyUser('success', `✓ ${u.fileName} enviado com sucesso`);
                onUploadSuccess?.({ fileName: u.fileName, documentId: u.documentId });
            });
    }, [uploads, onUploadSuccess]);

    useEffect(() => {
        uploads
            .filter(u => u.status === 'error' && u.error)
            .forEach(u => {
                notifyUser('error', `✗ ${u.fileName}: ${u.error}`);
            });
    }, [uploads]);

    const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
        onDrop,
        accept: {
            "application/pdf": [".pdf"],
            "image/jpeg": [".jpg", ".jpeg"],
            "image/png": [".png"],
        },
        maxSize: MAX_SIZE,
        multiple: true,
        disabled: isUploading,
    });

    return (
        <div className="max-w-4xl mx-auto px-4">
            <div
                {...getRootProps()}
                className={`relative border-4 border-dashed rounded-3xl p-12 transition-all duration-300 group cursor-pointer
          ${isDragActive ? "border-red-500 bg-red-50" : "border-gray-200 bg-white hover:border-red-400 hover:bg-gray-50"}
          ${isUploading ? "opacity-50 cursor-not-allowed" : ""}
        `}
            >
                <input {...getInputProps()} />

                <div className="flex flex-col items-center text-center">
                    <div className={`p-6 rounded-2xl mb-6 transition-transform duration-300 group-hover:scale-110
            ${isDragActive ? "bg-red-500 text-white" : "bg-red-50 text-red-600"}
          `}>
                        {isUploading ? (
                            <Loader2 className="h-12 w-12 animate-spin" />
                        ) : (
                            <UploadIcon className="h-12 w-12" />
                        )}
                    </div>

                    <h2 className="text-2xl font-bold text-gray-800 mb-2">
                        {isDragActive ? "Solte para enviar" : "Arraste seus documentos aqui"}
                    </h2>
                    <p className="text-gray-500 max-w-sm">
                        Suporta PDF, JPG e PNG até 20MB.
                    </p>

                    <button
                        type="button"
                        onClick={(e) => { e.stopPropagation(); open(); }}
                        disabled={isUploading}
                        className="mt-8 px-8 py-3 bg-gray-900 text-white rounded-xl font-bold hover:bg-black transition shadow-lg hover:shadow-xl disabled:bg-gray-400"
                    >
                        Selecionar Documentos
                    </button>
                </div>
            </div>

            {/* Fila de uploads */}
            {uploads.length > 0 && (
                <div className="mt-8 space-y-3">
                    <h3 className="font-semibold text-gray-800">Ficheiros ({uploads.length})</h3>
                    {uploads.map(upload => (
                        <div
                            key={upload.fileName}
                            className="bg-white border border-gray-200 rounded-lg p-4 flex items-center justify-between hover:shadow-md transition"
                        >
                            <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900 truncate">
                                    {upload.fileName}
                                </p>
                                
                                {/* Progress bar para uploading/processing */}
                                {(upload.status === 'uploading' || upload.status === 'processing') && (
                                    <div className="mt-2 h-2 bg-gray-200 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-blue-600 transition-all duration-300"
                                            style={{ width: `${upload.progress}%` }}
                                        />
                                    </div>
                                )}

                                {/* Status text */}
                                <p className="text-xs text-gray-500 mt-1">
                                    {upload.status === 'pending' && 'Pendente...'}
                                    {upload.status === 'uploading' && `Enviando ${upload.progress}%...`}
                                    {upload.status === 'processing' && '⏳ Processando no servidor...'}
                                    {upload.status === 'success' && '✓ Concluído'}
                                    {upload.status === 'error' && `Erro: ${upload.error || 'Desconhecido'}`}
                                </p>
                            </div>

                            {/* Status icon */}
                            <div className="ml-4 flex-shrink-0">
                                {upload.status === 'uploading' && (
                                    <Loader2 className="h-5 w-5 text-blue-600 animate-spin" />
                                )}
                                {upload.status === 'processing' && (
                                    <Loader2 className="h-5 w-5 text-yellow-600 animate-spin" />
                                )}
                                {upload.status === 'success' && (
                                    <CheckCircle className="h-5 w-5 text-green-600" />
                                )}
                                {upload.status === 'error' && (
                                    <AlertCircle className="h-5 w-5 text-red-600" />
                                )}
                                {upload.status === 'pending' && (
                                    <div className="h-5 w-5 rounded-full border-2 border-gray-300" />
                                )}
                            </div>

                            {/* Cancel button */}
                            {(upload.status === 'pending' || upload.status === 'uploading') && (
                                <button
                                    onClick={() => cancelUpload(upload.documentId, upload.fileName)}
                                    className="ml-3 text-red-600 hover:text-red-800 transition"
                                    title="Cancelar"
                                >
                                    <Trash2 className="h-4 w-4" />
                                </button>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};