from pydantic_settings import BaseSettings ,SettingsConfigDict

class Settings(BaseSettings):
    QDRANT_ENDPOINT:str
    QDRANT_API_KEY:str
    QDRANT_COLLECTION:str
    HUGGINGFACE_API_KEY:str
    UPLOAD_DIR:str
    HUGGINGFACE_EMBEDDING_MODEL:str
    HUGGINGFACE_LLM_MODEL:str
    HUGGINGFACE_LLM_TASK:str
    HUGGINGFACE_LLM_TEMPERATURE:str
    DATABASE_URL:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()




