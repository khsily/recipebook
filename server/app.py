from flask import Flask
import configparser

from routes import api
import db

config = configparser.ConfigParser()
config.read('config/server.cfg')
config = config['default']


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    return app


if __name__ == '__main__':
    # check database connection
    db.info()

    # create server
    app = create_app()
    app.run(**config)
