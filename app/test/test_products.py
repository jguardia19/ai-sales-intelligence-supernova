from app.core.database import source_engine
from app.etl.extract.extractors import extract_named_dataframe
from app.etl.sql.source_queries import DOCUMENT_QUERIES
from app.business_docs.services.products_top_dataset_transformer import transform_product_dataset
from app.business_docs.generators.products_top_documents import generate_product_documents

def run():

    extracted_dataframes = {}

    for query_name, query_sql in DOCUMENT_QUERIES.items():
        df = extract_named_dataframe(source_engine, query_name, query_sql)
        extracted_dataframes[query_name] = df

        print("=" * 80)
        print(f"DATAFRAME: {query_name}")
        print(df.head())
        print(df.info())
        print("=" * 80)


    return extracted_dataframes

df = run()

df_transformed = transform_product_dataset(df["top_products"])

documents = generate_product_documents(df_transformed)

print(documents[0]["content"])



# if __name__ == "__main__":
#     run()