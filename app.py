"""
app.py — Data Lake ANS · Beneficiários de Saúde Suplementar · Alagoas
Lê Parquets diretamente do bucket OCI público — sem Snowflake.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.conexao import query

st.set_page_config(
    page_title="Data Lake ANS · Alagoas",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
.kpi-card {
    background: linear-gradient(160deg, #0f1620, #131c28);
    border: 1px solid #1f2d3d; border-radius: 14px;
    padding: 1.4rem 1.5rem; text-align: center;
    transition: border-color .3s;
}
.kpi-card:hover { border-color: #3dd6c4; }
.kpi-value { font-size: 2.1rem; font-weight: 700; color: #3dd6c4; line-height: 1; margin-bottom: .3rem; }
.kpi-label { font-size: .78rem; color: #8da2b8; font-weight: 300; letter-spacing: .04em; text-transform: uppercase; }
.section-title { font-size: 1.1rem; font-weight: 600; color: #e8eef5;
    margin: 1.8rem 0 .8rem; padding-bottom: .4rem; border-bottom: 1px solid #1f2d3d; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏥 Data Lake ANS")
    st.markdown("""
    <div style='font-size:.85rem;color:#8da2b8;line-height:1.7'>
    Beneficiários de saúde suplementar<br>
    do estado de <b style='color:#e8eef5'>Alagoas</b>.<br><br>
    Pipeline de dados sobre<br>
    <b style='color:#3dd6c4'>OCI</b> + <b style='color:#3dd6c4'>Snowflake</b>.
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div style='font-size:.72rem;color:#5a7088;font-family:JetBrains Mono,monospace;line-height:1.8'>
    Fonte: ANS Dados Abertos<br>
    Camada: Gold → Parquet OCI<br>
    Período: 2019-04 → 2026-04<br>
    Atualização: mensal
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.page_link("pages/01_analise.py",    label="📊 Análise Detalhada")
    st.page_link("pages/02_operadoras.py", label="🏢 Operadoras")
    st.page_link("pages/03_perfil.py",     label="👥 Perfil dos Beneficiários")
    st.page_link("pages/04_glossario.py",  label="📋 Glossário de Indicadores")
    st.page_link("pages/05_governanca.py", label="🔍 Governança Técnica")

