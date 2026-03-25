import pandas as pd


def to_datetime_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Convert the specified columns of a DataFrame to datetime.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to convert.
    columns : list of str
        The columns to convert.

    Returns
    -------
    pandas.DataFrame
        The converted DataFrame.
    """
    df = df.copy()

    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def add_date_key(df: pd.DataFrame, source_col: str, target_col: str) -> pd.DataFrame:
    """
    Add a date key column to a DataFrame.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to add the column to.
    source_col : str
        The column to use as the source for the date key.
    target_col : str
        The name of the new date key column.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with the new date key column.
    """
    df = df.copy()

    if source_col in df.columns:
        df[target_col] = pd.to_datetime(df[source_col], errors="coerce").dt.strftime("%Y%m%d")
        df[target_col] = pd.to_numeric(df[target_col], errors="coerce").astype("Int64")

    return df