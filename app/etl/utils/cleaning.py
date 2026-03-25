import pandas as pd

def strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove leading and trailing whitespace from all string columns in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to clean.

    Returns
    -------
    pandas.DataFrame
        The cleaned DataFrame.
    """
    df = df.copy()

    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].astype("string").str.strip()

    return df


def uppercase_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Uppercase all values in the specified columns of a DataFrame.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to clean.
    columns : list of str
        The columns to uppercase.

    Returns
    -------
    pandas.DataFrame
        The cleaned DataFrame.
    """
    df = df.copy()

    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype("string").str.upper().str.strip()

    return df

def fill_null_strings(df: pd.DataFrame, columns: list[str], value: str = "") -> pd.DataFrame:
    """
    Fill null values in the specified columns of a DataFrame with the specified value.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to clean.
    columns : list of str
        The columns to fill.
    value : str, default ""
        The value to fill with.

    Returns
    -------
    pandas.DataFrame
        The cleaned DataFrame.
    """
    df = df.copy()

    for col in columns:
        if col in df.columns:
            df[col] = df[col].fillna(value)

    return df

def drop_duplicate_by_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Drop duplicate rows based on the specified columns.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to clean.
    columns : list of str
        The columns to use for identifying duplicates.

    Returns
    -------
    pandas.DataFrame
        The cleaned DataFrame.
    """
    df = df.copy()

    df.drop_duplicates(subset=columns, keep="first", inplace=True)

    return df
   