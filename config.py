import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    db_host=os.environ.get('db_host')
    ARCTEST = 'k123'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    HOST = '127.0.0.1'
    PORT = 5000
    DEBUG=True

class SQLConfig:
    sql_username='sql'
    sql_password='sql'
    sql_host='127.0.0.1'
    sql_dbname='sql'

class ProductionConfig(Config):
    HOST = '192.168.1.50'
    PORT = 8000
    DEBUG = False


config={
    'development':DevelopmentConfig,
    'production': ProductionConfig,
    'default':DevelopmentConfig
}