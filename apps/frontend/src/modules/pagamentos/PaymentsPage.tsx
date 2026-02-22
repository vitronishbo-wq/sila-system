
import React, { useState } from 'react';
import { 
  IdCard, 
  FileText, 
  UserCheck, 
  Droplet, 
  Zap, 
  Briefcase, 
  FileSignature, 
  Bus, 
  Gavel,
  CreditCard,
  QrCode,
  CheckCircle2,
  X,
  Search,
  ArrowRight
} from 'lucide-react';
import PaymentModal from './components/PaymentModal';

interface Service {
  id: string;
  name: string;
  icon: React.ReactNode;
  color: string;
}

const SERVICES: Service[] = [
  { id: 'identidade', name: 'Identidade Civil', icon: <IdCard className="w-8 h-8" />, color: 'bg-blue-500' },
  { id: 'registo', name: 'Registo Civil', icon: <FileText className="w-8 h-8" />, color: 'bg-green-500' },
  { id: 'contribuinte', name: 'Contribuinte (AGT)', icon: <UserCheck className="w-8 h-8" />, color: 'bg-yellow-500' },
  { id: 'agua', name: 'Água e Saneamento', icon: <Droplet className="w-8 h-8" />, color: 'bg-cyan-500' },
  { id: 'energia', name: 'Energia Elétrica', icon: <Zap className="w-8 h-8" />, color: 'bg-orange-500' },
  { id: 'emprego', name: 'Emprego e Trabalho', icon: <Briefcase className="w-8 h-8" />, color: 'bg-purple-500' },
  { id: 'licenciamento', name: 'Licenciamento', icon: <FileSignature className="w-8 h-8" />, color: 'bg-red-500' },
  { id: 'transportes', name: 'Transportes', icon: <Bus className="w-8 h-8" />, color: 'bg-emerald-500' },
  { id: 'cartorios', name: 'Cartórios e Notariado', icon: <Gavel className="w-8 h-8" />, color: 'bg-indigo-500' },
];

const App: React.FC = () => {
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [isPaymentModalOpen, setIsPaymentModalOpen] = useState(false);

  const handleServiceClick = (service: Service) => {
    setSelectedService(service);
    setIsPaymentModalOpen(true);
  };

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-[#f8fafc]">
      {/* Left Sidebar - Hero Section */}
      <div className="w-full md:w-[450px] bg-[#1a202c] text-white p-8 flex flex-col justify-between relative overflow-hidden">
        <div className="absolute top-0 right-0 w-full h-full opacity-10 pointer-events-none">
          <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" className="w-full h-full scale-150">
            <path fill="#FFFFFF" d="M44.7,-76.4C58.8,-69.2,71.8,-59.1,79.6,-46.1C87.4,-33.1,90,-16.5,88.4,-0.9C86.8,14.7,81,29.4,72.4,42.2C63.8,55.1,52.4,66,39,73.1C25.7,80.1,10.3,83.3,-4.2,89.5C-18.7,95.7,-37.3,104.9,-51,100.1C-64.7,95.3,-73.4,76.5,-79.9,59.3C-86.4,42.1,-90.7,26.5,-91.4,10.9C-92.1,-4.7,-89.2,-20.3,-82.1,-34.5C-75,-48.7,-63.7,-61.5,-50.3,-69.1C-36.9,-76.7,-21.5,-79.1,-4.7,-71C12.1,-62.9,25.3,-66,44.7,-76.4Z" transform="translate(100 100)" />
          </svg>
        </div>

        <div className="z-10">
          <div className="flex items-center gap-3 mb-12">
            <div className="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center font-bold text-2xl">S</div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">SILA-System</h1>
              <p className="text-xs text-gray-400">Integrated Local Administration System</p>
            </div>
          </div>

          <div className="mt-20">
            <h2 className="text-5xl font-extrabold leading-tight mb-6">
              Administração <br />
              <span className="text-yellow-500">mais próxima de si.</span>
            </h2>
            <p className="text-lg text-gray-300 max-w-sm mb-10">
              Aceda aos serviços públicos de forma rápida, segura e sem burocracia.
            </p>

            <div className="relative max-w-sm">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input 
                type="text" 
                placeholder="O que deseja tratar hoje?" 
                className="w-full bg-white text-gray-900 pl-12 pr-4 py-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-500 shadow-lg"
              />
            </div>
          </div>
        </div>

        <div className="z-10 mt-10">
          <div className="flex gap-6 text-sm text-gray-400">
            <a href="#" className="hover:text-white transition-colors">Ajuda</a>
            <a href="#" className="hover:text-white transition-colors">Contactos</a>
            <span className="opacity-50">v2026.1</span>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 p-6 md:p-12 overflow-y-auto">
        <div className="max-w-6xl mx-auto">
          <header className="flex justify-between items-center mb-12">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-yellow-400 rounded-md flex items-center justify-center">
                <i className="fa-solid fa-star text-white text-[10px]"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-800">Serviços Essenciais</h3>
            </div>
            <div className="flex gap-4">
              <button className="px-6 py-2 text-gray-700 font-medium hover:bg-gray-100 rounded-lg transition-all">Entrar</button>
              <button className="px-6 py-2 bg-[#1a202c] text-white font-bold rounded-lg hover:bg-gray-800 transition-all shadow-md">Criar Conta</button>
            </div>
          </header>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {SERVICES.map((service) => (
              <div 
                key={service.id}
                onClick={() => handleServiceClick(service)}
                className="group bg-white p-8 rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 cursor-pointer border border-transparent hover:border-gray-100 flex flex-col items-center justify-center text-center h-[220px]"
              >
                <div className={`${service.color} text-white p-4 rounded-2xl mb-4 group-hover:scale-110 transition-transform duration-300`}>
                  {service.icon}
                </div>
                <span className="text-gray-700 font-semibold group-hover:text-gray-900">{service.name}</span>
              </div>
            ))}
          </div>

          <footer className="mt-20 pt-10 border-t border-gray-200 text-center text-gray-400 text-sm">
            <p>&copy; 2026 Ministério da Administração do Território</p>
          </footer>
        </div>
      </div>

      {isPaymentModalOpen && selectedService && (
        <PaymentModal 
          service={selectedService} 
          onClose={() => setIsPaymentModalOpen(false)} 
        />
      )}
    </div>
  );
};

export default App;
