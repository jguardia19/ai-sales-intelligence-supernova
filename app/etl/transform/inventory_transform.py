import pandas as pd
from app.etl.utils.cleaning import drop_duplicates_by_columns


def transform_fact_inventory_snapshot(df: pd.DataFrame, snapshot_date_key: int) -> pd.DataFrame:
    df = df.copy()

    numeric_columns = [
        "inventory_row_id",
        "almacen_id",
        "product_id",
        "cantidad",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = drop_duplicates_by_columns(df, ["inventory_row_id"])
    df["snapshot_date_key"] = snapshot_date_key

    expected_columns = [
        "inventory_row_id",
        "almacen_id",
        "product_id",
        "cantidad",
        "snapshot_date_key",
    ]

    df = df[expected_columns]

    return df