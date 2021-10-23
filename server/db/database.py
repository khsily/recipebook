import psycopg2
import psycopg2.extras
import os
import json

SHCEMA_PATH = 'db/schema'

config = {
    'host': os.environ['POSTGRES_HOST'],
    'dbname': os.environ['POSTGRES_DB'],
    'user': os.environ['POSTGRES_USER'],
    'password': os.environ['POSTGRES_PASSWORD'],
    'port': os.environ['POSTGRES_PORT'],
}

db = psycopg2.connect(**config)
cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def execute(sql_file, params=None):
    sql = open(os.path.join(SHCEMA_PATH, sql_file), 'r')
    cur.execute(sql.read(), params)
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
    records = execute('server.sql')
    print(records)
