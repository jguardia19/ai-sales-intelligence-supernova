import math
import numpy as np
import pandas as pd


def clean_json_value(value):
    if pd.isna(value):
        return None

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.floating,)):
        return float(value)

    if hasattr(value, "isoformat"):
        return value.isoformat()

    return value


def clean_document_for_json(document: dict) -> dict:
    cleaned = {}

    for key, value in document.items():
        if isinstance(value, dict):
            cleaned[key] = {
                sub_key: clean_json_value(sub_value)
                for sub_key, sub_value in value.items()
            }
        else:
            cleaned[key] = clean_json_value(value)

    return cleaned