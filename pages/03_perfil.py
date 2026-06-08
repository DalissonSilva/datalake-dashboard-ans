"""pages/03_perfil.py — Perfil dos beneficiários por faixa etária e sexo."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.conexao import query

st.set_page_config(page_title="Perfil · ANS", page_icon="👥", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'Sora',sans-serif}
.section-title{font-size:1.1rem;font-weight:600;color:#e8eef5;margin:1.5rem 0 .7rem;
    padding-bottom:.4rem;border-bottom:1px solid #1f2d3d}
</style>""", unsafe_allow_html=True)

st.markdown("## 👥 Perfil dos Beneficiários")

with st.spinner("Carregando..."):
    df = query("faixa_etaria")

df["COMPETENCIA"] = df["COMPETENCIA"].astype(str)

comps    = sorted(df["COMPETENCIA"].unique(), reverse=True)
comp_sel = st.selectbox("Competência", comps)
df_f     = df[df["COMPETENCIA"] == comp_sel]

st.markdown("<div class='section-title'>Pirâmide etária — masculino vs feminino</div>",
            unsafe_allow_html=True)
df_m  = df_f[df_f["SEXO"]=="M"].groupby("FAIXA_ETARIA")["TOTAL_ATIVOS"].sum().reset_index()
df_fe = df_f[df_f["SEXO"]=="F"].groupby("FAIXA_ETARIA")["TOTAL_ATIVOS"].sum().reset_index()

fig = go.Figure()
fig.add_trace(go.Bar(y=df_m["FAIXA_ETARIA"],  x=-df_m["TOTAL_ATIVOS"],
    name="Masculino", orientation="h", marker_color="#4d9fff"))
fig.add_trace(go.Bar(y=df_fe["FAIXA_ETARIA"], x=df_fe["TOTAL_ATIVOS"],
    name="Feminino",  orientation="h", marker_color="#f47560"))
fig.update_layout(barmode="overlay", height=380,
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Sora",color="#8da2b8"),
    legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.08),
    margin=dict(l=0,r=0,t=30,b=0),
    xaxis=dict(showgrid=True,gridcolor="#1f2d3d",gridwidth=0.5,title="Beneficiários"),
    yaxis=dict(showgrid=False))
st.plotly_chart(fig, use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("<div class='section-title'>Distribuição por sexo</div>", unsafe_allow_html=True)
    df_sexo = df_f.groupby("SEXO")["TOTAL_ATIVOS"].sum().reset_index()
    df_sexo["SEXO"] = df_sexo["SEXO"].map({"M":"Masculino","F":"Feminino"})
    fig2 = px.pie(df_sexo, names="SEXO", values="TOTAL_ATIVOS",
        color_discrete_sequence=["#4d9fff","#f47560"], hole=.5)
    fig2.update_layout(height=240, paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Sora",color="#8da2b8"),
        legend=dict(bgcolor="rgba(0,0,0,0)"), margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig2, use_container_width=True)

with col_b:
    st.markdown("<div class='section-title'>Total por faixa etária</div>", unsafe_allow_html=True)
    df_faixa = df_f.groupby("FAIXA_ETARIA")["TOTAL_ATIVOS"].sum().reset_index()
    fig3 = px.bar(df_faixa, x="FAIXA_ETARIA", y="TOTAL_ATIVOS",
        color_discrete_sequence=["#9b87f5"])
    fig3.update_layout(height=240, paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Sora",color="#8da2b8",size=10),
        showlegend=False, margin=dict(l=0,r=0,t=10,b=0),
        xaxis=dict(showgrid=False,tickangle=-35),
        yaxis=dict(showgrid=True,gridcolor="#1f2d3d",gridwidth=0.5))
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("<div class='section-title'>Evolução de uma faixa etária</div>", unsafe_allow_html=True)
faixas    = sorted(df["FAIXA_ETARIA"].unique())
faixa_sel = st.selectbox("Faixa etária", faixas)
df_evo = (df[df["FAIXA_ETARIA"]==faixa_sel]
          .groupby(["COMPETENCIA","SEXO"])["TOTAL_ATIVOS"].sum().reset_index())
fig4 = px.line(df_evo, x="COMPETENCIA", y="TOTAL_ATIVOS", color="SEXO",
    color_discrete_map={"M":"#4d9fff","F":"#f47560"})
fig4.update_layout(height=240, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Sora",color="#8da2b8"),
    legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.08),
    margin=dict(l=0,r=0,t=30,b=0),
    xaxis=dict(showgrid=False,tickangle=-45,tickfont=dict(size=9),
               tickmode="array",
               tickvals=df_evo["COMPETENCIA"].iloc[::6].tolist()),
    yaxis=dict(showgrid=True,gridcolor="#1f2d3d",gridwidth=0.5))
st.plotly_chart(fig4, use_container_width=True)
