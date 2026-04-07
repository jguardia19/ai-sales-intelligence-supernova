import pandas as pd
from app.business_docs.cleaners.common_cleaner import (
    normalize_text,
    to_numeric,
    remove_rows_with_nulls,
    remove_duplicates,
)


def clean_dead_stock_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["codigo"] = df["codigo"].apply(normalize_text)
    df["nombre"] = df["nombre"].apply(normalize_text)

    df["product_id"] = to_numeric(df["product_id"])
    df["stock"] = to_numeric(df["stock"])

    df = remove_rows_with_nulls(df, ["product_id", "codigo", "nombre"])

    # solo stock positivo
    df = df[df["stock"] > 0].copy()

    df = remove_duplicates(df, ["product_id"])
    df = df.reset_index(drop=True)

    return df