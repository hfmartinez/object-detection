import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.database_settings = {
            "NAME": os.getenv("DATABASE_NAME"),
            "USER": os.getenv("DATABASE_USER"),
            "PASSWORD": os.getenv("DATABASE_PASS"),
            "HOST": os.getenv("DATABASE_HOST"),
            "PORT": os.getenv("DATABASE_PORT"),
        }

    def get_sync_database_url(self):
        return f"postgresql://{self.database_settings.get('USER')}:{self.database_settings.get('PASSWORD')}@{self.database_settings.get('HOST')}:{self.database_settings.get('PORT')}/{self.database_settings.get('NAME')}"

    def get_settings(self):
        return self.database_settings


global_config = Config()
