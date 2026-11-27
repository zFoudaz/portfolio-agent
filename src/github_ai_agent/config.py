from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import find_dotenv

class Settings(BaseSettings):
    GROQ_API_KEY:str 
    DB_HOST:str
    DB_PORT:int
    DB_NAME:str
    DB_USERNAME:str
    DB_PASSWORD:str
    origins:list
    model_config = SettingsConfigDict(env_file=find_dotenv(), extra='ignore')

settings = Settings()

DB_CONN_DICT = {
    'dbname':settings.DB_NAME,
    'user':settings.DB_USERNAME,
    'password':settings.DB_PASSWORD,
    'host':settings.DB_HOST,
    'port':settings.DB_PORT
}