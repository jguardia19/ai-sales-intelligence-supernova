import pandas as pd


def transform_dead_stock_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["stock"] = pd.to_numeric(df["stock"], errors="coerce")
    df = df.sort_values("stock", ascending=False).reset_index(drop=True)
    df["ranking_stock"] = df.index + 1

    def classify_alert(stock):
        if pd.isna(stock):
            return "SIN DATO"
        if stock >= 1000:
            return "CRITICA"
        if stock >= 200:
            return "ALTA"
        if stock >= 50:
            return "MEDIA"
        return "BAJA"

    def classify_risk(stock):
        if pd.isna(stock):
            return "NO DETERMINADO"
        if stock >= 1000:
            return "CAPITAL INMOVILIZADO ALTO"
        if stock >= 200:
            return "SOBRESTOCK SIN ROTACION"
        if stock >= 50:
            return "PRODUCTO ESTANCADO"
        return "ESTANCAMIENTO LEVE"

    def build_recommendation(stock):
        if pd.isna(stock):
            return "Revisar manualmente el producto."
        if stock >= 1000:
            return "Evaluar liquidación, campaña comercial o redistribución urgente."
        if stock >= 200:
            return "Evaluar promoción, bundle o redistribución entre almacenes."
        if stock >= 50:
            return "Analizar visibilidad comercial y posible promoción."
        return "Monitorear comportamiento del producto y revisar catálogo."

    df["nivel_alerta"] = df["stock"].apply(classify_alert)
    df["tipo_riesgo"] = df["stock"].apply(classify_risk)
    df["recomendacion"] = df["stock"].apply(build_recommendation)

    return df