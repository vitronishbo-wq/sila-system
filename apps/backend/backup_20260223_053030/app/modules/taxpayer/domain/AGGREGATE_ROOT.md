"""
AGGREGATE ROOT: Taxpayer

Estrutura de Agregado de Domínio para o módulo Taxpayer.

=== CONCEITO ===

Um AGGREGATE em Domain-Driven Design é um grupo de objetos de domínio
que devem ser tratados como uma unidade atômica para fins de mudança de dados.

No contexto do módulo Taxpayer:

┌─────────────────────────────────────────────────────────┐
│         TAXPAYER (AGGREGATE ROOT)                       │
│                                                         │
│  • ID único (taxpayer_id)                              │
│  • Responsável pela consistência do agregado           │
│  • Ponto de entrada para queries                       │
│  • Gerencia transações                                 │
│                                                         │
│  ├─ TaxDeclaration (VALUE OBJECT/ENTITY)              │
│  │  └─ Dentro do contexto do Taxpayer                 │
│  │                                                    │
│  ├─ TaxDebt (VALUE OBJECT/ENTITY)                     │
│  │  └─ Dentro do contexto do Taxpayer                 │
│  │                                                    │
│  ├─ TaxPayment (VALUE OBJECT/ENTITY)                  │
│  │  └─ Dentro do contexto do Taxpayer                 │
│  │                                                    │
│  └─ TaxCertificate (VALUE OBJECT/ENTITY)              │
│     └─ Dentro do contexto do Taxpayer                 │
│                                                         │
└─────────────────────────────────────────────────────────┘

=== POR QUE TAXPAYER É AGGREGATE ROOT ===

1. IDENTIDADE ÚNICA
   • Cada contribuinte (NIF) é único
   • El é a entidade principal do domínio

2. CONSISTÊNCIA TRANSACIONAL
   • Todas as operações de um contribuinte (registrar, declarar, pagar)
     devem manter a consistência
   • Se uma declaração é rejeitada, afeta débitos potenciais
   • Se um débito é registrado, afeta o status

3. LIMITE DE TRANSAÇÃO
   • Sempre trabalhamos com um Taxpayer como unidade
   • Não queryamos Declarations diretamente
   • Sempre: "Declarations de um Taxpayer"

4. INVARIANTES DE DOMÍNIO
   • Todas as regras de negócio ficam no Taxpayer
   • Ex: "Não pode ter 2 declarations para mesmo período"
   • Ex: "Não pode pagar mais que o débito"

=== ENTIDADES DENTRO DO AGGREGATE ===

NÃO são AGGREGATES separados:

   ❌ get_declaration(id)  -> Errado!
   ✅ taxpayer.get_declaration(id)  -> Correto!

   ❌ update_payment(payment_id, ...)  -> Errado!
   ✅ taxpayer.update_payment(payment_id, ...)  -> Correto!

=== BOUNDARIES (LIMITES) ===

DENTRO DO AGGREGATE (coesão forte):
├─ Taxpayer entity (root)
├─ TaxDeclaration
├─ TaxDebt
├─ TaxPayment
└─ TaxCertificate

FORA DO AGGREGATE (referências por ID):
├─ User agents (referência via user_id)
├─ Organization (se houver, referência via organization_id)
└─ External AGT integration (referência via protocol_number)

=== REPOSITÓRIO ===

Only ONE REPOSITORY:
   
   ✅ TaxpayerRepository::find(taxpayer_id) -> Taxpayer agregado completo

NÃO ter:
   
   ❌ DeclarationRepository
   ❌ DebtRepository  
   ❌ PaymentRepository

Todas as operações passam por Taxpayer:

   ✅ taxpayer.add_declaration(...)
   ✅ taxpayer.add_debt(...)
   ✅ taxpayer.add_payment(...)

=== FACTORY & CREATION ===

Taxpayer é criado através de FACTORY PATTERN:

   class TaxpayerFactory:
       def create(nif, name, ...): -> Taxpayer
       
   # Nunca:
   taxpayer = Taxpayer(...)
   
   # Sempre:
   taxpayer = TaxpayerFactory.create(...)

=== PERSISTÊNCIA ===

O repositório serializa/deserializa o agregado COMPLETO:

   # Salva:
   taxpayer.add_declaration(...)
   repo.save(taxpayer)  # Salva taxpayer + declarations + debts + payments
   
   # Lê:
   taxpayer = repo.find(nif)  # Retorna completo
   taxpayer.declarations  # Acesso via aggregate root

=== EXEMPLOS DE USO CORRETO ===

1. Registrar Contribuinte + Declaração:
   
   taxpayer = TaxpayerFactory.create(nif="123456789", name="João")
   taxpayer.add_declaration(TaxType.IRS, TaxPeriod.from_year(2024), ...)
   taxpayer_repo.save(taxpayer)

2. Adicionar Débito:
   
   taxpayer = taxpayer_repo.find_by_nif("123456789")
   taxpayer.add_debt(debt_number="DEBT-2024-001", amount=1500)
   taxpayer_repo.save(taxpayer)

3. Pagar Imposto:
   
   taxpayer = taxpayer_repo.find_by_nif("123456789")
   payment = taxpayer.pay_debt(debt_id=debt_id, amount=1500)
   taxpayer_repo.save(taxpayer)  # Tudo atomicamente

=== DOMAIN EVENTS ===

São Disparados pelo Aggregate Root:

   taxpayer = TaxpayerFactory.create(...)
   -> disparos: TaxpayerRegistered event
   
   taxpayer.add_declaration(...)
   -> dispara: TaxDeclarationFiled event
   
   taxpayer.add_payment(...)
   -> dispara: TaxPaid event

=== TRANSAÇÕES ===

Toda operação de escrita é ATÔMICA:

   @transaction  # Uma transação = um save()
   def register_taxpayer(...):
       taxpayer = TaxpayerFactory.create(...)
       repo.save(taxpayer)  # Tudo ou nada
       
   NÃO fazer:
   
   taxpayer = TaxpayerFactory.create(...)
   repo.save(taxpayer)
   declaration = TaxDeclaration(...)
   declaration_repo.save(declaration)  # ERRADO! Dois saves = dois problemas

=== INVARIANTES DE DOMÍNIO ===

O Aggregate Root garante:

1. Um NIF não pode ter 2 contribuintes
2. Um Taxpayer não pode ter 2 declarations no mesmo período
3. Um Taxpayer não pode ter débitos negativos
4. Débitos resolvidos não podem voltar ao estado aberto

Estes são VALIDADOS no Taxpayer, não na Application Layer:

   ✅ taxpayer.add_declaration(...)  # Valida aqui
   
   ❌ if taxpayer.declarations_count < max:
        taxpayer.add_declaration(...)

=== CONCLUSÃO ===

Taxpayer é o CORAÇÃO do módulo.

Tudo passa por ele.
Tudo é consistente em relação a ele.
Tudo é persistido com ele.

É o padrão correto para sistemas fiscais com integridade crítica.
"""
