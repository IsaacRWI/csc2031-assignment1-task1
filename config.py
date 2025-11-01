import os
import dotenv
class Config:
    SECRET_KEY = os.environ.get("SECRET")  # SECRET = "devkey123"
    DEBUG = True
    TESTING = True