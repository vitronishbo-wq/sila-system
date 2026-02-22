# Integração de APIs - SILA System Frontend

## 📋 Visão Geral

Este documento descreve como integrar os componentes React com os endpoints backend da API SILA.

## 🏗️ Arquitetura

### Novo Serviço Centralizado: `apiService.ts`

Localizado em: `/apps/frontend/src/services/apiService.ts`

Fornece uma interface unificada para todas as chamadas de API com:
- ✅ Gerenciamento automático de tokens JWT
- ✅ Tratamento centralizado de erros
- ✅ Interceptação de requests/responses
- ✅ Typescript typing completo
- ✅ Logout automático em 401

### Organização por Contexto

```typescript
apiService.ts
├── invoiceAPI         // Operações de faturas
├── paymentAPI         // Operações de pagamentos
├── citizenAPI         // Dados de cidadão (FUC)
├── authAPI            // Autenticação
└── publicAPI          // Endpoints públicos
```

---

## 📦 Módulos Disponíveis

### 1. **invoiceAPI** - Gerenciamento de Faturas

```typescript
import { invoiceAPI } from '@/services/apiService';

// Listar faturas de um cidadão
const invoices = await invoiceAPI.listCitizenInvoices(citizenId);

// Listar apenas faturas pendentes
const pending = await invoiceAPI.listPendingInvoices(citizenId);

// Obter detalhes de uma fatura
const invoice = await invoiceAPI.getInvoice(invoiceId);

// Cancelar fatura
const updated = await invoiceAPI.cancelInvoice(invoiceId, 'Motivo do cancelamento');

// Download de fatura
const blob = await invoiceAPI.downloadInvoice(invoiceId, 'pdf');
saveAs(blob, `fatura-${invoiceId}.pdf`);
```

### 2. **paymentAPI** - Processamento de Pagamentos

```typescript
import { paymentAPI } from '@/services/apiService';

// Registar pagamento
const payment = await paymentAPI.registerPayment({
  invoice_id: 'inv_123',
  amount: 500.00,
  currency: 'AOA',
  payment_method: 'multicaixa',
  gateway_reference: 'GW-2026022200001'
});

// Histórico de pagamentos
const history = await paymentAPI.getPaymentHistory(citizenId);

// Consultar status por referência (reconciliação)
const status = await paymentAPI.getPaymentByReference('GW-2026022200001');

// Download de comprovativo
const proof = await paymentAPI.downloadProof(paymentId);
```

### 3. **citizenAPI** - Dados do Cidadão

```typescript
import { citizenAPI } from '@/services/apiService';

// Perfil do cidadão atual (autenticado)
const profile = await citizenAPI.getCurrentProfile();

// Obter cidadão por ID
const citizen = await citizenAPI.getCitizen(citizenId);

// Eventos/histórico do cidadão
const events = await citizenAPI.getEvents(citizenId);

// Atualizar perfil
const updated = await citizenAPI.updateProfile(citizenId, {
  email: 'novo@email.com',
  phone: '+244912345678'
});
```

### 4. **authAPI** - Autenticação

```typescript
import { authAPI } from '@/services/apiService';

// Login
const { token, user } = await authAPI.login('email@example.com', 'password');

// Registrar
const { token, user } = await authAPI.register({
  email: 'novo@example.com',
  password: 'senha123',
  name: 'João Silva'
});

// Logout
authAPI.logout();

// Verificar autenticação
if (authAPI.isAuthenticated()) {
  const user = authAPI.getCurrentUser();
}
```

### 5. **publicAPI** - Endpoints Públicos

```typescript
import { publicAPI } from '@/services/apiService';

// Listar serviços disponíveis (sem autenticação)
const services = await publicAPI.listServices();

// Informações públicas
const info = await publicAPI.getInfo();
```

---

## 💻 Exemplos de Componentes Integrados

### Exemplo 1: PaymentModal com API

