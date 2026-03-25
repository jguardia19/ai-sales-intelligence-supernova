import pandas as pd
from sqlalchemy.engine import Engine

def extract_dataframe(engine: Engine, query: str) -> pd.DataFrame:
    return pd.read_sql_query(query, con=engine)

def extract_named_dataframe(engine: Engine, name: str, query: str) -> pd.DataFrame:
    print(f"[extract] Extracting: {name}")
    df = pd.read_sql_query(query, con=engine)
    print(f"[extract] {name} -> {len(df)} rows")
    return df