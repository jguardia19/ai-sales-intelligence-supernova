from app.core.database import source_engine
from app.etl.extract.extractors import extract_named_dataframe
from app.etl.sql.source_queries import SOURCE_QUERIES


def run():
    df_clients = extract_named_dataframe(
        source_engine,
        "dim_client",
        SOURCE_QUERIES["dim_client"]
    )
    print(df_clients.head())
    print(df_clients.info())

    df_products = extract_named_dataframe(
        source_engine,
        "dim_product",
        SOURCE_QUERIES["dim_product"]
    )
    print(df_products.head())
    print(df_products.info())

    df_orders = extract_named_dataframe(
        source_engine,
        "fact_order",
        SOURCE_QUERIES["fact_order"]
    )
    print(df_orders.head())
    print(df_orders.info())

    df_order_detail = extract_named_dataframe(
        source_engine,
        "fact_order_detail",
        SOURCE_QUERIES["fact_order_detail"]
    )
    print(df_order_detail.head())
    print(df_order_detail.info())

    df_inventory = extract_named_dataframe(
        source_engine,
        "fact_inventory_snapshot",
        SOURCE_QUERIES["fact_inventory_snapshot"]
    )
    print(df_inventory.head())
    print(df_inventory.info())


if __name__ == "__main__":
    run()