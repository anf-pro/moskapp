from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")
   
settings=Settings()