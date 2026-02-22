
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';
import { ASSETS, APP_VERSION } from '../constants';

const Register: React.FC = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        nif: '',
        password: '',
        confirmPassword: ''
    });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        if (formData.password !== formData.confirmPassword) {
            setError('As palavras-passe não coincidem.');
            setIsLoading(false);
            return;
        }

        try {
            const { confirmPassword, ...registerData } = formData;
            await authService.register(registerData);
            setSuccess(true);
            setTimeout(() => {
                navigate('/citizen/login');
            }, 3000);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao criar conta. Verifique os dados introduzidos.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex bg-white font-inter">
            {/* Left Side: Visual/Hero */}
            <div className="hidden lg:flex lg:w-1/2 relative bg-slate-900 overflow-hidden">
                <img
                    src={ASSETS.LOGIN_HERO}
                    alt="Angola Architecture"
                    className="absolute inset-0 w-full h-full object-cover opacity-60"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent"></div>

                <div className="relative z-10 w-full p-16 flex flex-col justify-end text-white">
                    <div className="mb-12">
                        <img src={ASSETS.BRASAO} alt="Brasão" className="w-24 mb-6 shadow-2xl" />
                        <h2 className="text-5xl font-extrabold tracking-tight mb-4">SILA-System</h2>
                        <p className="text-xl opacity-80 max-w-md">Junte-se ao Sistema Integrado de Administração Local. Crie a sua conta para aceder aos serviços do cidadão.</p>
                    </div>
                    <div className="flex gap-4 items-center">
                        <div className="w-12 h-1 bg-yellow-500"></div>
                        <p className="text-sm font-medium tracking-widest uppercase text-yellow-500">República de Angola</p>
                    </div>
                </div>
            </div>

            {/* Right Side: Register Form */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-slate-50 lg:bg-white overflow-y-auto">
                <div className="w-full max-w-md py-12">
                    <div className="mb-10 text-center lg:text-left">
                        <button
                            onClick={() => navigate('/')}
                            className="mb-6 flex items-center gap-2 text-slate-500 hover:text-slate-900 font-semibold transition-colors"
                        >
                            <i className="fa-solid fa-arrow-left"></i>
                            <span>Voltar</span>
                        </button>
                        <h1 className="text-3xl font-bold text-slate-900 mb-2">Criar Conta</h1>
                        <p className="text-gray-500">Registe-se como cidadão para solicitar e acompanhar serviços públicos.</p>
                    </div>

                    {success ? (
                        <div className="p-8 bg-green-50 border border-green-100 rounded-2xl text-center space-y-4">
                            <div className="w-16 h-16 bg-green-500 text-white rounded-full flex items-center justify-center mx-auto text-3xl">
                                <i className="fa-solid fa-check"></i>
                            </div>
                            <h3 className="text-xl font-bold text-green-900">Conta Criada com Sucesso!</h3>
                            <p className="text-green-700">A sua conta foi registada. A redirecionar para a página de login...</p>
                        </div>
                    ) : (
                        <form onSubmit={handleRegister} className="space-y-5">
                            {error && (
                                <div className="p-4 bg-red-50 border border-red-200 text-red-600 rounded-xl flex items-center gap-3 text-sm font-medium animate-shake">
                                    <i className="fa-solid fa-circle-exclamation"></i>
                                    {error}
                                </div>
                            )}

                            <div>
                                <label className="block text-sm font-bold text-slate-700 mb-2">Nome Completo</label>
                                <div className="relative">
                                    <input
                                        name="name"
                                        type="text"
                                        value={formData.name}
                                        onChange={handleChange}
                                        className="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-4 focus:ring-slate-100 focus:border-slate-900 outline-none transition-all pl-12"
                                        placeholder="Seu nome completo"
                                        required
                                    />
                                    <i className="fa-solid fa-id-card absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-bold text-slate-700 mb-2">Email</label>
                                <div className="relative">
                                    <input
                                        name="email"
                                        type="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        className="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-4 focus:ring-slate-100 focus:border-slate-900 outline-none transition-all pl-12"
                                        placeholder="email@exemplo.gv.ao"
                                        required
                                    />
                                    <i className="fa-solid fa-envelope absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-bold text-slate-700 mb-2">NIF (Número de Identificação Fiscal)</label>
                                <div className="relative">
                                    <input
                                        name="nif"
                                        type="text"
                                        value={formData.nif}
                                        onChange={handleChange}
                                        className="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-4 focus:ring-slate-100 focus:border-slate-900 outline-none transition-all pl-12"
                                        placeholder="Introduza o seu NIF"
                                        required
                                    />
                                    <i className="fa-solid fa-fingerprint absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-bold text-slate-700 mb-2">Palavra-passe</label>
                                    <div className="relative">
                                        <input
                                            name="password"
                                            type="password"
                                            value={formData.password}
                                            onChange={handleChange}
                                            className="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-4 focus:ring-slate-100 focus:border-slate-900 outline-none transition-all pl-12"
                                            placeholder="••••••••"
                                            required
                                        />
                                        <i className="fa-solid fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-bold text-slate-700 mb-2">Confirmar</label>
                                    <div className="relative">
                                        <input
                                            name="confirmPassword"
                                            type="password"
                                            value={formData.confirmPassword}
                                            onChange={handleChange}
                                            className="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-4 focus:ring-slate-100 focus:border-slate-900 outline-none transition-all pl-12"
                                            placeholder="••••••••"
                                            required
                                        />
                                        <i className="fa-solid fa-shield-check absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                                    </div>
                                </div>
                            </div>

                            <div className="pt-2">
                                <button
                                    type="submit"
                                    disabled={isLoading}
                                    className="w-full py-4 bg-slate-900 text-white rounded-xl font-bold text-lg hover:bg-slate-800 transition-all shadow-lg active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
                                >
                                    {isLoading ? (
                                        <i className="fa-solid fa-circle-notch fa-spin"></i>
                                    ) : (
                                        <>
                                            <span>Criar a minha conta</span>
                                            <i className="fa-solid fa-user-plus"></i>
                                        </>
                                    )}
                                </button>
                            </div>
                        </form>
                    )}

                    {!success && (
                        <div className="mt-8 text-center text-gray-600">
                            <p>Já tem uma conta? <button onClick={() => navigate('/citizen/login')} className="text-slate-900 font-bold hover:underline">Entre aqui.</button></p>
                        </div>
                    )}

                    {!success && (
                        <div className="mt-12 pt-8 border-t text-center text-gray-400 text-xs">
                            <div className="flex justify-center gap-4">
                                <img src={ASSETS.BRASAO} alt="MAT" className="h-6 opacity-40 grayscale" />
                                <p className="border-l pl-4">v{APP_VERSION}</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Register;
