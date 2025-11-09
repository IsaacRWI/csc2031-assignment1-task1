import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SECRET_KEY = os.environ.get("SECRET")  # SECRET = "devkey123"
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = True

# config_test = Config()
# print(config_test.SECRET_KEY)