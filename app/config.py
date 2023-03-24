from pydantic import BaseSettings, PostgresDsn, RedisDsn

DEBUG_MODE = True


class Config(BaseSettings):

    PostgresUrl: PostgresDsn
    RedisUrl: RedisDsn

    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Config()
