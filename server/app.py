from flask import Flask
import os

from routes import api
import db

config = {
    'host': os.environ['SERVER_HOST'],
    'port': os.environ['SERVER_PORT'],
}


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
