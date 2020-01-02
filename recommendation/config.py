import os


class Config:
    
    SECRET_KEY = 'c2bf943e2d8c88bccd3a58dd103c3a40'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///recommendation'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
class ProductionConfig(Config):
    DEUG =  False