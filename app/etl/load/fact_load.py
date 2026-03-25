import pandas as pd

from app.core.database import warehouse_engine
from app.etl.load.loaders import truncate_table, append_dataframe
from app.etl.load.lookup_load import (
    get_dim_channel_lookup,
    get_dim_client_lookup,
    get_dim_product_lookup,
    get_dim_storehouse_lookup,
)


def prepare_fact_order(df_orders: pd.DataFrame) -> pd.DataFrame:
    df = df_orders.copy()

    df_clients = get_dim_client_lookup()
    df_channels = get_dim_channel_lookup()

    df = df.merge(df_clients, on="client_id", how="left")
    df = df.merge(df_channels, on="channel_name", how="left")

    df["fecha_procesado_key"] = pd.to_numeric(df["fecha_procesado_key"], errors="coerce").astype("Int64")
    df["fecha_salida_key"] = pd.to_numeric(df["fecha_salida_key"], errors="coerce").astype("Int64")
    df["fecha_entrega_key"] = pd.to_numeric(df["fecha_entrega_key"], errors="coerce").astype("Int64")

    fact_df = df[
        [
            "folio_id",
            "orden",
            "client_key",
            "channel_key",
            "fecha_procesado_key",
            "fecha_salida_key",
            "fecha_entrega_key",
            "paqueteria",
            "cantidad_productos",
            "total",
            "estatus",
            "cajas",
            "envio",
            "is_delivery",
        ]
    ].copy()

    return fact_df


def prepare_fact_order_detail(df_order_detail: pd.DataFrame) -> pd.DataFrame:
    df = df_order_detail.copy()

    df_clients = get_dim_client_lookup()
    df_products = get_dim_product_lookup()

    query_orders = """
    SELECT order_key, orden
    FROM fact_order
    """
    df_orders_lookup = pd.read_sql(query_orders, warehouse_engine)

    df = df.merge(df_clients, on="client_id", how="left")
    df = df.merge(df_products, on="product_id", how="left")
    df = df.merge(df_orders_lookup, on="orden", how="left")

    df["fecha_key"] = pd.to_numeric(df["fecha_key"], errors="coerce").astype("Int64")
    df["fecha_procesado_key"] = pd.to_numeric(df["fecha_procesado_key"], errors="coerce").astype("Int64")

    fact_df = df[
        [
            "detail_id",
            "orden",
            "order_key",
            "client_key",
            "product_key",
            "fecha_key",
            "fecha_procesado_key",
            "cantidad",
            "precio_unitario",
            "subtotal",
            "product_name_snapshot",
            "product_code_snapshot",
        ]
    ].copy()

    return fact_df


def prepare_fact_inventory_snapshot(df_inventory: pd.DataFrame) -> pd.DataFrame:
    df = df_inventory.copy()

    df_storehouses = get_dim_storehouse_lookup()
    df_products = get_dim_product_lookup()

    df = df.merge(df_storehouses, on="almacen_id", how="left")
    df = df.merge(df_products, on="product_id", how="left")

    fact_df = df[
        [
            "snapshot_date_key",
            "storehouse_key",
            "product_key",
            "cantidad",
        ]
    ].copy()

    return fact_df


def load_facts(transformed_data: dict) -> None:
    if "fact_order" in transformed_data:
        print("[LOAD] Preparando fact_order...")
        fact_order_df = prepare_fact_order(transformed_data["fact_order"])
        truncate_table(warehouse_engine, "fact_order")
        append_dataframe(fact_order_df, "fact_order", warehouse_engine)

    if "fact_order_detail" in transformed_data:
        print("[LOAD] Preparando fact_order_detail...")
        fact_order_detail_df = prepare_fact_order_detail(transformed_data["fact_order_detail"])
        truncate_table(warehouse_engine, "fact_order_detail")
        append_dataframe(fact_order_detail_df, "fact_order_detail", warehouse_engine)

    if "fact_inventory_snapshot" in transformed_data:
        print("[LOAD] Preparando fact_inventory_snapshot...")
        fact_inventory_df = prepare_fact_inventory_snapshot(transformed_data["fact_inventory_snapshot"])
        truncate_table(warehouse_engine, "fact_inventory_snapshot")
        append_dataframe(fact_inventory_df, "fact_inventory_snapshot", warehouse_engine)