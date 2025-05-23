class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@db:5432/movies'
    REDIS_URL = 'redis://redis:6379/0'
    STRIPE_SECRET_KEY = 'your_stripe_secret_key'
