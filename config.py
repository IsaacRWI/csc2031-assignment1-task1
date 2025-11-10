import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SECRET_KEY = os.environ.get("SECRET")  # SECRET = "devkey123" in .env
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = True  # csrf = true

# config_test = Config()
# print(config_test.SECRET_KEY)