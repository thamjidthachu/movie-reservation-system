import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    REDIS_URL = os.getenv('REDIS_URL')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    JWT_SECRET_KEY = "your_jwt_secret_key_here"  # change this!
    SEAT_PRICE = 15
    CURRENCY = 'aed'
    LOCK_DURATION = timedelta(minutes=5)