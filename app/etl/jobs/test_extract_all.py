from app.core.database import source_engine
from app.etl.extract.extractors import extract_named_dataframe
from app.etl.sql.source_queries import SOURCE_QUERIES


def run():
    extracted_dataframes = {}

    for query_name, query_sql in SOURCE_QUERIES.items():
        df = extract_named_dataframe(source_engine, query_name, query_sql)
        extracted_dataframes[query_name] = df

        print("=" * 80)
        print(f"DATAFRAME: {query_name}")
        print(df.head())
        print(df.info())
        print("=" * 80)

    return extracted_dataframes


if __name__ == "__main__":
    run()