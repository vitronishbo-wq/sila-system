import { Link } from 'react-router-dom';

export const UnauthorizedPage = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4">
            <div className="max-w-md w-full text-center space-y-8">
                {/* Ícone ou imagem subtil da bandeira (opcional) */}
                <div className="mx-auto w-32 h-32 bg-red-600 rounded-full opacity-10 flex items-center justify-center">
                    <div className="w-16 h-16 bg-red-600 rounded-full animate-pulse"></div>
                </div>

                <h1 className="text-3xl font-black text-gray-900 tracking-tight">Acesso Não Autorizado</h1>

                <p className="text-lg text-gray-600 font-medium">
                    O seu perfil não tem permissão para aceder a este portal administrativo.
                </p>

                <p className="text-gray-500 leading-relaxed">
                    Pode ter selecionado por engano o nível errado. Escolha o portal correto de acordo com o seu cargo.
                </p>

                <div className="pt-6">
                    <Link to="/portal">
                        <button className="bg-red-600 hover:bg-red-700 text-white px-10 py-5 rounded-2xl text-lg font-black transition-all shadow-xl shadow-red-100 flex items-center justify-center mx-auto gap-3">
                            Voltar para a Seleção de Portal
                        </button>
                    </Link>
                </div>

                <footer className="mt-12 text-sm font-black text-gray-300 uppercase tracking-widest">
                    República de Angola • Governo Digital 2025
                </footer>
            </div>
        </div>
    );
};

export default UnauthorizedPage;
