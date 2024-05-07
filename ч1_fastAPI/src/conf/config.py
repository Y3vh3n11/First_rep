from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):    
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloud_name: str
    api_key: str
    api_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra='ignore'


settings = Settings()
