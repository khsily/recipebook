from flask import Flask, request
import os

from routes import api
import db

config = {
    'host': os.environ['SERVER_HOST'],
    'port': os.environ['SERVER_PORT'],
    'threaded': True,
}


@api.get("/test_db")
def db_info():
    body = request.json
    print(body, flush=True)
    info = db.execute('server.sql')[0]['version']
    return info


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
