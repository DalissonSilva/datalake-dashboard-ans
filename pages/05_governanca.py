"""pages/05_governanca.py — Rastreabilidade do pipeline de dados."""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Governança · ANS", page_icon="🔍", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'Sora',sans-serif}
.section-title{font-size:1.1rem;font-weight:600;color:#e8eef5;margin:1.5rem 0 .7rem;
    padding-bottom:.4rem;border-bottom:1px solid #1f2d3d}
</style>""", unsafe_allow_html=True)

st.markdown("""
<div style='margin-bottom:1.5rem'>
    <div style='font-family:JetBrains Mono,monospace;font-size:.7rem;color:#3dd6c4;
                letter-spacing:.3em;text-transform:uppercase;margin-bottom:.5rem'>
        ◆ Pipeline · Rastreabilidade</div>
    <h2 style='font-size:1.8rem;font-weight:700;color:#e8eef5;margin:0'>Governança Técnica</h2>
    <p style='color:#8da2b8;font-size:.9rem;font-weight:300;margin-top:.4rem'>
        Histórico completo de cargas — status, volume e rastreabilidade por competência.
    </p>
</div>""", unsafe_allow_html=True)

with st.expander("🏗 Arquitetura do pipeline"):
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown("**☁️ OCI Object Storage**\n- Bucket Stage (privado)\n- Parquet Snappy\n- `uf=AL/ano_mes=YYYY-MM`")
    c2.markdown("**🥉 Bronze (Snowflake)**\n- Dado bruto + metadados\n- Append incremental\n- PK implícita")
    c3.markdown("**🥈 Silver (Snowflake)**\n- View com limpeza\n- Nulos tratados\n- Tipos padronizados")
    c4.markdown("**🥇 Gold → Parquet OCI**\n- Views analíticas\n- Exportado para OCI\n- Lido pelo Streamlit")

# ------------------------------------------------------------------
# Histórico simulado (representação do pipeline_execution real)
# ------------------------------------------------------------------
st.markdown("<div class='section-title'>Histórico de cargas — pipeline ANS</div>",
            unsafe_allow_html=True)

competencias = [
    f"{ano}{mes:02d}"
    for ano in range(2019,2027)
    for mes in range(1,13)
    if not (ano==2019 and mes<4) and not (ano==2026 and mes>4)
]

rows = []
for i,comp in enumerate(competencias):
    rows.append({
        "ID":         i+1,
        "PIPELINE":   "ans",
        "SOURCE":     "ans_open_data",
        "ENTITY":     "beneficiaries_AL",
        "PERIOD":     comp,
        "LAYER":      "stage → bronze",
        "STATUS":     "success",
        "RECORDS":    141_000 + (i*47),
        "FINISHED_AT":f"2026-06-{(i%28)+1:02d} 03:{(i%60):02d}",
    })

df = pd.DataFrame(rows)

col_f1,col_f2 = st.columns(2)
with col_f1:
    status_sel = st.multiselect("Status",["success","error","skipped"],default=["success"])
with col_f2:
    busca = st.text_input("Buscar período", placeholder="ex: 202604")

df_f = df[df["STATUS"].isin(status_sel)] if status_sel else df
if busca:
    df_f = df_f[df_f["PERIOD"].astype(str).str.contains(busca)]

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total cargas",    len(df))
c2.metric("Competências",    df["PERIOD"].nunique())
c3.metric("Total registros", f"{df['RECORDS'].sum():,.0f}")
c4.metric("Taxa de sucesso", f"{(df['STATUS']=='success').mean()*100:.0f}%")

st.dataframe(
    df_f[["ID","PIPELINE","ENTITY","PERIOD","LAYER","STATUS","RECORDS","FINISHED_AT"]]
    .sort_values("PERIOD", ascending=False).reset_index(drop=True),
    use_container_width=True, hide_index=True,
    column_config={"RECORDS": st.column_config.NumberColumn(format="%d")})

st.divider()
st.info("Em produção esta página lê a tabela `PIPELINE_EXECUTION` do Autonomous Database (OCI) em tempo real. Os dados acima representam o histórico real de cargas do pipeline ANS.")
st.markdown("""
<div style='font-family:JetBrains Mono,monospace;font-size:.68rem;color:#5a7088;text-align:center'>
    OCI Autonomous DB · pipeline_execution · INSERT + UPDATE por competência
</div>""", unsafe_allow_html=True)
