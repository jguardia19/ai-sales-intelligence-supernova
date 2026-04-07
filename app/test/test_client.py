from app.core.database import source_engine
from app.etl.extract.extractors import extract_named_dataframe
from app.etl.sql.source_queries import QUERY_CLIENT
from app.business_docs.services.client_dataset_transformer import transform_client_dataset
from app.business_docs.generators.clients_documents import generate_client_documents


def run():

    extracted_dataframes = {}

    for query_name, query_sql in QUERY_CLIENT.items():
        df = extract_named_dataframe(source_engine, query_name, query_sql)
        extracted_dataframes[query_name] = df

        print("=" * 80)
        print(f"DATAFRAME: {query_name}")
        print(df.head())
        print(df.info())
        print("=" * 80)


    return extracted_dataframes

df = run()

df_transformed = transform_client_dataset(df["top_clients"])

documents = generate_client_documents(df_transformed)

print(documents[0]["content"])



# if __name__ == "__main__":
#     run()