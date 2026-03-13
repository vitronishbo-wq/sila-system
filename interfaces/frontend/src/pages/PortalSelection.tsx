import { useNavigate } from "react-router-dom";
import { IMAGES } from "../constants/images";
import { LayoutGrid, Building2, Users } from "lucide-react";

export default function PortalSelection() {
    const navigate = useNavigate();

    const portals = [
        {
            id: "CENTRAL",
            name: "Nível Central",
            subtitle: "Painel Nacional",
            description: "Visão estratégica e indicadores consolidados de todo o país para tomada de decisão.",
            image: IMAGES.GEO_LEVELS.NATIONAL,
            icon: LayoutGrid,
            path: "/admin/national",
            color: "from-[#0f172a] via-[#1e293b] to-[#172554]",
            badge: "Central",
            accent: "text-amber-300"
        },
        {
            id: "PROVINCIAL",
            name: "Nível Provincial",
            subtitle: "Gestão Local",
            description: "Administração técnica dos governos provinciais e monitorização de infraestruturas.",
            image: IMAGES.GEO_LEVELS.PROVINCIAL,
            icon: Building2,
            path: "/admin/province",
            color: "from-[#102d6a] via-[#1d4f91] to-[#355f9e]",
            badge: "Provincial",
            accent: "text-sky-200"
        },
        {
            id: "LOCAL",
            name: "Nível Municipal",
            subtitle: "Portal do Cidadão",
            description: "Geração de documentos, pagamentos de taxas e serviços públicos simplificados.",
            image: IMAGES.GEO_LEVELS.MUNICIPAL,
            icon: Users,
            path: "/citizen",
            color: "from-[#1f3d79] via-[#3a537f] to-[#b3862f]",
            badge: "Municipal",
            accent: "text-amber-200"
        },
    ];

    return (
        <div className="sila-shell sila-grid-overlay py-14 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto relative z-10">
                <div className="flex items-start justify-between flex-wrap gap-4 mb-14">
                    <button
                        onClick={() => navigate("/")}
                        className="group flex items-center gap-3 rounded-2xl px-4 py-3 sila-card hover:shadow-2xl transition-all"
                        title="Voltar ao início"
                    >
                        <img src={IMAGES.BRAND.INSIGNIA_ALT} alt="Insígnia Oficial" className="h-10 w-10 object-contain" />
                        <div className="text-left">
                            <p className="text-[11px] uppercase tracking-[0.24em] text-slate-500">República de Angola</p>
                            <p className="text-base font-semibold text-slate-900">Plataforma SILA</p>
                        </div>
                    </button>
                    <img src={IMAGES.BRAND.LOGO} alt="SILA System" className="h-10 opacity-90" />
                </div>

                <div className="text-center mb-20 space-y-5">
                    <div className="inline-block px-4 py-1.5 rounded-full text-[11px] font-bold uppercase tracking-[0.28em] sila-chip">
                        Acesso Institucional
                    </div>
                    <h1 className="sila-display text-5xl md:text-6xl text-slate-900 tracking-tight">
                        Identidade Digital
                        <span className="block text-[#a67921]">SILA Projecto</span>
                    </h1>
                    <p className="text-lg md:text-xl text-slate-600 max-w-3xl mx-auto font-medium leading-relaxed">
                        Selecione a esfera administrativa para aceder aos seus serviços digitais de forma segura e centralizada.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {portals.map((portal) => (
                        <div
                            key={portal.id}
                            onClick={() => navigate(portal.path)}
                            className="group cursor-pointer rounded-[2.1rem] overflow-hidden transform hover:-translate-y-2 transition-all duration-500 sila-card border border-transparent hover:border-amber-200/60 flex flex-col h-full"
                        >
                            <div className="relative h-64 w-full overflow-hidden">
                                <img
                                    src={portal.image}
                                    alt={portal.name}
                                    className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000"
                                />
                                <div className={`absolute inset-0 bg-gradient-to-t ${portal.color} opacity-78 group-hover:opacity-88 transition-opacity duration-500`} />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/45 to-transparent" />
                                <div className="absolute top-8 left-8">
                                    <span className="bg-white/20 backdrop-blur-md text-white text-[10px] font-black uppercase tracking-[0.24em] px-4 py-1.5 rounded-full border border-white/30">
                                        {portal.badge}
                                    </span>
                                </div>
                                <div className="absolute bottom-8 right-8">
                                    <portal.icon className={`h-8 w-8 ${portal.accent}`} />
                                </div>
                            </div>

                            <div className="p-9 flex-grow flex flex-col">
                                <div className="mb-5">
                                    <span className="text-[11px] font-black text-[#1e3a8a] uppercase tracking-[0.2em] opacity-75">{portal.name}</span>
                                    <h3 className="sila-display text-3xl text-slate-900 mt-2 tracking-tight">
                                        {portal.subtitle}
                                    </h3>
                                </div>
                                <p className="text-slate-600 leading-relaxed font-medium mb-8">
                                    {portal.description}
                                </p>
                                <div className="mt-auto flex items-center text-sm font-black text-[#1e3a8a] group-hover:gap-4 gap-2 transition-all">
                                    Aceder agora
                                    <svg className="w-6 h-6 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="mt-20 flex flex-col items-center gap-4 text-slate-500">
                    <div className="h-px w-20 bg-slate-300" />
                    <p className="text-xs font-bold uppercase tracking-[0.18em] opacity-70">República de Angola • Governo Digital 2026</p>
                </div>
            </div>
        </div>
    );
}
