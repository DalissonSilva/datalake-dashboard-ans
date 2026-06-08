"""
etl/ans/gold_export.py
=======================
Exporta as views Gold do Snowflake para Parquet no bucket OCI 'Gold'.
O bucket Gold é público — permite acesso direto pelo Streamlit Cloud.

Executar após cada carga Bronze para manter o Gold atualizado.

Execução:
  cd ~/project/etl-datalake
  poetry run python -m etl_datalake.etl.ans.gold_export
"""

import warnings
warnings.filterwarnings("ignore")

import oci
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO

from etl_datalake.utils.conexao_snowflake import get_snowflake_connection

# ------------------------------------------------------------------
# Configurações
# ------------------------------------------------------------------
BUCKET_GOLD = "Gold"

VIEWS = [
    {
        "view":   "DATALAKE.GOLD.ANS_EVOLUCAO_MENSAL",
        "objeto": "ans_evolucao_mensal.parquet",
    },
    {
        "view":   "DATALAKE.GOLD.ANS_RANKING_OPERADORAS",
        "objeto": "ans_ranking_operadoras.parquet",
    },
    {
        "view":   "DATALAKE.GOLD.ANS_FAIXA_ETARIA",
        "objeto": "ans_faixa_etaria.parquet",
    },
    {
        "view":   "DATALAKE.GOLD.ANS_MODALIDADE",
        "objeto": "ans_modalidade.parquet",
    },
    {
        "view":   "DATALAKE.GOLD.ANS_RESUMO_GERAL",
        "objeto": "ans_resumo_geral.parquet",
    },
]


# ------------------------------------------------------------------
# Cliente OCI via Instance Principal
# ------------------------------------------------------------------
def get_oci_client():
    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    return oci.object_storage.ObjectStorageClient(config={}, signer=signer)


# ------------------------------------------------------------------
# Upload de DataFrame como Parquet para o bucket OCI
# ------------------------------------------------------------------
def upload_parquet(client, namespace: str, bucket: str,
                   object_name: str, df: pd.DataFrame) -> bool:
    buffer = BytesIO()
    table  = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(table, buffer, compression="snappy")
    buffer.seek(0)

    client.put_object(
        namespace_name = namespace,
        bucket_name    = bucket,
        object_name    = object_name,
        put_object_body= buffer,
        content_type   = "application/octet-stream",
    )

    # Confirma com head_object
    try:
        client.head_object(namespace, bucket, object_name)
        return True
    except Exception:
        return False


# ------------------------------------------------------------------
# Exportação principal
# ------------------------------------------------------------------
def exportar():
    print("=" * 60)
    print("EXPORTAÇÃO: Gold Snowflake → Parquet OCI")
    print(f"Bucket destino: {BUCKET_GOLD} (público)")
    print("=" * 60)

    # Clientes
    oci_client = get_oci_client()
    namespace  = oci_client.get_namespace().data
    sf_conn    = get_snowflake_connection()

    print(f"\nNamespace OCI: {namespace}")

    total_registros = 0
    exportados      = 0
    erros           = 0

    for item in VIEWS:
        view   = item["view"]
        objeto = item["objeto"]

        print(f"\n{'─'*50}")
        print(f"📥 {view}")

        try:
            # 1) Lê do Snowflake
            df = pd.read_sql(f"SELECT * FROM {view}", sf_conn)
            print(f"   {len(df):,} registros × {len(df.columns)} colunas")

            # 2) Upload para OCI
            confirmado = upload_parquet(
                oci_client, namespace, BUCKET_GOLD, objeto, df
            )

            if confirmado:
                url = (
                    f"https://objectstorage.sa-saopaulo-1.oraclecloud.com"
                    f"/n/{namespace}/b/{BUCKET_GOLD}/o/{objeto}"
                )
                print(f"   ✅ Salvo em {BUCKET_GOLD}/{objeto}")
                print(f"   🌐 URL: {url}")
                total_registros += len(df)
                exportados      += 1
            else:
                print(f"   ❌ Upload não confirmado")
                erros += 1

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            erros += 1

    sf_conn.close()

    print(f"\n{'='*60}")
    print(f"✅ EXPORTAÇÃO CONCLUÍDA")
    print(f"   Exportados: {exportados} arquivo(s)")
    print(f"   Erros:      {erros} arquivo(s)")
    print(f"   Registros:  {total_registros:,}")
    print(f"\n📋 URLs públicas:")
    for item in VIEWS:
        print(f"   https://objectstorage.sa-saopaulo-1.oraclecloud.com"
              f"/n/{namespace}/b/{BUCKET_GOLD}/o/{item['objeto']}")
    print(f"{'='*60}")


if __name__ == "__main__":
    exportar()
