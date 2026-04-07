from app.core.database import source_engine
from app.etl.extract.extractors import extract_named_dataframe
from app.etl.sql.source_queries import QUERY_ZONE
from app.business_docs.services.zone_dataset_transformer import transform_zone_dataset
from app.business_docs.generators.zone_documents import generate_zone_documents



def run():

    extracted_dataframes = {}

    for query_name, query_sql in QUERY_ZONE.items():
        df = extract_named_dataframe(source_engine, query_name, query_sql)
        extracted_dataframes[query_name] = df

        print("=" * 80)
        print(f"DATAFRAME: {query_name}")
        print(df.head())
        print(df.info())
        print("=" * 80)


    return extracted_dataframes

df = run()

df_transformed = transform_zone_dataset(df["sales_by_state"])

documents = generate_zone_documents(df_transformed)

print(documents[0]["content"])



# if __name__ == "__main__":
#     run()