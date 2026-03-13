"""
Observatório Institucional - Dashboard Executivo
=================================================
Dashboard Streamlit para decisores institucionais.
Foco em 30 segundos de leitura com métricas chave e sinais de governança.

Executar: streamlit run institutional_dashboard.py
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
import os
import sys

# Tentar importar ports_config para URL centralizada
try:
    # PYTHONPATH should be configured via setup_dev_env.sh so imports resolve.
    from app.core.ports_config import PortsConfig
    
    # Montar URL base + endpoint
    BASE_URL = PortsConfig.get_api_base_url() + "/observability"
except Exception as e:
    # Fallback: usar variável de ambiente ou padrão Docker
    BASE_URL = os.getenv("BACKEND_URL", "http://backend:8000") + "/observability"

TOKEN = os.getenv("INSTITUTIONAL_TOKEN", "")

st.set_page_config(
    page_title="Observatório Institucional - SILA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para visual institucional
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1e3a5f;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
    }
    .signal-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .signal-success { background-color: #d4edda; border-left: 4px solid #28a745; }
    .signal-warning { background-color: #fff3cd; border-left: 4px solid #ffc107; }
    .signal-danger { background-color: #f8d7da; border-left: 4px solid #dc3545; }
    .signal-info { background-color: #d1ecf1; border-left: 4px solid #17a2b8; }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown('<h1 class="main-header">📊 Observatório Institucional – Piloto Bailundo</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sistema Integrado de Logística Administrativa (SILA) – República de Angola</p>', unsafe_allow_html=True)

# Controles
col_level, col_since, col_until, col_btn = st.columns([2, 2, 2, 1])

with col_level:
    level = st.selectbox(
        "Nível de Observabilidade",
        ["provincia", "nacional"],
        format_func=lambda x: "Provincial" if x == "provincia" else "Nacional"
    )

with col_since:
    since = st.date_input("Desde", datetime.now() - timedelta(days=7))

with col_until:
    until = st.date_input("Até", datetime.now())

with col_btn:
    st.write("")  # Espaçador
    st.write("")
    refresh = st.button("🔄 Atualizar", use_container_width=True)

st.divider()

# Buscar dados
def fetch_data():
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    params = {
        "level": level,
        "since": since.isoformat(),
        "until": until.isoformat()
    }
    try:
        r = requests.get(f"{BASE_URL}/territorial", params=params, headers=headers, timeout=30)
        if r.status_code == 200:
            return r.json(), None
        else:
            return None, f"Erro {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return None, str(e)

if refresh or "data" not in st.session_state:
    data, error = fetch_data()
    if data:
        st.session_state.data = data
        st.session_state.error = None
    else:
        st.session_state.data = None
        st.session_state.error = error

# Exibir dados
if st.session_state.get("data"):
    data = st.session_state.data
    m = data.get("metrics", {})
    s = data.get("signals", {})
    
    # Métricas principais - 6 colunas
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric(
            "⏱️ Tempo Médio",
            f"{m.get('mean_processing_time', 0):.2f}s",
            help="Tempo médio de processamento de documentos"
        )
    
    with col2:
        p95 = m.get('p95_processing_time', 0)
        st.metric(
            "📉 P95 Tempo",
            f"{p95:.2f}s",
            delta="⚠️ SLA" if p95 > 5 else None,
            delta_color="inverse"
        )
    
    with col3:
        approval = m.get('approval_rate', 0) * 100
        st.metric(
            "✅ Taxa Aprovação",
            f"{approval:.1f}%",
            help="Percentagem de documentos aprovados"
        )
    
    with col4:
        rejection = m.get('rejection_rate', 0) * 100
        st.metric(
            "❌ Taxa Rejeição",
            f"{rejection:.1f}%"
        )
    
    with col5:
        blocked = int(m.get('blocked_actions_count', 0))
        st.metric(
            "⛔ Bloqueios RBAC",
            blocked,
            delta="🚨" if blocked > 0 else None,
            delta_color="inverse"
        )
    
    with col6:
        docs_comuna = m.get('documents_per_comuna', 0)
        st.metric(
            "📄 Docs/Comuna",
            f"{docs_comuna:.1f}",
            help="Média de documentos por comuna"
        )
    
    st.divider()
    
    # Sinais de Governança
    st.subheader("🏛️ Sinais de Governança")
    
    col_signals, col_summary = st.columns([2, 1])
    
    with col_signals:
        if s.get("blocked_detected"):
            st.error("🚫 **Violação potencial de governação detectada** – Bloqueios RBAC registados. Auditoria recomendada.")
        
        if s.get("sla_breach"):
            st.warning("⚠️ **Compromisso de SLA em risco** – P95 acima de 5 segundos. Verificar comunas afectadas e recursos locais.")
        
        if s.get("low_activity"):
            st.info("ℹ️ **Atividade abaixo do esperado** – Menos de 10 documentos por comuna. Possível necessidade de formação local.")
        
        if not any(s.values()):
            st.success("✅ **Sistema estável e conforme** – Todos os indicadores dentro dos parâmetros. Pronto para avaliação de escala.")
    
    with col_summary:
        st.markdown("### Resumo Executivo")
        total = m.get('total_documents', 0)
        st.markdown(f"**Total de documentos:** {total:,}")
        st.markdown(f"**Nível:** {level.title()}")
        st.markdown(f"**Período:** {since} a {until}")
    
    st.divider()
    
    # Rodapé institucional
    st.caption(
        f"Dados derivados de logs auditáveis. Observabilidade territorial independente de operações executivas. "
        f"Última atualização: {data.get('last_update', 'N/A')}"
    )

elif st.session_state.get("error"):
    st.error(f"❌ Erro institucional: {st.session_state.error}")
    st.info("Verifique a conexão com o backend ou contacte o suporte técnico governamental.")

else:
    st.info("👆 Clique em 'Atualizar' para carregar os dados de observabilidade.")

# Sidebar com informações adicionais
with st.sidebar:
    st.markdown("### ℹ️ Sobre")
    st.markdown("""
    Este dashboard apresenta métricas de observabilidade
    territorial para apoio à decisão institucional.
    
    **Critérios de Escala:**
    - SLA: P95 ≤ 5 segundos
    - Bloqueios RBAC: 0
    - Atividade mínima: 10 docs/comuna
    - Aprovação: ≥ 80%
    """)
    
    st.markdown("---")
    st.markdown("**SILA** - Sistema Integrado de Logística Administrativa")
    st.markdown("República de Angola")
