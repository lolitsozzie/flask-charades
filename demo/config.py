from decouple import config


class Config:
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.DEBUG = config('DEBUG', cast=bool, default=True)
        if self.DEBUG is False:
            self.ENV = 'production'
