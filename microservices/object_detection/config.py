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
        self.database_settings_test = {
            "NAME": os.getenv("DATABASE_TEST_NAME"),
            "USER": os.getenv("DATABASE_TEST_USER"),
            "PASSWORD": os.getenv("DATABASE_TEST_PASS"),
            "HOST": os.getenv("DATABASE_TEST_HOST"),
            "PORT": os.getenv("DATABASE_TEST_PORT"),
        }
        self.api_key = os.getenv("API_KEY")
        self.redis_config = {
            "REDIS_HOSTNAME": os.environ.get("REDIS_HOSTNAME"),
            "REDIS_PORT": os.environ.get("REDIS_PORT"),
        }

    def get_sync_database_url(self):
        return f"postgresql://{self.database_settings.get('USER')}:{self.database_settings.get('PASSWORD')}@{self.database_settings.get('HOST')}:{self.database_settings.get('PORT')}/{self.database_settings.get('NAME')}"

    def get_sync_database_url_test(self):
        return f"postgresql://{self.database_settings_test.get('USER')}:{self.database_settings_test.get('PASSWORD')}@{self.database_settings_test.get('HOST')}:{self.database_settings_test.get('PORT')}/{self.database_settings_test.get('NAME')}"

    def get_settings(self):
        return self.database_settings

    def get_redis_config(self):
        return self.redis_config

    def get_api_key(self):
        return self.api_key


global_config = Config()
