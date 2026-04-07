import pandas as pd
from app.business_docs.cleaners.common_cleaner import normalize_text, to_numeric


INVALID_STATES = {
    None,
    "",
    "Seleccione uno...",
    "Seleccione uno",
    "SIN ESTADO",
}


def clean_zone_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["estado"] = df["estado"].apply(normalize_text)

    numeric_cols = [
        "clientes_activos",
        "total_pedidos",
        "ventas_totales",
        "ticket_promedio",
        "participacion_ventas_pct",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = to_numeric(df[col])

    if "ultima_compra_zona" in df.columns:
        df["ultima_compra_zona"] = pd.to_datetime(
            df["ultima_compra_zona"], errors="coerce"
        ).dt.date

    if "nivel_concentracion" in df.columns:
        df["nivel_concentracion"] = df["nivel_concentracion"].apply(normalize_text)

    # quitar estados inválidos
    df = df[~df["estado"].isin(INVALID_STATES)].copy()

    # quitar filas sin datos clave
    df = df.dropna(subset=["estado", "clientes_activos", "ventas_totales"]).copy()

    # valores válidos
    df = df[
        (df["clientes_activos"] > 0) &
        (df["total_pedidos"] >= 0) &
        (df["ventas_totales"] >= 0)
    ].copy()

    df = df.drop_duplicates(subset=["estado"]).copy()
    df = df.reset_index(drop=True)

    return df