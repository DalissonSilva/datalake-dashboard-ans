"""pages/02_operadoras.py — Ranking e análise das operadoras."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.conexao import query

st.set_page_config(page_title="Operadoras · ANS", page_icon="🏢", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'Sora',sans-serif}
.section-title{font-size:1.1rem;font-weight:600;color:#e8eef5;margin:1.5rem 0 .7rem;
    padding-bottom:.4rem;border-bottom:1px solid #1f2d3d}
</style>""", unsafe_allow_html=True)

st.markdown("## 🏢 Operadoras de Saúde")

with st.spinner("Carregando..."):
    df_rank = query("ranking_operadoras")
    df_mod  = query("modalidade")

df_rank["COMPETENCIA"] = df_rank["COMPETENCIA"].astype(str)
df_mod["COMPETENCIA"]  = df_mod["COMPETENCIA"].astype(str)

col_f1, col_f2 = st.columns(2)
with col_f1:
    comps    = sorted(df_rank["COMPETENCIA"].unique(), reverse=True)
    comp_sel = st.selectbox("Competência", comps)
with col_f2:
    top_n = st.slider("Top N operadoras", 5, 20, 10)

df_c   = df_rank[df_rank["COMPETENCIA"] == comp_sel]
df_top = df_c.head(top_n)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Operadoras",      df_c["CD_OPERADORA"].nunique())
c2.metric("Total Ativos",    f"{df_c['TOTAL_ATIVOS'].sum():,.0f}")
c3.metric("Total Aderidos",  f"{df_c['TOTAL_ADERIDOS'].sum():,.0f}")
c4.metric("Total Cancelados",f"{df_c['TOTAL_CANCELADOS'].sum():,.0f}")

st.markdown("<div class='section-title'>Ranking — beneficiários ativos</div>", unsafe_allow_html=True)
fig = go.Figure(go.Bar(
    x=df_top["TOTAL_ATIVOS"], y=df_top["NM_OPERADORA"], orientation="h",
    marker_color="#3dd6c4",
    text=df_top["TOTAL_ATIVOS"].apply(lambda v: f"{v:,.0f}"), textposition="outside",
))
fig.update_layout(height=max(260, top_n*34), paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Sora",color="#8da2b8",size=11),
    margin=dict(l=0,r=80,t=10,b=0), showlegend=False,
    xaxis=dict(showgrid=True,gridcolor="#1f2d3d",gridwidth=0.5),
    yaxis=dict(showgrid=False,autorange="reversed"))
st.plotly_chart(fig, use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("<div class='section-title'>Taxa de cancelamento</div>", unsafe_allow_html=True)
    df_canc = (df_c.dropna(subset=["TAXA_CANCELAMENTO_PCT"])
               .sort_values("TAXA_CANCELAMENTO_PCT", ascending=False).head(10))
    cores = ["#f47560" if v>5 else "#f5b942" if v>2 else "#5dd97a"
             for v in df_canc["TAXA_CANCELAMENTO_PCT"]]
    fig2 = go.Figure(go.Bar(x=df_canc["NM_OPERADORA"], y=df_canc["TAXA_CANCELAMENTO_PCT"],
        marker_color=cores,
        text=df_canc["TAXA_CANCELAMENTO_PCT"].apply(lambda v:f"{v:.1f}%"),
        textposition="outside"))
    fig2.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Sora",color="#8da2b8",size=10), margin=dict(l=0,r=0,t=10,b=0),
        showlegend=False, xaxis=dict(showgrid=False,tickangle=-35),
        yaxis=dict(showgrid=True,gridcolor="#1f2d3d",gridwidth=0.5,title="Taxa (%)"))
    st.plotly_chart(fig2, use_container_width=True)

with col_b:
    st.markdown("<div class='section-title'>Distribuição por modalidade</div>", unsafe_allow_html=True)
    df_m = (df_mod[df_mod["COMPETENCIA"]==comp_sel]
            .groupby("MODALIDADE_OPERADORA")["TOTAL_ATIVOS"].sum()
            .reset_index().sort_values("TOTAL_ATIVOS", ascending=False))
    fig3 = px.pie(df_m, names="MODALIDADE_OPERADORA", values="TOTAL_ATIVOS",
        color_discrete_sequence=["#3dd6c4","#4d9fff","#f5b942","#9b87f5","#5dd97a","#f47560"],
        hole=.45)
    fig3.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Sora",color="#8da2b8"),
        legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10)),
        margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("<div class='section-title'>Detalhe por operadora</div>", unsafe_allow_html=True)
st.dataframe(
    df_c[["NM_OPERADORA","MODALIDADE_OPERADORA","TOTAL_ATIVOS",
          "TOTAL_ADERIDOS","TOTAL_CANCELADOS","TAXA_CANCELAMENTO_PCT"]]
    .sort_values("TOTAL_ATIVOS", ascending=False).reset_index(drop=True),
    use_container_width=True, hide_index=True)
