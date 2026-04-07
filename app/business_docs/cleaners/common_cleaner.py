import re
import pandas as pd


INVALID_TEXT_VALUES = {
    "",
    "none",
    "null",
    "nan",
    "n/a",
    "na",
    "sin dato",
    "seleccione uno...",
    "seleccione uno",
}


def normalize_text(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if not value:
        return None

    # quitar espacios repetidos
    value = re.sub(r"\s+", " ", value)

    # corregir caracteres invisibles comunes
    value = value.replace("\u00a0", " ").strip()

    if value.lower() in INVALID_TEXT_VALUES:
        return None

    return value


def normalize_upper_text(value):
    value = normalize_text(value)
    return value.upper() if value else None


def normalize_title_text(value):
    value = normalize_text(value)
    return value.title() if value else None


def to_numeric(series):
    return pd.to_numeric(series, errors="coerce")


def remove_rows_with_nulls(df: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
    return df.dropna(subset=required_columns).copy()


def remove_duplicates(df: pd.DataFrame, subset: list[str]) -> pd.DataFrame:
    return df.drop_duplicates(subset=subset).copy()


def apply_text_normalization(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(normalize_text)
    return df