"""Institutional catalog blueprint for large-scale service seeding."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ModuleBlueprint:
    slug: str
    title: str
    description: str
    is_foundational: bool
    focus_terms: tuple[str, ...]


@dataclass(frozen=True)
class ServiceBlueprint:
    code: str
    module_slug: str
    name: str
    description: str
    fee: Decimal
    sla_days: int
    workflow_template: str
    required_documents: tuple[str, ...]
    visibility: str
    is_essential: bool
    business_priority: int


ESSENTIAL_MODULE_SLUGS = {
    "identity",
    "saude",
    "educacao",
    "seguranca-social",
    "financas-impostos",
    "registo-civil",
    "justica",
    "emprego",
    "transportes",
    "habitacao",
    "migracao",
    "apoio-empresarial",
    "agricultura",
}

MODULE_BLUEPRINTS: tuple[ModuleBlueprint, ...] = (
    ModuleBlueprint(
        slug="identity",
        title="Identificacao Civil",
        description="Servicos de identificacao do cidadao.",
        is_foundational=True,
        focus_terms=("bilhete de identidade", "nif", "residencia", "alteracao de dados"),
    ),
    ModuleBlueprint(
        slug="saude",
        title="Saude",
        description="Servicos de saude primaria, preventiva e hospitalar.",
        is_foundational=True,
        focus_terms=("consulta clinica", "vacinacao", "registo medico", "referencia hospitalar"),
    ),
    ModuleBlueprint(
        slug="educacao",
        title="Educacao",
        description="Servicos de matricula, validacao e historico escolar.",
        is_foundational=True,
        focus_terms=(
            "matricula escolar",
            "certificado escolar",
            "historico escolar",
            "bolsa de estudo",
        ),
    ),
    ModuleBlueprint(
        slug="seguranca-social",
        title="Seguranca Social",
        description="Prestacoes, contribuicoes e protecao social.",
        is_foundational=True,
        focus_terms=(
            "inscricao contributiva",
            "subsidio familiar",
            "pensao social",
            "prova de vida",
        ),
    ),
    ModuleBlueprint(
        slug="financas-impostos",
        title="Financas e Impostos",
        description="Gestao fiscal, cobranca e regularizacao tributaria.",
        is_foundational=True,
        focus_terms=(
            "declaracao fiscal",
            "certidao tributaria",
            "pagamento de imposto",
            "regularizacao fiscal",
        ),
    ),
    ModuleBlueprint(
        slug="registo-civil",
        title="Registo Civil",
        description="Registos vitais de nascimento, casamento e obito.",
        is_foundational=True,
        focus_terms=(
            "certidao de nascimento",
            "certidao de casamento",
            "certidao de obito",
            "averbamento",
        ),
    ),
    ModuleBlueprint(
        slug="justica",
        title="Justica",
        description="Servicos judiciais e administrativos de justica.",
        is_foundational=True,
        focus_terms=(
            "certificado criminal",
            "processo judicial",
            "mediacao",
            "reconhecimento de firma",
        ),
    ),
    ModuleBlueprint(
        slug="emprego",
        title="Emprego",
        description="Intermediacao laboral e programas de emprego.",
        is_foundational=True,
        focus_terms=(
            "inscricao de emprego",
            "candidatura a vaga",
            "declaracao de desemprego",
            "estagio profissional",
        ),
    ),
    ModuleBlueprint(
        slug="transportes",
        title="Transportes",
        description="Licenciamento, autorizacao e mobilidade publica.",
        is_foundational=True,
        focus_terms=(
            "licenca de conducao",
            "inspecao veicular",
            "titulo de transporte",
            "autorizacao de rota",
        ),
    ),
    ModuleBlueprint(
        slug="habitacao",
        title="Habitacao",
        description="Acesso habitacional, regularizacao e apoio social.",
        is_foundational=True,
        focus_terms=(
            "candidatura habitacional",
            "regularizacao predial",
            "subsidio de renda",
            "vistoria tecnica",
        ),
    ),
    ModuleBlueprint(
        slug="migracao",
        title="Migracao",
        description="Servicos de vistos, residencia e mobilidade migratoria.",
        is_foundational=True,
        focus_terms=(
            "visto",
            "residencia temporaria",
            "residencia permanente",
            "renovacao migratoria",
        ),
    ),
    ModuleBlueprint(
        slug="apoio-empresarial",
        title="Apoio Empresarial",
        description="Abertura, licenciamento e suporte ao setor empresarial.",
        is_foundational=True,
        focus_terms=(
            "abertura de empresa",
            "licenca comercial",
            "certificacao empresarial",
            "alteracao societaria",
        ),
    ),
    ModuleBlueprint(
        slug="agricultura",
        title="Agricultura",
        description="Servicos de apoio tecnico, credito e extensao rural.",
        is_foundational=True,
        focus_terms=(
            "registro agricola",
            "assistencia tecnica",
            "credito rural",
            "certificacao fitossanitaria",
        ),
    ),
    ModuleBlueprint(
        slug="cultura",
        title="Cultura",
        description="Incentivos, registros e programas culturais.",
        is_foundational=False,
        focus_terms=(
            "apoio cultural",
            "registro artistico",
            "licenca de evento",
            "fomento cultural",
        ),
    ),
    ModuleBlueprint(
        slug="turismo",
        title="Turismo",
        description="Licenciamento e promocao do setor turistico.",
        is_foundational=False,
        focus_terms=(
            "registro turistico",
            "licenca turistica",
            "certificacao de guia",
            "promocao de destino",
        ),
    ),
    ModuleBlueprint(
        slug="ambiente",
        title="Ambiente",
        description="Licenciamento ambiental e monitoramento ecologico.",
        is_foundational=False,
        focus_terms=(
            "licenca ambiental",
            "avaliacao de impacto",
            "monitoramento ambiental",
            "gestao de residuos",
        ),
    ),
    ModuleBlueprint(
        slug="energia",
        title="Energia",
        description="Conexao, regularizacao e fiscalizacao energetica.",
        is_foundational=False,
        focus_terms=(
            "ligacao eletrica",
            "regularizacao energetica",
            "inspecao eletrica",
            "tarifa social",
        ),
    ),
    ModuleBlueprint(
        slug="urbanismo",
        title="Urbanismo",
        description="Planeamento urbano e licenciamento territorial.",
        is_foundational=False,
        focus_terms=(
            "licenca de construcao",
            "alvara urbano",
            "consulta urbanistica",
            "uso do solo",
        ),
    ),
    ModuleBlueprint(
        slug="comercio",
        title="Comercio",
        description="Regulacao comercial e autorizacoes economicas.",
        is_foundational=False,
        focus_terms=(
            "registro comercial",
            "autorizacao comercial",
            "fiscalizacao comercial",
            "certificado de origem",
        ),
    ),
    ModuleBlueprint(
        slug="industria",
        title="Industria",
        description="Licenciamento industrial e controle de qualidade.",
        is_foundational=False,
        focus_terms=(
            "licenca industrial",
            "inspecao industrial",
            "certificacao industrial",
            "plano produtivo",
        ),
    ),
    ModuleBlueprint(
        slug="pescas",
        title="Pescas",
        description="Licenciamento e gestao de atividades pesqueiras.",
        is_foundational=False,
        focus_terms=(
            "licenca de pesca",
            "autorizacao de captura",
            "registro pesqueiro",
            "controle de frota",
        ),
    ),
    ModuleBlueprint(
        slug="desporto",
        title="Desporto",
        description="Registros federativos e apoio desportivo.",
        is_foundational=False,
        focus_terms=(
            "registro de atleta",
            "apoio desportivo",
            "licenca de evento desportivo",
            "certificacao tecnica",
        ),
    ),
    ModuleBlueprint(
        slug="juventude",
        title="Juventude",
        description="Programas de capacitacao e inclusao juvenil.",
        is_foundational=False,
        focus_terms=(
            "programa juvenil",
            "bolsa juvenil",
            "capacitacao juvenil",
            "empreendedorismo juvenil",
        ),
    ),
    ModuleBlueprint(
        slug="familia",
        title="Familia",
        description="Servicos de apoio e protecao familiar.",
        is_foundational=False,
        focus_terms=(
            "apoio familiar",
            "mediacao familiar",
            "assistencia parental",
            "registro familiar",
        ),
    ),
    ModuleBlueprint(
        slug="igualdade",
        title="Igualdade",
        description="Promocao da igualdade e nao discriminacao.",
        is_foundational=False,
        focus_terms=(
            "apoio a igualdade",
            "protecao contra discriminacao",
            "orientacao juridica",
            "programa inclusivo",
        ),
    ),
    ModuleBlueprint(
        slug="protecao-civil",
        title="Protecao Civil",
        description="Prevencao, resposta e recuperacao de emergencias.",
        is_foundational=False,
        focus_terms=(
            "plano de emergencia",
            "aviso de risco",
            "apoio pos desastre",
            "certificacao de brigada",
        ),
    ),
    ModuleBlueprint(
        slug="estatistica",
        title="Estatistica",
        description="Coleta, validacao e divulgacao estatistica.",
        is_foundational=False,
        focus_terms=(
            "pedido estatistico",
            "dados oficiais",
            "certidao estatistica",
            "painel de indicadores",
        ),
    ),
    ModuleBlueprint(
        slug="administracao-local",
        title="Administracao Local",
        description="Servicos locais de atendimento e governanca territorial.",
        is_foundational=False,
        focus_terms=(
            "atendimento local",
            "licenca local",
            "certidao local",
            "participacao comunitaria",
        ),
    ),
    ModuleBlueprint(
        slug="aguas-saneamento",
        title="Aguas e Saneamento",
        description="Ligacao, manutencao e qualidade de agua e saneamento.",
        is_foundational=False,
        focus_terms=(
            "ligacao de agua",
            "saneamento basico",
            "inspecao hidrica",
            "tarifa social de agua",
        ),
    ),
    ModuleBlueprint(
        slug="telecomunicacoes",
        title="Telecomunicacoes",
        description="Licenciamento e regulacao de telecomunicacoes.",
        is_foundational=False,
        focus_terms=(
            "registro de operadora",
            "licenca de frequencia",
            "homologacao de equipamento",
            "certificacao digital",
        ),
    ),
    ModuleBlueprint(
        slug="tecnologia-inovacao",
        title="Tecnologia e Inovacao",
        description="Programas tecnologicos e suporte a inovacao.",
        is_foundational=False,
        focus_terms=(
            "inovacao tecnologica",
            "aceleracao digital",
            "apoio a startup",
            "laboratorio de inovacao",
        ),
    ),
    ModuleBlueprint(
        slug="trabalho-inspecao",
        title="Trabalho e Inspecao",
        description="Inspecao laboral, relacoes de trabalho e seguranca ocupacional.",
        is_foundational=False,
        focus_terms=(
            "inspecao laboral",
            "mediacao laboral",
            "seguranca ocupacional",
            "registro de contrato",
        ),
    ),
    ModuleBlueprint(
        slug="planeamento",
        title="Planeamento",
        description="Planeamento publico, projetos e execucao setorial.",
        is_foundational=False,
        focus_terms=(
            "plano setorial",
            "aprovacao de projeto",
            "monitoramento de meta",
            "priorizacao publica",
        ),
    ),
    ModuleBlueprint(
        slug="obras-publicas",
        title="Obras Publicas",
        description="Gestao de obras, contratos e fiscalizacao.",
        is_foundational=False,
        focus_terms=(
            "licenca de obra",
            "fiscalizacao de obra",
            "medicao de obra",
            "recebimento provisiorio",
        ),
    ),
    ModuleBlueprint(
        slug="recursos-minerais",
        title="Recursos Minerais",
        description="Autorizacao e monitoramento da atividade mineira.",
        is_foundational=False,
        focus_terms=(
            "prospeccao mineral",
            "licenca mineira",
            "relatorio geologico",
            "fiscalizacao mineira",
        ),
    ),
    ModuleBlueprint(
        slug="petroleo-gas",
        title="Petroleo e Gas",
        description="Regulacao, autorizacao e compliance de hidrocarbonetos.",
        is_foundational=False,
        focus_terms=(
            "autorizacao petrolifera",
            "licenca de gas",
            "inspecao de instalacao",
            "relatorio operacional",
        ),
    ),
    ModuleBlueprint(
        slug="florestas",
        title="Florestas",
        description="Gestao de recursos florestais e autorizacoes associadas.",
        is_foundational=False,
        focus_terms=(
            "licenca florestal",
            "reflorestamento",
            "aproveitamento florestal",
            "controle de desmatamento",
        ),
    ),
    ModuleBlueprint(
        slug="pecuaria",
        title="Pecuaria",
        description="Registro e controle sanitario animal.",
        is_foundational=False,
        focus_terms=(
            "registro pecuario",
            "vacinacao animal",
            "guia de transito animal",
            "controle veterinario",
        ),
    ),
    ModuleBlueprint(
        slug="cooperacao-internacional",
        title="Cooperacao Internacional",
        description="Gestao de programas e acordos internacionais.",
        is_foundational=False,
        focus_terms=(
            "acordo internacional",
            "registro de projeto internacional",
            "assistencia tecnica externa",
            "vistoria de convenio",
        ),
    ),
    ModuleBlueprint(
        slug="defesa-consumidor",
        title="Defesa do Consumidor",
        description="Protecao de direitos do consumidor e fiscalizacao.",
        is_foundational=False,
        focus_terms=(
            "reclamacao de consumo",
            "mediacao de consumo",
            "fiscalizacao de mercado",
            "alerta de produto",
        ),
    ),
    ModuleBlueprint(
        slug="seguranca-publica",
        title="Seguranca Publica",
        description="Servicos de seguranca, registo e controle publico.",
        is_foundational=False,
        focus_terms=(
            "registro de ocorrencia",
            "autorizacao de evento",
            "certidao policial",
            "plano de seguranca",
        ),
    ),
    ModuleBlueprint(
        slug="protecao-dados",
        title="Protecao de Dados",
        description="Conformidade e atendimento de direitos de dados pessoais.",
        is_foundational=False,
        focus_terms=(
            "direito de acesso a dados",
            "retificacao de dados",
            "portabilidade de dados",
            "notificacao de incidente",
        ),
    ),
    ModuleBlueprint(
        slug="arquivo-nacional",
        title="Arquivo Nacional",
        description="Conservacao, consulta e certificacao documental.",
        is_foundational=False,
        focus_terms=(
            "consulta de arquivo",
            "certidao documental",
            "digitalizacao de acervo",
            "preservacao historica",
        ),
    ),
    ModuleBlueprint(
        slug="patrimonio-cultural",
        title="Patrimonio Cultural",
        description="Registro e protecao de bens culturais.",
        is_foundational=False,
        focus_terms=(
            "registro de patrimonio",
            "autorizacao de restauro",
            "inventario cultural",
            "certificacao patrimonial",
        ),
    ),
    ModuleBlueprint(
        slug="ciencia-pesquisa",
        title="Ciencia e Pesquisa",
        description="Fomento cientifico e suporte a investigacao.",
        is_foundational=False,
        focus_terms=(
            "submissao cientifica",
            "financiamento de pesquisa",
            "parecer etico",
            "registro de laboratorio",
        ),
    ),
    ModuleBlueprint(
        slug="meteorologia",
        title="Meteorologia",
        description="Previsao, alerta e dados climaticos oficiais.",
        is_foundational=False,
        focus_terms=(
            "boletim meteorologico",
            "alerta climatico",
            "historico pluviometrico",
            "dados climaticos",
        ),
    ),
    ModuleBlueprint(
        slug="aviacao-civil",
        title="Aviacao Civil",
        description="Licenciamento aeronautico e seguranca operacional.",
        is_foundational=False,
        focus_terms=(
            "licenca aeronautica",
            "certificacao de aeronave",
            "plano de voo",
            "inspecao aeroportuaria",
        ),
    ),
    ModuleBlueprint(
        slug="portos-logistica",
        title="Portos e Logistica",
        description="Gestao portuaria e autorizacoes logisticas.",
        is_foundational=False,
        focus_terms=(
            "autorizacao portuaria",
            "controle de carga",
            "registro logistico",
            "inspecao de terminal",
        ),
    ),
    ModuleBlueprint(
        slug="comercio-externo",
        title="Comercio Externo",
        description="Licenciamento e controle de importacao e exportacao.",
        is_foundational=False,
        focus_terms=(
            "licenca de importacao",
            "licenca de exportacao",
            "certificado de origem",
            "despacho aduaneiro",
        ),
    ),
    ModuleBlueprint(
        slug="pescas-industriais",
        title="Pescas Industriais",
        description="Regulacao de atividade pesqueira industrial.",
        is_foundational=False,
        focus_terms=(
            "licenca industrial de pesca",
            "monitoramento de frota",
            "quota de captura",
            "inspecao maritima",
        ),
    ),
    ModuleBlueprint(
        slug="gestao-fundiaria",
        title="Gestao Fundiaria",
        description="Cadastro e regularizacao de terras.",
        is_foundational=False,
        focus_terms=(
            "registro fundiario",
            "regularizacao de posse",
            "georreferenciamento",
            "certidao fundiaria",
        ),
    ),
    ModuleBlueprint(
        slug="assistencia-social",
        title="Assistencia Social",
        description="Programas sociais e protecao de grupos vulneraveis.",
        is_foundational=False,
        focus_terms=(
            "subsidio social",
            "cadastro social",
            "acompanhamento social",
            "beneficio eventual",
        ),
    ),
    ModuleBlueprint(
        slug="seguranca-alimentar",
        title="Seguranca Alimentar",
        description="Controle de qualidade e abastecimento alimentar.",
        is_foundational=False,
        focus_terms=(
            "certificacao alimentar",
            "inspecao sanitaria alimentar",
            "monitoramento de estoque",
            "alerta de seguranca alimentar",
        ),
    ),
)
ACTION_VARIANTS = (
    "Emissao",
    "Renovacao",
    "Segunda via",
    "Atualizacao cadastral",
    "Licenciamento",
    "Agendamento",
    "Consulta",
    "Declaracao",
    "Certificacao",
    "Pagamento",
    "Revalidacao",
    "Cancelamento",
)
QUALIFIERS = ("padrao", "urgente", "programado")

EDUCACAO_CANONICAL_SERVICES: tuple[tuple[str, str, int, Decimal, tuple[str, ...]], ...] = (
    (
        "Nova Matricula Escolar",
        "Pedido orientado ao cidadao para matricular estudante na educacao basica.",
        5,
        Decimal("0.00"),
        (
            "bi_estudante",
            "bi_encarregado",
            "fotografia",
            "certificado_anterior",
            "boletim_anterior",
        ),
    ),
    (
        "Renovacao de Matricula Escolar",
        "Renovacao anual da matricula escolar existente.",
        3,
        Decimal("0.00"),
        ("bi_estudante", "comprovativo_matricula", "boletim_anterior"),
    ),
    (
        "Transferencia Escolar",
        "Transferencia de estudante entre escolas com validacao de vaga.",
        7,
        Decimal("0.00"),
        ("bi_estudante", "declaracao_transferencia", "boletim_anterior"),
    ),
    (
        "Consultar Matricula",
        "Consulta do estado e dados essenciais da matricula escolar.",
        1,
        Decimal("0.00"),
        ("bi_estudante",),
    ),
    (
        "Consultar Historico Escolar",
        "Consulta do percurso escolar e resultados academicos do estudante.",
        1,
        Decimal("0.00"),
        ("bi_estudante",),
    ),
    (
        "Declaracao Escolar",
        "Emissao de declaracao de frequencia ou situacao escolar.",
        2,
        Decimal("500.00"),
        ("bi_estudante", "comprovativo_matricula"),
    ),
    (
        "Certificado Escolar",
        "Pedido de certificado escolar ou certificado de conclusao.",
        5,
        Decimal("1000.00"),
        ("bi_estudante", "comprovativo_matricula"),
    ),
    (
        "Segunda Via de Documento Escolar",
        "Emissao de segunda via de documento escolar ja existente.",
        3,
        Decimal("750.00"),
        ("bi_estudante", "declaracao_perda_ou_dano"),
    ),
    (
        "Inscricao em Curso Tecnico",
        "Inscricao de candidato em curso tecnico-profissional.",
        7,
        Decimal("0.00"),
        ("bi_candidato", "certificado_anterior", "fotografia"),
    ),
    (
        "Transferencia Tecnica",
        "Transferencia de estudante entre cursos ou instituicoes tecnicas.",
        7,
        Decimal("0.00"),
        ("bi_estudante", "historico_tecnico", "declaracao_transferencia"),
    ),
    (
        "Certificacao Profissional",
        "Certificacao de competencias ou conclusao profissional.",
        10,
        Decimal("1500.00"),
        ("bi_candidato", "comprovativos_formacao"),
    ),
    (
        "Candidatura Universitaria",
        "Candidatura de ingresso no ensino superior.",
        10,
        Decimal("0.00"),
        ("bi_candidato", "certificado_medio", "fotografia"),
    ),
    (
        "Matricula Universitaria",
        "Matricula de estudante admitido no ensino superior.",
        7,
        Decimal("0.00"),
        ("bi_estudante", "comprovativo_admissao", "certificado_medio"),
    ),
    (
        "Transferencia Universitaria",
        "Transferencia entre instituicoes ou cursos do ensino superior.",
        12,
        Decimal("0.00"),
        ("bi_estudante", "historico_universitario", "plano_curricular"),
    ),
    (
        "Mobilidade Academica",
        "Pedido de mobilidade academica nacional ou internacional.",
        12,
        Decimal("0.00"),
        ("bi_estudante", "historico_universitario", "carta_aceitacao"),
    ),
    (
        "Reconhecimento de Diploma",
        "Reconhecimento administrativo de diploma academico.",
        20,
        Decimal("2500.00"),
        ("bi_requerente", "diploma", "historico_academico"),
    ),
    (
        "Reconhecimento de Grau",
        "Reconhecimento de grau academico obtido noutra instituicao.",
        20,
        Decimal("2500.00"),
        ("bi_requerente", "diploma", "historico_academico"),
    ),
    (
        "Certificado Universitario",
        "Pedido de certificado, declaracao ou comprovativo universitario.",
        5,
        Decimal("1500.00"),
        ("bi_estudante", "comprovativo_matricula"),
    ),
    (
        "Candidatura a Bolsa",
        "Submissao de candidatura a bolsa de estudo.",
        15,
        Decimal("0.00"),
        ("bi_candidato", "comprovativo_rendimento", "certificado_anterior"),
    ),
    (
        "Renovacao de Bolsa",
        "Renovacao de bolsa de estudo ativa.",
        10,
        Decimal("0.00"),
        ("bi_bolseiro", "comprovativo_aproveitamento", "declaracao_matricula"),
    ),
    (
        "Consulta de Bolsa",
        "Consulta do estado de candidatura ou renovacao de bolsa.",
        1,
        Decimal("0.00"),
        ("bi_candidato",),
    ),
    (
        "Inscricao em Formacao",
        "Inscricao em programa de formacao profissional.",
        5,
        Decimal("0.00"),
        ("bi_candidato", "certificado_anterior"),
    ),
    (
        "Consulta de Formacao",
        "Consulta de programas, vagas e inscricoes em formacao.",
        1,
        Decimal("0.00"),
        ("bi_candidato",),
    ),
    (
        "Estagio",
        "Pedido ou candidatura a estagio academico ou profissional.",
        10,
        Decimal("0.00"),
        ("bi_candidato", "curriculum", "comprovativo_formacao"),
    ),
    (
        "Intermediacao de Emprego",
        "Encaminhamento para oportunidades de emprego associadas a formacao.",
        7,
        Decimal("0.00"),
        ("bi_candidato", "curriculum", "certificados"),
    ),
)


def build_service_blueprints(target_count: int = 900) -> tuple[ServiceBlueprint, ...]:
    """Generate institutional service blueprints as data (not controllers)."""
    if target_count < len(MODULE_BLUEPRINTS):
        raise ValueError("target_count must be at least the number of modules")
    module_count = len(MODULE_BLUEPRINTS)
    base_per_module = target_count // module_count
    remainder = target_count % module_count
    blueprints: list[ServiceBlueprint] = []
    for module_index, module in enumerate(MODULE_BLUEPRINTS):
        per_module = base_per_module + (1 if module_index < remainder else 0)
        if module.slug == "educacao":
            for local_idx, (name, description, sla_days, fee, documents) in enumerate(
                EDUCACAO_CANONICAL_SERVICES
            ):
                blueprints.append(
                    ServiceBlueprint(
                        code=f"EDUCACAO_{local_idx + 1:03d}",
                        module_slug=module.slug,
                        name=name,
                        description=description,
                        fee=fee,
                        sla_days=sla_days,
                        workflow_template="educacao.canonical.v1",
                        required_documents=documents,
                        visibility="PUBLIC",
                        is_essential=local_idx < 8,
                        business_priority=1 + local_idx,
                    )
                )
            continue
        for local_idx in range(per_module):
            action = ACTION_VARIANTS[local_idx % len(ACTION_VARIANTS)]
            focus = module.focus_terms[local_idx // len(ACTION_VARIANTS) % len(module.focus_terms)]
            qualifier = QUALIFIERS[
                local_idx // (len(ACTION_VARIANTS) * len(module.focus_terms)) % len(QUALIFIERS)
            ]
            service_name = f"{action} de {focus}"
            if qualifier != "padrao":
                service_name = f"{service_name} - {qualifier}"
            is_essential = module.slug in ESSENTIAL_MODULE_SLUGS and local_idx < 10
            visibility = "INTERNAL" if local_idx % 11 == 0 else "PUBLIC"
            fee = _estimate_fee(module.slug, local_idx, is_essential)
            sla_days = 2 + local_idx % 15
            code = f"{module.slug.upper().replace('-', '_')}_{local_idx + 1:03d}"
            description = (
                f"{module.title}: {service_name.lower()} com fluxo institucional completo, "
                "rastreabilidade e auditoria."
            )
            blueprints.append(
                ServiceBlueprint(
                    code=code,
                    module_slug=module.slug,
                    name=service_name,
                    description=description,
                    fee=fee,
                    sla_days=sla_days,
                    workflow_template=f"{module.slug}.standard.v1",
                    required_documents=_required_documents(module.slug, local_idx),
                    visibility=visibility,
                    is_essential=is_essential,
                    business_priority=1 + local_idx
                    if module.slug in ESSENTIAL_MODULE_SLUGS
                    else 50 + local_idx,
                )
            )
    return tuple(blueprints)


def _estimate_fee(module_slug: str, index: int, is_essential: bool) -> Decimal:
    if "assistencia-social" in module_slug:
        return Decimal("0.00")
    base = Decimal("500.00") if is_essential else Decimal("1200.00")
    multiplier = Decimal(index % 9) * Decimal("250.00")
    return base + multiplier


def _required_documents(module_slug: str, index: int) -> tuple[str, ...]:
    core_docs = ("bi", "nif")
    if module_slug in {"migracao", "aviacao-civil"}:
        return (*core_docs, "comprovativo_residencia", "foto_passaporte")
    if module_slug in {"financas-impostos", "apoio-empresarial", "comercio-externo"}:
        return (*core_docs, "comprovativo_pagamento", "declaracao_assinada")
    if module_slug in {"saude", "assistencia-social", "seguranca-social"}:
        return (*core_docs, "comprovativo_morada", "declaracao_social")
    if index % 7 == 0:
        return (*core_docs, "comprovativo_pagamento")
    return core_docs
