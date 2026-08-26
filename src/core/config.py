from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = { "env_file": ".env", "extra": "ignore"}
    APP_NAME: str = 'api'
    PROFILE: str = 'dev'
    DATABASE_URL: str
    REDIS_SERVER: str
    APP_VERSION: str
    PREFIX_ROUTER: str
    CICLO_BASE_URL: str
    CICLO_API_KEY: str 
    CICLO_CACHE_TTL: int
    FRONTEND_URL: str

settings = Settings()