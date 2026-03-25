import pandas as pd
from sqlalchemy.engine import Engine


def truncate_table(engine: Engine, table_name: str) -> None:
    with engine.begin() as conn:
        conn.exec_driver_sql(f"TRUNCATE TABLE {table_name}")


def append_dataframe(df: pd.DataFrame, table_name: str, engine: Engine) -> None:
    if df.empty:
        print(f"[LOAD] {table_name}: DataFrame vacío, no se insertó nada.")
        return

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )

    print(f"[LOAD] {table_name}: {len(df)} filas insertadas.")

    