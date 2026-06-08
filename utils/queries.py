"""
utils/queries.py
================
Indicadores catalogados no DataGov.
"""

INDICADORES_GLOSSARIO = [
    {
        "codigo":     "IND-2026-0001",
        "nome":       "Beneficiários Ativos",
        "nivel":      "Operacional",
        "tipo":       "KPI",
        "natureza":   "Lagging",
        "regra":      "SUM(qt_beneficiario_ativo) agrupado por competência e UF",
        "fonte":      "ANS Dados Abertos — BRONZE.ANS_BENEFICIARIOS",
        "data_owner": "Secretaria de Saúde — AL",
        "status":     "Ativo",
        "descricao":  "Total de beneficiários com plano ativo no período de competência.",
    },
    {
        "codigo":     "IND-2026-0002",
        "nome":       "Beneficiários Aderidos",
        "nivel":      "Operacional",
        "tipo":       "KPI",
        "natureza":   "Leading",
        "regra":      "SUM(qt_beneficiario_aderido) agrupado por competência e UF",
        "fonte":      "ANS Dados Abertos — BRONZE.ANS_BENEFICIARIOS",
        "data_owner": "Secretaria de Saúde — AL",
        "status":     "Ativo",
        "descricao":  "Novos beneficiários que aderiram no período. Indicador antecedente — reflete tendência de crescimento.",
    },
    {
        "codigo":     "IND-2026-0003",
        "nome":       "Beneficiários Cancelados",
        "nivel":      "Operacional",
        "tipo":       "KPI",
        "natureza":   "Lagging",
        "regra":      "SUM(qt_beneficiario_cancelado) agrupado por competência e UF",
        "fonte":      "ANS Dados Abertos — BRONZE.ANS_BENEFICIARIOS",
        "data_owner": "Secretaria de Saúde — AL",
        "status":     "Ativo",
        "descricao":  "Beneficiários que cancelaram planos no período. Indicador consequente — reflete evasão já ocorrida.",
    },
]
