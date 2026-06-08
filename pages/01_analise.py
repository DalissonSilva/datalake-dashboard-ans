"""pages/01_analise.py — Análise detalhada com filtros."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.conexao import query

st.set_page_config(page_title="Análise · ANS", page_icon="📊", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'Sora',sans-serif}
.section-title{font-size:1.1rem;font-weight:600;color:#e8eef5;margin:1.5rem 0 .7rem;
    padding-bottom:.4rem;border-bottom:1px solid #1f2d3d}
</style>""", unsafe_allow_html=True)

st.markdown("## 📊 Análise Detalhada")

with st.spinner("Carregando..."):
    df = query("evolucao_mensal")

df["COMPETENCIA"] = df["COMPETENCIA"].astype(str)

col_f1, col_f2 = st.columns(2)
with col_f1:
    anos = sorted(df["ANO"].unique())
    ano_sel = st.multiselect("Ano", anos, default=anos[-3:])
with col_f2:
    metrica = st.selectbox(
        "Métrica",
        ["TOTAL_ATIVOS","TOTAL_ADERIDOS","TOTAL_CANCELADOS","SALDO_LIQUIDO"],
        format_func=lambda x: x.replace("_"," ").title()
    )

df_f = df[df["ANO"].isin(ano_sel)] if ano_sel else df

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Ativos",     f"{df_f['TOTAL_ATIVOS'].sum():,.0f}")
c2.metric("Total Aderidos",   f"{df_f['TOTAL_ADERIDOS'].sum():,.0f}")
c3.metric("Total Cancelados", f"{df_f['TOTAL_CANCELADOS'].sum():,.0f}")
c4.metric("Saldo Líquido",    f"{df_f['SALDO_LIQUIDO'].sum():,.0f}")

st.markdown(f"<div class='section-title'>{metrica.replace('_',' ').title()} — evolução mensal</div>",
            unsafe_allow_html=True)
fig = px.area(df_f, x="COMPETENCIA", y=metrica, color_discrete_sequence=["#3dd6c4"])
fig.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Sora",color="#8da2b8"), margin=dict(l=0,r=0,t=10,b=0), showlegend=False,
    xaxis=dict(showgrid=False,tickangle=-45,tickfont=dict(size=9)),
    yaxis=dict(showgrid=True,gridcolor="#1f2d3d",gridwidth=0.5))
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='section-title'>Comparativo anual</div>", unsafe_allow_html=True)
df_anual = (df_f.groupby("ANO")
    .agg(ATIVOS=("TOTAL_ATIVOS","sum"), ADERIDOS=("TOTAL_ADERIDOS","sum"),
         CANCELADOS=("TOTAL_CANCELADOS","sum")).reset_index())
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=df_anual["ANO"],y=df_anual["ATIVOS"],    name="Ativos",     marker_color="#3dd6c4"))
fig2.add_trace(go.Bar(x=df_anual["ANO"],y=df_anual["ADERIDOS"],  name="Aderidos",   marker_color="#5dd97a"))
fig2.add_trace(go.Bar(x=df_anual["ANO"],y=df_anual["CANCELADOS"],name="Cancelados", marker_color="#f47560"))
fig2.update_layout(height=280, barmode="group", paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Sora",color="#8da2b8"),
    legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.08),
    margin=dict(l=0,r=0,t=30,b=0),
    xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,gridcolor="#1f2d3d",gridwidth=0.5))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("<div class='section-title'>Tabela detalhada</div>", unsafe_allow_html=True)
st.dataframe(
    df_f[["COMPETENCIA","ANO","MES","TOTAL_ATIVOS","TOTAL_ADERIDOS",
          "TOTAL_CANCELADOS","SALDO_LIQUIDO","TOTAL_OPERADORAS"]]
    .sort_values("COMPETENCIA", ascending=False),
    use_container_width=True, hide_index=True)