```typescript
import React, { useState } from 'react';
import { paymentAPI, invoiceAPI } from '@/services/apiService';
import { Payment, Invoice } from '@/services/apiService';

interface PaymentModalProps {
  invoice: Invoice;
  onClose: () => void;
  onSuccess?: (payment: Payment) => void;
}

export const PaymentModal: React.FC<PaymentModalProps> = ({ invoice, onClose, onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePayment = async (method: string) => {
    setLoading(true);
    setError(null);
    try {
      // Gerar referência única
      const gatewayRef = `GW-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      
      // Registar pagamento
      const payment = await paymentAPI.registerPayment({
        invoice_id: invoice.id,
        amount: invoice.amount,
        currency: invoice.currency,
        payment_method: method,
        gateway_reference: gatewayRef,
      });

      // Download de comprovativo
      const proof = await paymentAPI.downloadProof(payment.id);
      const url = window.URL.createObjectURL(proof);
      const a = document.createElement('a');
      a.href = url;
      a.download = `comprovativo-${payment.id}.pdf`;
      a.click();

      onSuccess?.(payment);
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao processar pagamento');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal">
      <h2>Confirmar Pagamento</h2>
      
      {error && <div className="error">{error}</div>}
      
      <div className="invoice-summary">
        <p>Montante: {invoice.amount} {invoice.currency}</p>
        <p>Referência: {invoice.id}</p>
      </div>

      <div className="payment-methods">
        <button
          onClick={() => handlePayment('multicaixa')}
          disabled={loading}
        >
          {loading ? 'Processando...' : 'Pagar com Multicaixa'}
        </button>
        <button
          onClick={() => handlePayment('express')}
          disabled={loading}
        >
          {loading ? 'Processando...' : 'Pagar com Express'}
        </button>
      </div>

      <button onClick={onClose}>Cancelar</button>
    </div>
  );
};
```

### Exemplo 2: FinancialDashboard com API

```typescript
import React, { useEffect, useState } from 'react';
import { invoiceAPI, authAPI, Invoice } from '@/services/apiService';

