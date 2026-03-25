import pandas as pd
from app.core.database import warehouse_engine


def get_dim_client_lookup() -> pd.DataFrame:
    query = """
    SELECT client_key, client_id
    FROM dim_client
    """
    return pd.read_sql(query, warehouse_engine)


def get_dim_product_lookup() -> pd.DataFrame:
    query = """
    SELECT product_key, product_id
    FROM dim_product
    """
    return pd.read_sql(query, warehouse_engine)


def get_dim_channel_lookup() -> pd.DataFrame:
    query = """
    SELECT channel_key, channel_name
    FROM dim_channel
    """
    return pd.read_sql(query, warehouse_engine)


def get_dim_storehouse_lookup() -> pd.DataFrame:
    query = """
    SELECT storehouse_key, almacen_id
    FROM dim_storehouse
    """
    return pd.read_sql(query, warehouse_engine)


def get_dim_subcategory_lookup() -> pd.DataFrame:
    query = """
    SELECT subcategory_key, subcategoria_id
    FROM dim_subcategory
    """
    return pd.read_sql(query, warehouse_engine)