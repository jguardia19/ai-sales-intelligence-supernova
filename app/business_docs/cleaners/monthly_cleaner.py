import pandas as pd
from app.business_docs.cleaners.common_cleaner import normalize_text, to_numeric


def clean_monthly_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["periodo"] = df["periodo"].apply(normalize_text)
    df["pedidos"] = to_numeric(df["pedidos"])
    df["ventas_totales"] = to_numeric(df["ventas_totales"])

    df = df.dropna(subset=["periodo", "pedidos", "ventas_totales"]).copy()

    # quitar ventas o pedidos negativos
    df = df[
        (df["pedidos"] >= 0) &
        (df["ventas_totales"] >= 0)
    ].copy()

    # quitar duplicados de periodo
    df = df.drop_duplicates(subset=["periodo"]).copy()

    df = df.sort_values("periodo").reset_index(drop=True)

    return df
