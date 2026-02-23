"""
QUERIES CONGELADAS - FASE 2 COMPLETA
NÃO MODIFICAR SEM ADR APROVADA

Data Freeze: 2026-02-12
Versão: 1.0.0
Status: PRODUÇÃO
Responsável: Arquitetura SILA

Cada método representa 1 visão administrativa oficial.
Qualquer alteração requer ADR + validação de arquitetura.
"""

from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, case

from app.citizen.core.models import CitizenRequest
from app.core.territory.models.territory import Territory


class FrozenProfileQueries:
    """
    🧊 QUERIES OFICIAIS - PRODUÇÃO
    
    Cada método = 1 visão administrativa
    Qualquer alteração requer ADR e validação de arquitetura
    TIPO: frozen - versão 1.0.0
    """
    
    # ======================================================================
    # PERFIL 1: COMUNA (EXECUÇÃO)
    # ======================================================================
    
    @staticmethod
    def view_commune_active_requests(
        db: Session,
        commune_id: UUID,
        officer_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """
        VISÃO OFICIAL DA COMUNA - EXECUÇÃO
        
        Responsabilidade: Processar pedidos da sua comuna
        - Apenas pedidos NÃO escalados
        - Apenas da sua comuna
        - Ordenados por urgência
        
        CHECK: Nunca retorna dados de outros concelhos
        """
        
        # Base query - FILTRO TERRITORIAL ESTRITO
        base = db.query(CitizenRequest).filter(
            CitizenRequest.commune_id == commune_id,
            CitizenRequest.is_escalated == False,
            CitizenRequest.state.notin_([
                'RESOLVIDO', 'REJEITADO', 'CANCELADO',
                'ESCALADO_MUNICIPIO', 'ESCALADO_PROVINCIA', 'ESCALADO_CENTRAL'
            ])
        )
        
        # Pedidos pendentes (prioridade máxima) - não entregues ao utilizador
        pendentes = base.filter(
            CitizenRequest.state.in_([
                'SUBMETIDO',
                'EM_ANALISE_COMUNAL',
                'AGUARDANDO_CIDADAO_COMUNAL'
            ])
        ).order_by(
            CitizenRequest.created_at.asc()
        ).limit(50).all()
        
        # Pedidos atribuídos ao officer atual (se provided)
        meus = []
        if officer_id:
            meus = db.query(CitizenRequest).filter(
                CitizenRequest.commune_id == commune_id,
                CitizenRequest.assigned_to_id == officer_id,
                CitizenRequest.state.notin_(['RESOLVIDO', 'REJEITADO', 'CANCELADO'])
            ).order_by(
                CitizenRequest.created_at.asc()
            ).all()
        
        # Métricas operacionais de apenas ESTA comuna
        total_ativos = base.count()
        media_dias = db.query(
            func.avg(
                func.extract('epoch', func.now() - CitizenRequest.created_at) / 86400
            )
        ).filter(
            CitizenRequest.commune_id == commune_id,
            CitizenRequest.state.notin_(['RESOLVIDO', 'REJEITADO', 'CANCELADO'])
        ).scalar() or 0
        
        metrics = {
            "total_ativos": total_ativos,
            "pendentes": len(pendentes),
            "atribuidos_a_mim": len(meus),
            "media_dias_abertos": round(float(media_dias), 2)
        }
        
        return {
            "perfil": "COMUNA",
            "territorio_id": str(commune_id),
            "territorio_tipo": "COMMUNE",
            "pedidos_por_processar": [p.__dict__ for p in pendentes],
            "meus_pedidos": [p.__dict__ for p in meus],
            "metricas": metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # ======================================================================
    # PERFIL 2: MUNICÍPIO (SUPERVISÃO)
    # ======================================================================
    
    @staticmethod
    def view_municipality_supervision(
        db: Session,
        municipality_id: UUID
    ) -> Dict[str, Any]:
        """
        VISÃO OFICIAL DO MUNICÍPIO - SUPERVISÃO
        
        Responsabilidade: Supervisionar performance das comunas
        - Pedidos escalados para o município
        - Agregado de performance das comunas (NÃO detalhe)
        - Identificar gargalos
        
        CHECK: Nunca retorna detalhe operacional
        CHECK: Apenas visão agregada por comuna
        """
        
        # 1. Escalados para o município (supervisão de casos críticos)
        escalados = db.query(CitizenRequest).filter(
            CitizenRequest.current_territory_id == municipality_id,
            CitizenRequest.escalation_level == 'municipality',
            CitizenRequest.state.in_([
                'ESCALADO_MUNICIPIO',
                'EM_ANALISE_MUNICIPAL',
                'AGUARDANDO_CIDADAO_MUNICIPAL'
            ])
        ).order_by(
            CitizenRequest.escalated_at.desc()
        ).limit(50).all()
        
        # 2. Encontrar todas as comunas desta localidade
        communes = db.query(Territory).filter(
            Territory.id.in_(
                db.query(CitizenRequest.commune_id).filter(
                    CitizenRequest.municipality_id == municipality_id
                ).distinct()
            )
        ).all()
        
        # 3. Performance de cada comuna (agregado APENAS)
        communes_performance = []
        for commune in communes:
            stats = db.query(
                func.count().label('total'),
                func.sum(
                    case(
                        (CitizenRequest.state.in_(['RESOLVIDO']), 1),
                        else_=0
                    )
                ).label('resolvidos'),
                func.sum(
                    case(
                        (CitizenRequest.is_escalated == True, 1),
                        else_=0
                    )
                ).label('escalados')
            ).filter(
                CitizenRequest.commune_id == commune.id,
                CitizenRequest.state.notin_(['CANCELADO'])
            ).first()
            
            total_reqs = stats.total or 0
            resolvidos = stats.resolvidos or 0
            escalados_cnt = stats.escalados or 0
            
            communes_performance.append({
                "comuna": commune.name,
                "id": str(commune.id),
                "total_pedidos": total_reqs,
                "taxa_resolucao": round(
                    (resolvidos / total_reqs * 100) if total_reqs > 0 else 0,
                    2
                ),
                "taxa_escalamento": round(
                    (escalados_cnt / total_reqs * 100) if total_reqs > 0 else 0,
                    2
                )
            })
        
        return {
            "perfil": "MUNICIPIO",
            "territorio_id": str(municipality_id),
            "territorio_tipo": "MUNICIPALITY",
            "pedidos_escalados_aqui": len(escalados),
            "ultimos_escalados": [e.__dict__ for e in escalados[:10]],
            "performance_comunas": sorted(
                communes_performance,
                key=lambda x: x['taxa_escalamento'],
                reverse=True
            ),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # ======================================================================
    # PERFIL 3: PROVÍNCIA (EXCEÇÕES)
    # ======================================================================
    
    @staticmethod
    def view_province_exceptions(
        db: Session,
        province_id: UUID
    ) -> Dict[str, Any]:
        """
        VISÃO OFICIAL DA PROVÍNCIA - EXCEÇÕES
        
        Responsabilidade: Identificar e resolver casos críticos APENAS
        - Casos escalados para a província
        - Municípios com gargalos críticos
        - NUNCA vê operação normal
        
        CHECK: Apenas exceções, nunca casos normais
        CHECK: Agregado por município, NÃO por comuna
        """
        
        # Casos críticos: escalados para província ou com problemas severos
        casos_criticos = db.query(CitizenRequest).filter(
            CitizenRequest.province_id == province_id,
            or_(
                CitizenRequest.state.in_([
                    'ESCALADO_PROVINCIA',
                    'EM_ANALISE_PROVINCIAL',
                    'AGUARDANDO_CIDADAO_PROVINCIAL'
                ]),
                and_(
                    CitizenRequest.is_escalated == True,
                    CitizenRequest.escalation_level == 'province',
                    CitizenRequest.escalated_at >= datetime.utcnow() - timedelta(days=7)
                )
            )
        ).order_by(
            CitizenRequest.escalated_at.desc().nullslast()
        ).all()
        
        # Encontrar todos os municípios desta província
        municipalities = db.query(Territory).filter(
            Territory.id.in_(
                db.query(CitizenRequest.municipality_id).filter(
                    CitizenRequest.province_id == province_id
                ).distinct()
            )
        ).all()
        
        # Análise de gargalos por município (threshold=5)
        gargalos = []
        for municipality in municipalities:
            escalados_count = db.query(CitizenRequest).filter(
                CitizenRequest.municipality_id == municipality.id,
                CitizenRequest.is_escalated == True,
                CitizenRequest.escalated_at >= datetime.utcnow() - timedelta(days=30)
            ).count()
            
            if escalados_count >= 5:  # Threshold crítico
                gargalos.append({
                    "municipio": municipality.name,
                    "id": str(municipality.id),
                    "escalados_30d": escalados_count,
                    "severidade": "CRÍTICA" if escalados_count >= 10 else "MÉDIA"
                })
        
        return {
            "perfil": "PROVINCIA",
            "territorio_id": str(province_id),
            "territorio_tipo": "PROVINCE",
            "casos_criticos_total": len(casos_criticos),
            "casos_criticos": [c.__dict__ for c in casos_criticos[:20]],
            "gargalos_identificados": gargalos,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # ======================================================================
    # PERFIL 4: CENTRAL (GOVERNANÇA)
    # ======================================================================
    
    @staticmethod
    def view_central_governance(db: Session) -> Dict[str, Any]:
        """
        VISÃO OFICIAL CENTRAL - GOVERNANÇA NACIONAL
        
        Responsabilidade: KPIs e tendências nacionais APENAS
        - Dados agregados (nunca casos individuais)
        - Performance por província
        - Tendências nacionais
        
        CHECK: Nunca retorna detalhes de casos
        CHECK: Apenas métricas agregadas
        """
        
        # KPIs globais
        total = db.query(CitizenRequest).count()
        ativos = db.query(CitizenRequest).filter(
            ~CitizenRequest.state.in_(['RESOLVIDO', 'REJEITADO', 'CANCELADO'])
        ).count()
        resolvidos = db.query(CitizenRequest).filter(
            CitizenRequest.state == 'RESOLVIDO'
        ).count()
        escalados_total = db.query(CitizenRequest).filter(
            CitizenRequest.is_escalated == True
        ).count()
        
        # Tempo médio de resolução
        tempo_medio = db.query(
            func.avg(
                func.extract('epoch', CitizenRequest.resolved_at - CitizenRequest.created_at) / 86400
            )
        ).filter(
            CitizenRequest.state == 'RESOLVIDO',
            CitizenRequest.resolved_at.isnot(None)
        ).scalar() or 0
        
        # Performance por província
        provinces = db.query(Territory).filter(
            Territory.id.in_(
                db.query(CitizenRequest.province_id).distinct()
            )
        ).all()
        
        performance_provincias = []
        for province in provinces:
            prov_reqs = db.query(CitizenRequest).filter(
                CitizenRequest.province_id == province.id
            )
            
            total_prov = prov_reqs.count()
            if total_prov > 0:
                performance_provincias.append({
                    "provincia": province.name,
                    "id": str(province.id),
                    "total": total_prov,
                    "ativos": prov_reqs.filter(
                        ~CitizenRequest.state.in_(['RESOLVIDO', 'REJEITADO', 'CANCELADO'])
                    ).count(),
                    "resolvidos": prov_reqs.filter(CitizenRequest.state == 'RESOLVIDO').count(),
                    "taxa_resolucao": round(
                        prov_reqs.filter(CitizenRequest.state == 'RESOLVIDO').count() / total_prov * 100,
                        2
                    ),
                    "taxa_escalamento": round(
                        prov_reqs.filter(CitizenRequest.is_escalated == True).count() / total_prov * 100,
                        2
                    )
                })
        
        # Tendência últimos 30 dias
        tendencia = db.query(
            func.date(CitizenRequest.created_at).label('dia'),
            func.count().label('total'),
            func.sum(
                case(
                    (CitizenRequest.state == 'RESOLVIDO', 1),
                    else_=0
                )
            ).label('resolvidos')
        ).filter(
            CitizenRequest.created_at >= datetime.utcnow() - timedelta(days=30)
        ).group_by(
            func.date(CitizenRequest.created_at)
        ).order_by(
            func.date(CitizenRequest.created_at)
        ).all()
        
        return {
            "perfil": "CENTRAL",
            "territorio_tipo": "NACIONAL",
            "kpis_nacionais": {
                "total_pedidos": total,
                "pedidos_ativos": ativos,
                "pedidos_resolvidos": resolvidos,
                "taxa_conclusao": round((resolvidos / total * 100), 2) if total > 0 else 0,
                "taxa_escalamento_nacional": round((escalados_total / total * 100), 2) if total > 0 else 0,
                "tempo_medio_resolucao_dias": round(float(tempo_medio), 2)
            },
            "performance_provincias": sorted(
                performance_provincias,
                key=lambda x: x['ativos'],
                reverse=True
            ),
            "tendencia_30d": [
                {
                    "dia": str(d.dia),
                    "pedidos_recebidos": d.total or 0,
                    "pedidos_resolvidos": d.resolvidos or 0
                }
                for d in tendencia
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
