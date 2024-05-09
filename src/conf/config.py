from pydantic import ConfigDict
from pydantic_settings import BaseSettings
import os
from pathlib import Path

dot_env_path = Path(__file__).parent.parent/".env"

class Settings(BaseSettings):    
    sqlalchemy_database_url: str 
    secret_key: str 
    algorithm: str 
    mail_username: str 
    mail_password: str 
    mail_from: str 
    mail_port: int 
    mail_server: str 
    redis_host: str 
    redis_port: int 
    cloud_name: str 
    api_key: str 
    api_secret: str 


    class Config:
        env_file = dot_env_path
        env_file_encoding = "utf-8"
        extra='ignore'


settings = Settings()