export const FinancialDashboard: React.FC = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadInvoices = async () => {
      try {
        setLoading(true);
        const user = authAPI.getCurrentUser();
        if (user?.citizen_id) {
          const data = await invoiceAPI.listCitizenInvoices(user.citizen_id);
          setInvoices(data);
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadInvoices();
  }, []);

  const handleDownload = async (invoiceId: string) => {
    try {
      const blob = await invoiceAPI.downloadInvoice(invoiceId, 'pdf');
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `fatura-${invoiceId}.pdf`;
      a.click();
    } catch (err) {
      console.error('Erro ao fazer download:', err);
    }
  };

  if (loading) return <div>Carregando faturas...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="dashboard">
      <h2>Minhas Faturas</h2>
      
      {invoices.length === 0 ? (
        <p>Nenhuma fatura encontrada</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Serviço</th>
              <th>Montante</th>
              <th>Estado</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {invoices.map(invoice => (
              <tr key={invoice.id}>
                <td>{invoice.service_name}</td>
                <td>{invoice.amount} {invoice.currency}</td>
                <td>
                  <span className={`status-${invoice.status}`}>
                    {invoice.status}
                  </span>
                </td>
                <td>
                  <button onClick={() => handleDownload(invoice.id)}>
                    Download
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
```

### Exemplo 3: CitizenPortal com API

```typescript
import React, { useEffect, useState } from 'react';
import { citizenAPI, authAPI, Citizen } from '@/services/apiService';

export const CitizenPortal: React.FC = () => {
  const [profile, setProfile] = useState<Citizen | null>(null);
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('profile');

  useEffect(() => {
    const loadData = async () => {
      try {
        const user = authAPI.getCurrentUser();
        if (user?.citizen_id) {
          const [profileData, eventsData] = await Promise.all([
            citizenAPI.getCitizen(user.citizen_id),
            citizenAPI.getEvents(user.citizen_id),
          ]);
          setProfile(profileData);
          setEvents(eventsData);
        }
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) return <div>Carregando perfil...</div>;

  return (
    <div className="portal">
      {/* Tabs */}
      <div className="tabs">
        <button
          onClick={() => setActiveTab('profile')}
          className={activeTab === 'profile' ? 'active' : ''}
        >
          👤 Perfil
        </button>
        <button
          onClick={() => setActiveTab('events')}
          className={activeTab === 'events' ? 'active' : ''}
        >
          📋 Eventos
        </button>
      </div>

      {/* Content */}
      {activeTab === 'profile' && profile && (
        <div className="profile-section">
          <h3>Meu Perfil</h3>
          <p>Nome: {profile.name}</p>
          <p>Email: {profile.email}</p>
          <p>Telefone: {profile.phone}</p>
          <p>Status: {profile.status}</p>
        </div>
      )}

      {activeTab === 'events' && (
        <div className="events-section">
          <h3>Meus Eventos</h3>
          {events.length === 0 ? (
            <p>Sem eventos registrados</p>
          ) : (
            <ul>
              {events.map((event, idx) => (
                <li key={idx}>
                  {event.type} - {new Date(event.date).toLocaleDateString('pt-PT')}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};
```

---

## 🔒 Segurança

### Token Management

O `apiService` gerencia automaticamente:
- ✅ Armazenamento seguro em localStorage
- ✅ Injeção em headers Authorization
- ✅ Renovação em 401
- ✅ Logout em 403

```typescript
// Verificar autenticação
if (!authAPI.isAuthenticated()) {
  navigate('/login');
}

// Obter user atual
const user = authAPI.getCurrentUser();
if (user.role !== 'ADMIN') {
  // Acesso negado
}
```

### Tratamento de Erros

```typescript
try {
  const invoices = await invoiceAPI.listCitizenInvoices(citizenId);
} catch (error: any) {
  if (error.response?.status === 403) {
    // Acesso negado
  } else if (error.response?.status === 404) {
    // Não encontrado
  } else {
    // Erro genérico
    console.error(error.message);
  }
}
```

---

## 🌍 Endpoints Backend

### Financeiro
- `POST /api/v1/financas/invoices` - Criar fatura
- `GET /api/v1/financas/invoices/{id}` - Obter fatura
- `GET /api/v1/financas/invoices/citizen/{citizenId}` - Listar faturas
- `POST /api/v1/financas/invoices/{id}/cancel` - Cancelar
- `POST /api/v1/financas/payments` - Registar pagamento
- `GET /api/v1/financas/payments/citizen/{citizenId}` - Histórico
- `GET /api/v1/financas/payments/gateway/{ref}` - Consultar por ref

### Cidadão
- `GET /api/v1/identidade-civil/citizens/me` - Perfil atual
- `GET /api/v1/identidade-civil/citizens/{id}` - Obter cidadão
- `GET /api/v1/identidade-civil/citizens/{id}/events` - Eventos
- `PUT /api/v1/identidade-civil/citizens/{id}` - Atualizar

### Autenticação
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Registrar
- `POST /api/auth/logout` - Logout

---

## ✅ Checklist de Integração

- [ ] Importar `apiService` nos componentes
- [ ] Remover chamadas HTTP diretas  
- [ ] Use type hints: `Invoice`, `Payment`, `Citizen`
- [ ] Adicionar loading states
- [ ] Adicionar error handling
- [ ] Testar autenticação (tokens)
- [ ] Testar 403 (acesso negado)
- [ ] Testar 404 (não encontrado)
- [ ] Validar CORS no backend
- [ ] Documentar fluxos no README

---

## 🧪 Teste de Exemplo

```typescript
// Teste básico
import { invoiceAPI, authAPI } from '@/services/apiService';

test('Deve listar faturas do cidadão', async () => {
  // Login
  await authAPI.login('citizen@example.com', 'password');
  const user = authAPI.getCurrentUser();
  
  // Listar
  const invoices = await invoiceAPI.listCitizenInvoices(user.citizen_id);
  
  // Assert
  expect(invoices).toBeInstanceOf(Array);
  expect(invoices.length).toBeGreaterThan(0);
});
```

---

## 📚 Recursos Adicionais

- [Axios Documentation](https://axios-http.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [FastAPI Backend Docs](../../backend/docs/)
- [Environment Variables](../.env.example)

---

**Status**: ✅ Pronto para uso
**Última atualização**: 22 de Fevereiro de 2026
