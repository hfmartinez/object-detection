import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.urls = {
            "OBJECT_DETECTION_URL": os.getenv("OBJECT_DETECTION_URL"),
            "REPORTS_URL": os.getenv("REPORTS_URL"),
        }
        self.jwt_config = {
            "SECRET_KEY": os.getenv("SECRET_KEY"),
            "ALGORITHM": os.getenv("ALGORITHM"),
            "ACCESS_TOKEN_EXPIRE_MINUTES": os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
        }
        self.api_key = os.getenv("API_KEY")

    def get_urls(self):
        return self.urls

    def get_jwt_config(self):
        return self.jwt_config

    def get_api_key(self):
        return self.api_key


global_config = Config()
