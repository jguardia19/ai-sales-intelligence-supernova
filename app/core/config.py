from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    app_name: str = "AI Sales Intelligence"
    app_env: str = "development"
    app_debug: bool = True

    source_db_host: str
    source_db_port: int = 3306
    source_db_user: str
    source_db_password: str
    source_db_name: str

    warehouse_db_host: str
    warehouse_db_port: int = 3306
    warehouse_db_user: str
    warehouse_db_password: str
    warehouse_db_name: str

    openai_api_key: str
    chroma_persist_dir: str = "./chroma_storage"
    chroma_collection_name: str = "ai_sales_supernova"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()