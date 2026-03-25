from app.core.database import source_engine, warehouse_engine
from app.etl.sql.source_queries import SQL_DIM_CLIENT_SOURCE
from app.etl.extract.extractors import extract_dataframe
from app.etl.transform.transformers import normalize_text_columns
from app.etl.load.loaders import load_dataframe


def run():
    print("Extracting dim_client...")

    df_clients = extract_dataframe(source_engine, SQL_DIM_CLIENT_SOURCE)
    df_clients = normalize_text_columns(
        df_clients,
        ["nombre", "apellido", "direccion", "colonia", "ciudad", "estado", "codigo_postal", "telefono", "correo"]
    )

    load_dataframe(df_clients, "dim_client", warehouse_engine, if_exists="append")

    print("ETL process completed successfully!")

if __name__ == "__main__":
    run()
