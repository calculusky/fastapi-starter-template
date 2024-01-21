from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache

load_dotenv()

class Settings(BaseSettings):
    jwt_secret: str
    jwt_token_expire: int = 30
    database_url: str
    dev_environment: bool = False
    allowed_domains: str | None = None
    

@lru_cache    
def validate_settings():
    settings = Settings()
    settings.allowed_domains = settings.allowed_domains.split(",") if settings.allowed_domains else ["*"]
    return settings

settings = validate_settings()