# ------------------------------------------------------------------
# Cabeçalho
# ------------------------------------------------------------------
st.markdown("""
<div style='margin-bottom:1.6rem'>
    <div style='font-family:JetBrains Mono,monospace;font-size:.7rem;
                color:#3dd6c4;letter-spacing:.3em;text-transform:uppercase;margin-bottom:.5rem'>
        ◆ Data Lake · Alagoas · ANS
    </div>
    <h1 style='font-size:2rem;font-weight:700;color:#e8eef5;margin:0;line-height:1.1'>
        Beneficiários de Saúde Suplementar
    </h1>
    <p style='color:#8da2b8;font-size:.95rem;font-weight:300;margin-top:.4rem'>
        Visão geral · Competências 2019-04 até 2026-04 · Estado de Alagoas
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Carrega dados
# ------------------------------------------------------------------
with st.spinner("Carregando dados..."):
    df_resumo   = query("resumo_geral")
    df_evolucao = query("evolucao_mensal")

if df_resumo.empty:
    st.error("Não foi possível carregar os dados do bucket OCI.")
    st.stop()

r = df_resumo.iloc[0]

# ------------------------------------------------------------------
# KPIs
# ------------------------------------------------------------------
def fmt(n):
    try:
        n = float(n)
        if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
        if n >= 1_000:     return f"{n/1_000:.0f}k"
        return f"{int(n):,}"
    except Exception:
        return str(n)

cols = st.columns(5)
kpis = [
    (cols[0], fmt(r.get("ATIVOS_ULTIMA_COMPETENCIA", 0)),  "Ativos — última competência"),
    (cols[1], fmt(r.get("TOTAL_ATIVOS_ACUMULADO", 0)),     "Total acumulado"),
    (cols[2], str(int(r.get("TOTAL_OPERADORAS", 0))),       "Operadoras ativas"),
    (cols[3], str(int(r.get("TOTAL_COMPETENCIAS", 0))),      "Competências"),
    (cols[4], f"{r.get('PRIMEIRA_COMPETENCIA','')}–{r.get('ULTIMA_COMPETENCIA','')}", "Período"),
]
for col, val, label in kpis:
    col.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-value'>{val}</div>
        <div class='kpi-label'>{label}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Evolução mensal
# ------------------------------------------------------------------
st.markdown("<div class='section-title'>Evolução mensal de beneficiários</div>",
            unsafe_allow_html=True)

df_evolucao["COMPETENCIA"] = df_evolucao["COMPETENCIA"].astype(str)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_evolucao["COMPETENCIA"], y=df_evolucao["TOTAL_ATIVOS"],
    name="Ativos", line=dict(color="#3dd6c4", width=2.5),
    fill="tozeroy", fillcolor="rgba(61,214,196,.07)", mode="lines",
))
fig.add_trace(go.Scatter(
    x=df_evolucao["COMPETENCIA"], y=df_evolucao["TOTAL_ADERIDOS"],
    name="Aderidos", line=dict(color="#5dd97a", width=1.5, dash="dot"), mode="lines",
))
fig.add_trace(go.Scatter(
    x=df_evolucao["COMPETENCIA"], y=df_evolucao["TOTAL_CANCELADOS"],
    name="Cancelados", line=dict(color="#f47560", width=1.5, dash="dot"), mode="lines",
))
fig.update_layout(
    height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Sora", color="#8da2b8"),
    legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
    margin=dict(l=0, r=0, t=30, b=0), hovermode="x unified",
    xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=9),
               tickmode="array",
               tickvals=df_evolucao["COMPETENCIA"].iloc[::6].tolist()),
    yaxis=dict(showgrid=True, gridcolor="#1f2d3d", gridwidth=0.5),
)
st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------
# Saldo líquido + ativos por ano
# ------------------------------------------------------------------
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("<div class='section-title'>Saldo líquido por competência</div>",
                unsafe_allow_html=True)
    cores = ["#5dd97a" if v >= 0 else "#f47560" for v in df_evolucao["SALDO_LIQUIDO"]]
    fig2 = go.Figure(go.Bar(
        x=df_evolucao["COMPETENCIA"], y=df_evolucao["SALDO_LIQUIDO"],
        marker_color=cores,
    ))
    fig2.update_layout(
        height=260, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Sora", color="#8da2b8"), showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=9),
                   tickmode="array",
                   tickvals=df_evolucao["COMPETENCIA"].iloc[::6].tolist()),
        yaxis=dict(showgrid=True, gridcolor="#1f2d3d", gridwidth=0.5),
    )
    st.plotly_chart(fig2, use_container_width=True)

with col_b:
    st.markdown("<div class='section-title'>Média de ativos por ano</div>",
                unsafe_allow_html=True)
    df_anual = (df_evolucao.groupby("ANO")["TOTAL_ATIVOS"]
                .mean().reset_index()
                .rename(columns={"TOTAL_ATIVOS": "MEDIA"}))
    fig3 = px.bar(df_anual, x="ANO", y="MEDIA",
                  color_discrete_sequence=["#4d9fff"])
    fig3.update_layout(
        height=260, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Sora", color="#8da2b8"), showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#1f2d3d", gridwidth=0.5),
    )
    st.plotly_chart(fig3, use_container_width=True)

# ------------------------------------------------------------------
# Rodapé
# ------------------------------------------------------------------
st.divider()
st.markdown("""
<div style='display:flex;justify-content:space-between;
            font-family:JetBrains Mono,monospace;font-size:.68rem;color:#5a7088'>
    <span>🏗 OCI Object Storage · Snowflake · Python · Streamlit</span>
    <span>ANS Dados Abertos · camada Gold</span>
    <span>Alagoas · 2019-04 → 2026-04</span>
</div>
""", unsafe_allow_html=True)
