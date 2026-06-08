# Data Lake ANS — Beneficiários de Saúde Suplementar · Alagoas

Dashboard público construído sobre pipeline de dados end-to-end usando
infraestrutura 100% gratuita: OCI + Snowflake + Streamlit Cloud.

## Como funciona

```
ANS Dados Abertos
      ↓ (pipeline Python — VM OCI)
  Stage (OCI bucket privado)     ← Parquet particionado
      ↓
  Bronze → Silver → Gold         ← Snowflake
      ↓ (gold_export.py)
  Gold (OCI bucket público)      ← Parquet por view
      ↓
  Dashboard (Streamlit Cloud)    ← pd.read_parquet(URL pública)
```

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Orquestração | Python 3.10 + Poetry |
| Data Lake | OCI Object Storage |
| Governança | OCI Autonomous Database |
| Data Warehouse | Snowflake (Bronze/Silver/Gold) |
| Dashboard | Streamlit Cloud |

## Executar localmente

```bash
git clone https://github.com/SEU-USUARIO/datalake-dashboard.git
cd datalake-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Não precisa de credenciais — lê direto das URLs públicas do bucket OCI.

## Deploy no Streamlit Cloud

1. Sobe o código para o GitHub
2. Acessa [share.streamlit.io](https://share.streamlit.io)
3. Seleciona o repositório → `app.py`
4. Clica em **Deploy** — sem secrets necessários

## Atualizar os dados (mensal)

Na VM OCI, após a carga Bronze:

```bash
cd ~/project/etl-datalake
poetry run python -m etl_datalake.etl.ans.gold_export
```

Os Parquets no bucket Gold são atualizados e o dashboard reflete
os novos dados automaticamente na próxima consulta (cache 24h).

## Indicadores catalogados (padrão DAMA)

| Código | Nome | Regra |
|--------|------|-------|
| IND-2026-0001 | Beneficiários Ativos | `SUM(qt_beneficiario_ativo)` |
| IND-2026-0002 | Beneficiários Aderidos | `SUM(qt_beneficiario_aderido)` |
| IND-2026-0003 | Beneficiários Cancelados | `SUM(qt_beneficiario_cancelado)` |
