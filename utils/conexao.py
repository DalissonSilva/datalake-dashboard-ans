"""
utils/conexao.py
================
Lê os Parquets Gold diretamente do bucket OCI público.
Sem Snowflake, sem credenciais — funciona para sempre.
Cache de 24h: dados mudam mensalmente, não precisa buscar a cada acesso.
"""

import streamlit as st
import pandas as pd

# ------------------------------------------------------------------
# URLs públicas do bucket Gold na OCI
# Namespace: grtzj1fytruq | Região: sa-saopaulo-1
# ------------------------------------------------------------------
_BASE = (
    "https://objectstorage.sa-saopaulo-1.oraclecloud.com"
    "/n/grtzj1fytruq/b/Gold/o"
)

ARQUIVOS = {
    "evolucao_mensal":    f"{_BASE}/ans_evolucao_mensal.parquet",
    "ranking_operadoras": f"{_BASE}/ans_ranking_operadoras.parquet",
    "faixa_etaria":       f"{_BASE}/ans_faixa_etaria.parquet",
    "modalidade":         f"{_BASE}/ans_modalidade.parquet",
    "resumo_geral":       f"{_BASE}/ans_resumo_geral.parquet",
}


@st.cache_data(ttl=86400, show_spinner=False)
def query(nome: str) -> pd.DataFrame:
    """
    Lê o parquet Gold pelo nome da view.
    Cache de 24h — dados mudam mensalmente.

    Uso:
      df = query('evolucao_mensal')
      df = query('ranking_operadoras')
      df = query('faixa_etaria')
      df = query('modalidade')
      df = query('resumo_geral')
    """
    url = ARQUIVOS.get(nome)
    if not url:
        raise ValueError(
            f"View '{nome}' não encontrada. "
            f"Disponíveis: {list(ARQUIVOS.keys())}"
        )
    try:
        return pd.read_parquet(url)
    except Exception as e:
        st.error(f"Erro ao carregar '{nome}': {e}")
        return pd.DataFrame()
