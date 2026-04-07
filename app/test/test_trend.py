from app.core.database import source_engine
from app.etl.extract.extractors import extract_named_dataframe
from app.etl.sql.source_queries import TREND_QUERIES
from app.business_docs.services.trend_dataset_transformer import transform_monthly_trends_dataset
from app.business_docs.generators.trend_documents import generate_trend_documents

def run():

    extracted_dataframes = {}

    for query_name, query_sql in TREND_QUERIES.items():
        df = extract_named_dataframe(source_engine, query_name, query_sql)
        extracted_dataframes[query_name] = df

        print("=" * 80)
        print(f"DATAFRAME: {query_name}")
        print(df.head())
        print(df.info())
        print("=" * 80)


    return extracted_dataframes

df = run()

df_transformed = transform_monthly_trends_dataset(df["monthly_sales_trend"])

documents = generate_trend_documents(df_transformed)

print(documents[1]["content"])



# if __name__ == "__main__":
#     run()