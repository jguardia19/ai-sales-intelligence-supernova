import pandas as pd

def normalize_text_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    return df