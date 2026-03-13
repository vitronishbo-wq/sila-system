import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import api from "@/services/api";
import { toast } from "react-hot-toast";
import { UploadCloud as UploadIcon, Loader2 } from "lucide-react";

const MAX_SIZE = 50 * 1024 * 1024; // 50MB

export const UploadZone = ({ onUploadSuccess }: { onUploadSuccess?: (data: any) => void }) => {
    const [uploading, setUploading] = useState(false);
    const [progress, setProgress] = useState(0);

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        if (acceptedFiles.length === 0) return;

        const formData = new FormData();
        acceptedFiles.forEach(file => formData.append("files", file));

        setUploading(true);
        setProgress(0);

        try {
            // O token já é injetado pelo interceptor do Axios
            const response = await api.post("/documents/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
                onUploadProgress: (e) => {
                    if (e.total) setProgress(Math.round((e.loaded * 100) / e.total));
                },
            });

            toast.success(`${acceptedFiles.length} documento(s) enviado(s).`);
            onUploadSuccess?.(response.data);
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail || "Erro no upload para o servidor";
            toast.error(errorMsg);
        } finally {
            setUploading(false);
            setProgress(0);
        }
    }, [onUploadSuccess]);

    const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
        onDrop,
        accept: {
            "application/pdf": [".pdf"],
            "image/jpeg": [".jpg", ".jpeg"],
            "image/png": [".png"],
        },
        maxSize: MAX_SIZE,
        multiple: true,
        disabled: uploading,
    });

    return (
        <div className="max-w-4xl mx-auto px-4">
            <div
                {...getRootProps()}
                className={`relative border-4 border-dashed rounded-3xl p-12 transition-all duration-300 group cursor-pointer
          ${isDragActive ? "border-red-500 bg-red-50" : "border-gray-200 bg-white hover:border-red-400 hover:bg-gray-50"}
          ${uploading ? "opacity-50 cursor-not-allowed" : ""}
        `}
            >
                <input {...getInputProps()} />

                <div className="flex flex-col items-center text-center">
                    <div className={`p-6 rounded-2xl mb-6 transition-transform duration-300 group-hover:scale-110
            ${isDragActive ? "bg-red-500 text-white" : "bg-red-50 text-red-600"}
          `}>
                        {uploading ? (
                            <Loader2 className="h-12 w-12 animate-spin" />
                        ) : (
                            <UploadIcon className="h-12 w-12" />
                        )}
                    </div>

                    <h2 className="text-2xl font-bold text-gray-800 mb-2">
                        {isDragActive ? "Solte para enviar" : "Arraste seus documentos aqui"}
                    </h2>
                    <p className="text-gray-500 max-w-sm">
                        Suporta PDF, JPG e PNG até 50MB.
                    </p>

                    <button
                        type="button"
                        onClick={(e) => { e.stopPropagation(); open(); }}
                        disabled={uploading}
                        className="mt-8 px-8 py-3 bg-gray-900 text-white rounded-xl font-bold hover:bg-black transition shadow-lg hover:shadow-xl disabled:bg-gray-400"
                    >
                        Selecionar Documentos
                    </button>
                </div>

                {uploading && (
                    <div className="absolute inset-x-0 bottom-0 p-1">
                        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-red-600 transition-all duration-300 ease-out"
                                style={{ width: `${progress}%` }}
                            />
                        </div>
                        <p className="text-center text-xs font-bold text-red-600 mt-2 uppercase tracking-widest">
                            Enviando: {progress}%
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};