from app.core.database import source_engine
from app.etl.extract.extractors import extract_named_dataframe
from app.etl.sql.source_queries import QUERY_MONTH
from app.business_docs.services.monthly_trend_transformer import transform_monthly_trends
from app.business_docs.generators.monthly_trend_documents import generate_monthly_documents



def run():

    extracted_dataframes = {}

    for query_name, query_sql in QUERY_MONTH.items():
        df = extract_named_dataframe(source_engine, query_name, query_sql)
        extracted_dataframes[query_name] = df

        print("=" * 80)
        print(f"DATAFRAME: {query_name}")
        print(df.head())
        print(df.info())
        print("=" * 80)


    return extracted_dataframes

df = run()

df_transformed = transform_monthly_trends(df["sales_by_month"])

documents = generate_monthly_documents(df_transformed)

print(documents[0]["content"])



# if __name__ == "__main__":
#     run()