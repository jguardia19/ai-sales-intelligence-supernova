import pandas as pd
from app.etl.utils.cleaning import strip_string_columns, uppercase_columns, drop_duplicates_by_columns
from app.etl.utils.dates import to_datetime_columns, add_date_key


def transform_fact_order(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = strip_string_columns(df)
    df = uppercase_columns(df, ["channel_name", "envio"])
    df = drop_duplicates_by_columns(df, ["orden"])

    numeric_columns = [
        "folio_id",
        "client_id",
        "cantidad_productos",
        "total",
        "cajas",
        "is_delivery",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = to_datetime_columns(df, ["fecha_procesado", "fecha_salida", "fecha_entrega"])
    df = add_date_key(df, "fecha_procesado", "fecha_procesado_key")
    df = add_date_key(df, "fecha_salida", "fecha_salida_key")
    df = add_date_key(df, "fecha_entrega", "fecha_entrega_key")

    expected_columns = [
        "folio_id",
        "orden",
        "client_id",
        "nombres_cliente_snapshot",
        "channel_name",
        "paqueteria",
        "cantidad_productos",
        "total",
        "estatus",
        "cajas",
        "envio",
        "is_delivery",
        "fecha_procesado",
        "fecha_salida",
        "fecha_entrega",
        "fecha_procesado_key",
        "fecha_salida_key",
        "fecha_entrega_key",
    ]

    df = df[expected_columns]

    return df