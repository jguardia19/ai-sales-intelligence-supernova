import pandas as pd

def transform_zone_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["ventas_totales"] = pd.to_numeric(df["ventas_totales"], errors="coerce")
    df["clientes_activos"] = pd.to_numeric(df["clientes_activos"], errors="coerce")

    # ranking por ventas
    df = df.sort_values("ventas_totales", ascending=False).reset_index(drop=True)
    df["ranking_estado"] = df.index + 1

    total_ventas = df["ventas_totales"].sum()

    # recalcular participación por seguridad
    df["participacion_pct"] = (df["ventas_totales"] / total_ventas) * 100

    # clasificar nivel comercial
    def classify_zone(row):
        if row["ranking_estado"] <= 3:
            return "ZONA CLAVE"
        elif row["ranking_estado"] <= 10:
            return "ZONA IMPORTANTE"
        else:
            return "ZONA SECUNDARIA"
        
    def classify_concentration(row):
        if row["clientes_activos"] >= 300:
            return "ALTA CONCENTRACION"
        elif row["clientes_activos"] >= 100:
            return "CONCENTRACION MEDIA"
        else:
            return "BAJA CONCENTRACION"

    df["nivel_comercial"] = df.apply(classify_zone, axis=1)
    df["nivel_concentracion"] = df.apply(classify_concentration, axis=1)

    return df