import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'not-a-secure-secret-key'