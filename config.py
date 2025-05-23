import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    REDIS_URL = os.getenv('REDIS_URL')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
