import pandas as pd
from app.business_docs.cleaners.common_cleaner import normalize_upper_text, to_numeric


def clean_channel_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["canal"] = df["canal"].apply(normalize_upper_text)
    df["pedidos"] = to_numeric(df["pedidos"])
    df["ventas_totales"] = to_numeric(df["ventas_totales"])

    if "ticket_promedio" in df.columns:
        df["ticket_promedio"] = to_numeric(df["ticket_promedio"])

    df = df.dropna(subset=["canal", "pedidos", "ventas_totales"]).copy()

    df = df[
        (df["pedidos"] > 0) &
        (df["ventas_totales"] > 0)
    ].copy()

    df = df.drop_duplicates(subset=["canal"]).copy()
    df = df.reset_index(drop=True)

    return df