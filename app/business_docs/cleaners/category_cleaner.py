import pandas as pd
from app.business_docs.cleaners.common_cleaner import (
    normalize_text,
    to_numeric,
    remove_rows_with_nulls,
    remove_duplicates,
)


def clean_category_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["categoria"] = df["categoria"].apply(normalize_text)
    df["subcategoria_id"] = to_numeric(df["subcategoria_id"])
    df["unidades_vendidas"] = to_numeric(df["unidades_vendidas"])
    df["monto_vendido"] = to_numeric(df["monto_vendido"])

    # opcional: reemplazar nulos por etiqueta controlada
    df["categoria"] = df["categoria"].fillna("SIN_CATEGORIA")

    df = remove_rows_with_nulls(df, ["subcategoria_id"])

    df = df[
        (df["unidades_vendidas"] >= 0) &
        (df["monto_vendido"] >= 0)
    ].copy()

    df = remove_duplicates(df, ["subcategoria_id"])
    df = df.reset_index(drop=True)

    return df