import pandas as pd
from app.etl.utils.cleaning import strip_string_columns, drop_duplicate_by_columns


def transform_dim_client(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the dim_client DataFrame.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to transform.

    Returns
    -------
    pandas.DataFrame
        The transformed DataFrame.
    """
    df = df.copy()

    df = strip_string_columns(df)
    df = drop_duplicate_by_columns(df, ["client_id"])

    expected_columns = [
        "client_id",
        "nombre",
        "apellido",
        "direccion",
        "colonia",
        "ciudad",
        "estado",
        
        "codigo_postal",
        "telefono",
        "correo",
    ]

    df = df[expected_columns]

    return df