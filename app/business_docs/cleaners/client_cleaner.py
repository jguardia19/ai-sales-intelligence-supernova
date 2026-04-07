import pandas as pd
from app.business_docs.cleaners.common_cleaner import (
    normalize_text,
    to_numeric,
    remove_rows_with_nulls,
    remove_duplicates,
)


def clean_client_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["cliente"] = df["cliente"].apply(normalize_text)

    df["client_id"] = to_numeric(df["client_id"])
    df["total_pedidos"] = to_numeric(df["total_pedidos"])
    df["total_comprado"] = to_numeric(df["total_comprado"])

    df = remove_rows_with_nulls(df, ["client_id", "cliente"])

    # quitar clientes sin pedidos o sin compra
    df = df[
        (df["total_pedidos"] > 0) &
        (df["total_comprado"] > 0)
    ].copy()

    df = remove_duplicates(df, ["client_id"])
    df = df.reset_index(drop=True)

    return df