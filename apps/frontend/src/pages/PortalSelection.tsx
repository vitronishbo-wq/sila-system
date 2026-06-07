import { useNavigate } from "react-router-dom";
import { APP_IMAGES } from "@/constants/images";
import { LayoutGrid, Building2, Users } from "lucide-react";

export default function PortalSelection() {
    const navigate = useNavigate();

    const portals = [
        {
            id: "CENTRAL",
            name: "Nível Central",
            subtitle: "Painel Nacional",
            description: "Visão estratégica e indicadores consolidados de todo o país para tomada de decisão.",
            image: APP_IMAGES.LEVEL_CENTRAL,
            icon: LayoutGrid,
            path: "/admin/national",
            color: "from-gray-800 to-black",
            badge: "Central"
        },
        {
            id: "PROVINCIAL",
            name: "Nível Provincial",
            subtitle: "Gestão Local",
            description: "Administração técnica dos governos provinciais e monitorização de infraestruturas.",
            image: APP_IMAGES.LEVEL_PROVINCIAL,
            icon: Building2,
            path: "/admin/province",
            color: "from-red-600 to-red-800",
            badge: "Provincial"
        },
        {
            id: "LOCAL",
            name: "Nível Municipal",
            subtitle: "Portal do Cidadão",
            description: "Geração de documentos, pagamentos de taxas e serviços públicos simplificados.",
            image: APP_IMAGES.LEVEL_MUNICIPAL,
            icon: Users,
            path: "/citizen",
            color: "from-blue-600 to-blue-800",
            badge: "Municipal"
        },
    ];

    return (
        <div className="min-h-screen bg-[#f8fafc] py-16 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="text-center mb-24 space-y-4">
                    <div className="inline-block px-4 py-1.5 bg-red-50 rounded-full text-red-600 text-xs font-bold uppercase tracking-widest mb-4">
                        Seleção de Portal Integrado
                    </div>
                    <h1 className="text-6xl font-black text-gray-900 tracking-tighter">
                        Ecossistema <span className="text-red-600">SILA</span>
                    </h1>
                    <p className="text-xl text-gray-500 max-w-2xl mx-auto font-medium leading-relaxed">
                        Selecione a esfera administrativa para aceder aos seus serviços digitais de forma segura e centralizada.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
                    {portals.map((portal) => (
                        <div
                            key={portal.id}
                            onClick={() => navigate(portal.path)}
                            className="group cursor-pointer bg-white rounded-[3rem] shadow-2xl overflow-hidden transform hover:-translate-y-4 transition-all duration-700 border border-transparent hover:border-red-100 flex flex-col h-full"
                        >
                            <div className="relative h-72 w-full overflow-hidden">
                                <img
                                    src={portal.image}
                                    alt={portal.name}
                                    className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000"
                                />
                                <div className={`absolute inset-0 bg-gradient-to-t ${portal.color} opacity-40 group-hover:opacity-60 transition-opacity duration-700`} />
                                <div className="absolute top-8 left-8">
                                    <span className="bg-white/20 backdrop-blur-md text-white text-[10px] font-black uppercase tracking-[0.2em] px-4 py-1.5 rounded-full border border-white/30">
                                        {portal.badge}
                                    </span>
                                </div>
                                <div className="absolute bottom-[-2rem] right-8 group-hover:bottom-8 transition-all duration-700 opacity-0 group-hover:opacity-100">
                                    <div className="bg-white p-4 rounded-3xl shadow-2xl">
                                        <portal.icon className="h-8 w-8 text-red-600" />
                                    </div>
                                </div>
                            </div>

                            <div className="p-12 flex-grow flex flex-col">
                                <div className="mb-6">
                                    <span className="text-xs font-black text-red-600 uppercase tracking-widest opacity-60">{portal.name}</span>
                                    <h3 className="text-3xl font-black text-gray-900 mt-2 tracking-tight">
                                        {portal.subtitle}
                                    </h3>
                                </div>
                                <p className="text-gray-500 leading-relaxed font-medium mb-10 text-lg">
                                    {portal.description}
                                </p>
                                <div className="mt-auto flex items-center text-sm font-black text-red-600 group-hover:gap-4 gap-2 transition-all">
                                    Aceder agora
                                    <svg className="w-6 h-6 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="mt-28 flex flex-col items-center gap-4 text-gray-400">
                    <div className="h-px w-20 bg-gray-200" />
                    <p className="text-xs font-bold uppercase tracking-widest opacity-60">República de Angola • Governo Digital 2025</p>
                </div>
            </div>
        </div>
    );
}
