from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PaperClarity"
    app_env: str = "dev"
    host: str = "0.0.0.0"
    port: int = 8000

    llm_provider: str = "mock"
    llm_base_url: str = "https://api.openai.com/v1"
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    llm_timeout_seconds: int = 30

    data_dir: str = "data"
    cache_dir: str = "data/cache"
    db_path: str = "data/paperclarity.db"

    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_prefix="PC_")


settings = Settings()
