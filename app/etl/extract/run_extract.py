from app.core.database import source_engine
from app.etl.extract.extractors import extract_named_dataframe
from app.etl.sql.source_queries import SOURCE_QUERIES


def extract_all_sources() -> dict:
    extracted = {}

    for query_name, query_sql in SOURCE_QUERIES.items():
        extracted[query_name] = extract_named_dataframe(
            source_engine,
            query_name,
            query_sql
        )

    return extracted