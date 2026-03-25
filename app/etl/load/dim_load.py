from app.core.database import warehouse_engine
from app.etl.load.loaders import truncate_table, append_dataframe



def load_dimensions(transformed_data: dict) -> None:
    load_order = [
        "dim_client",
        "dim_subcategory",
        "dim_storehouse",
        "dim_channel",
        "dim_date",
        "dim_product",
    ]

    for table_name in load_order:
        if table_name not in transformed_data:
            print(f"[LOAD] {table_name}: no encontrado en transformed_data")
            continue

        print(f"[LOAD] Cargando dimensión: {table_name}")
        truncate_table(warehouse_engine, table_name)
        append_dataframe(transformed_data[table_name], table_name, warehouse_engine)