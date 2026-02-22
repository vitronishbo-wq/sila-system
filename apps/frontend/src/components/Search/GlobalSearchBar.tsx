import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Search } from "lucide-react";

export const GlobalSearchBar = () => {
    const [query, setQuery] = useState("");
    const navigate = useNavigate();
    const inputRef = useRef<HTMLInputElement>(null);

    // CTRL+K / CMD+K Shortcut
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if ((e.ctrlKey || e.metaKey) && e.key === "k") {
                e.preventDefault();
                inputRef.current?.focus();
            }
        };

        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, []);

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim().length >= 3) {
            navigate(`/search/deep?q=${encodeURIComponent(query.trim())}`);
            setQuery(""); // Clear after search
        }
    };

    return (
        <form onSubmit={handleSearch} className="relative w-full max-w-lg group">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 group-focus-within:text-red-600 transition-colors z-10" />
            <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Buscar no conteúdo dos documentos..."
                className="w-full pl-12 pr-12 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-4 focus:ring-red-100 text-lg bg-white/90 backdrop-blur shadow-sm transition-all"
            />
            <div className="absolute right-4 top-1/2 -translate-y-1/2 hidden sm:flex items-center gap-1">
                <kbd className="px-2 py-1 text-[10px] font-bold text-gray-400 bg-gray-100 border border-gray-200 rounded-md">
                    CTRL
                </kbd>
                <span className="text-gray-300 font-bold">+</span>
                <kbd className="px-2 py-1 text-[10px] font-bold text-gray-400 bg-gray-100 border border-gray-200 rounded-md">
                    K
                </kbd>
            </div>
            {query.trim().length > 0 && query.trim().length < 3 && (
                <div className="absolute top-full left-6 mt-2 px-3 py-1 bg-black/90 text-white text-[10px] font-bold rounded-lg animate-in fade-in slide-in-from-top-2 border border-white/10 shadow-xl z-50">
                    Mínimo 3 caracteres
                </div>
            )}
        </form>
    );
};
