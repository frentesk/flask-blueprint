from flask import Flask,Blueprint
#from flask_sqlalchemy import  SQLAlchemy
from config import config


#db=SQLAlchemy()

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    #db.init_app(app)

    from .downloadraster import downloadraster as downloadraster_blueprint
    app.register_blueprint(downloadraster_blueprint)

    from .oauth import oauth as oauth_blueprint
    app.register_blueprint(oauth_blueprint)

    return app

