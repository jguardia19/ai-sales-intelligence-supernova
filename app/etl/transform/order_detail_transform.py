import pandas as pd
from app.etl.utils.cleaning import strip_string_columns, drop_duplicates_by_columns
from app.etl.utils.dates import to_datetime_columns, add_date_key


def transform_fact_order_detail(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = strip_string_columns(df)
    df = drop_duplicates_by_columns(df, ["detail_id"])

    numeric_columns = [
        "detail_id",
        "client_id",
        "product_id",
        "precio_unitario",
        "cantidad",
        "subtotal",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = to_datetime_columns(df, ["fecha", "fecha_procesado"])
    df = add_date_key(df, "fecha", "fecha_key")
    df = add_date_key(df, "fecha_procesado", "fecha_procesado_key")

    expected_columns = [
        "detail_id",
        "orden",
        "client_id",
        "product_id",
        "product_name_snapshot",
        "product_code_snapshot",
        "precio_unitario",
        "cantidad",
        "subtotal",
        "fecha",
        "fecha_procesado",
        "fecha_key",
        "fecha_procesado_key",
    ]

    df = df[expected_columns]

    return df