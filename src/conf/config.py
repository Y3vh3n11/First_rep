from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):    
    sqlalchemy_database_url: str = 'postgresql+psycopg2://$postgres:$567234@localhost:$5432/$postgres'
    secret_key: str = 'secret'
    algorithm: str = 'HS'
    mail_username: str = 'myemail@gmail.com'
    mail_password: str = '555'
    mail_from: str = 'myemail@gmail.com'
    mail_port: int = 555
    mail_server: str = 'smtp.meta.ua'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloud_name: str = 'myname'
    api_key: str = '65655'
    api_secret: str = 'sdfsdfb323'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra='ignore'


settings = Settings()
