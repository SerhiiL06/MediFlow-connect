import os

from dotenv import load_dotenv

load_dotenv()


class SQLAlhemySettings:
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    @property
    def get_async_url(self):
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")


settings = Settings()

sqlsetting = SQLAlhemySettings()
