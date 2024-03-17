import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.urls = {
            "OBJECT_DETECTION_URL": os.getenv("OBJECT_DETECTION_URL"),
        }

    def get_urls(self):
        return self.urls


global_config = Config()
