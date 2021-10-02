import psycopg2
import configparser
import os
import json

SHCEMA_PATH = 'db/schema'

config = configparser.ConfigParser()
config.read('config/db.cfg')
config = config[os.environ['FLASK_ENV']]

db = psycopg2.connect(**config)
cur = db.cursor()


def execute(sql_file):
    sql = open(os.path.join(SHCEMA_PATH, sql_file), 'r')
    cur.execute(sql.read())
    sql.close()

    return cur.fetchall()


def info():
    db_info = dict(config)
    del db_info['password']
    db_info = json.dumps(db_info, sort_keys=True, indent=4, separators=(',', ': '))

    print(' DATABASE INFO '.center(30, '='))
    print(db_info)
    print('=' * 30)


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    records = execute('server.sql')
    print(records)
