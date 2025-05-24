import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    REDIS_URL = os.getenv('REDIS_URL')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    FRONTEND_URl='http://127.0.0.1:3000'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEAT_PRICE = 1500
    CURRENCY = 'aed'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    LOCK_DURATION = timedelta(minutes=5)