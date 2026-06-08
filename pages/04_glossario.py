"""pages/04_glossario.py — Glossário de indicadores padrão DAMA."""

import streamlit as st
from utils.queries import INDICADORES_GLOSSARIO

st.set_page_config(page_title="Glossário · ANS", page_icon="📋", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'Sora',sans-serif}
.ind-card{background:linear-gradient(160deg,#0f1620,#131c28);border:1px solid #1f2d3d;
    border-radius:14px;padding:1.4rem 1.6rem;margin-bottom:1rem;transition:border-color .25s}
.ind-card:hover{border-color:#3dd6c4}
.ind-code{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#3dd6c4;
    letter-spacing:.15em;margin-bottom:.3rem}
.ind-nome{font-size:1.1rem;font-weight:600;color:#e8eef5;margin-bottom:.7rem}
.ind-desc{font-size:.86rem;color:#8da2b8;font-weight:300;line-height:1.6;margin-bottom:.9rem}
.ind-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.6rem}
.ind-field .lbl{color:#5a7088;font-family:'JetBrains Mono',monospace;font-size:.66rem;
    letter-spacing:.1em;text-transform:uppercase;display:block;margin-bottom:.2rem}
.ind-field .val{color:#e8eef5;font-size:.84rem}
.badge{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:.68rem;
    padding:.22rem .55rem;border-radius:6px;font-weight:500;margin-right:.3rem}
.b-op{background:rgba(93,217,122,.12);color:#5dd97a}
.b-kpi{background:rgba(61,214,196,.12);color:#3dd6c4}
.b-lag{background:rgba(245,185,66,.12);color:#f5b942}
.b-lea{background:rgba(93,217,122,.12);color:#5dd97a}
.b-ok{background:rgba(93,217,122,.12);color:#5dd97a}
.regra{font-family:'JetBrains Mono',monospace;font-size:.78rem;background:#070a0f;
    border:1px solid #1f2d3d;border-left:3px solid #3dd6c4;border-radius:8px;
    padding:.7rem 1rem;color:#b8c9da;margin-top:.8rem}
</style>""", unsafe_allow_html=True)

st.markdown("""
<div style='margin-bottom:1.5rem'>
    <div style='font-family:JetBrains Mono,monospace;font-size:.7rem;color:#3dd6c4;
                letter-spacing:.3em;text-transform:uppercase;margin-bottom:.5rem'>
        ◆ DataGov · Repositório de Indicadores</div>
    <h2 style='font-size:1.8rem;font-weight:700;color:#e8eef5;margin:0'>Glossário de Indicadores</h2>
    <p style='color:#8da2b8;font-size:.9rem;font-weight:300;margin-top:.4rem'>
        Ficha técnica · regra, data owner, nível e fonte · Padrão DAMA-DMBOK
    </p>
</div>""", unsafe_allow_html=True)

with st.expander("📌 Contexto da demanda — Secretaria de Saúde de Alagoas"):
    st.markdown("""
**Solicitante:** Gerência de Informação em Saúde — Secretaria de Saúde do Estado de Alagoas  
**Data owner:** Departamento de Regulação e Controle  
**Problema identificado:** Múltiplas áreas utilizavam regras diferentes para o mesmo indicador,
causando divergências nos relatórios gerenciais — dor real vivenciada em projetos anteriores.  
**Solução:** Centralização no DataGov com data owner único corporativo.
A regra só pode ser alterada pelo data owner — as áreas consomem, não definem.
    """)

busca = st.text_input("🔍 Buscar indicador", placeholder="nome, código ou regra...")
inds  = INDICADORES_GLOSSARIO
if busca:
    b    = busca.lower()
    inds = [i for i in inds if b in i["nome"].lower()
            or b in i["codigo"].lower() or b in i["regra"].lower()]

if not inds:
    st.info("Nenhum indicador encontrado.")

nat_cls = {"Lagging":"b-lag","Leading":"b-lea"}

for ind in inds:
    nc = nat_cls.get(ind["natureza"],"b-kpi")
    st.markdown(f"""
<div class='ind-card'>
    <div class='ind-code'>{ind['codigo']}</div>
    <div class='ind-nome'>
        {ind['nome']}
        <span class='badge b-kpi'>{ind['tipo']}</span>
        <span class='badge b-op'>{ind['nivel']}</span>
        <span class='badge {nc}'>{ind['natureza']}</span>
        <span class='badge b-ok'>{ind['status']}</span>
    </div>
    <div class='ind-desc'>{ind['descricao']}</div>
    <div class='ind-grid'>
        <div class='ind-field'><span class='lbl'>Data owner</span><span class='val'>{ind['data_owner']}</span></div>
        <div class='ind-field'><span class='lbl'>Fonte</span><span class='val'>{ind['fonte']}</span></div>
        <div class='ind-field'><span class='lbl'>Nível</span><span class='val'>{ind['nivel']}</span></div>
        <div class='ind-field'><span class='lbl'>Natureza</span><span class='val'>{ind['natureza']}</span></div>
    </div>
    <div class='regra'>
        <span style='color:#5a7088;font-size:.63rem;letter-spacing:.15em;text-transform:uppercase'>
            Regra de cálculo</span><br>{ind['regra']}
    </div>
</div>""", unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style='font-family:JetBrains Mono,monospace;font-size:.68rem;color:#5a7088;text-align:center'>
    Gestão de indicadores · padrão DAMA-DMBOK · data owner único corporativo
</div>""", unsafe_allow_html=True)
