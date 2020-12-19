#!/usr/bin/env python3.7

import sys

import psycopg2
import environ

env = environ.Env()

try:
    db_settings = env.db('DATABASE_URL')
    psycopg2.connect(
        dbname=db_settings['NAME'],
        user=db_settings['USER'],
        password=db_settings['PASSWORD'],
        host=db_settings['HOST'],
        port=db_settings['PORT'] or 5432,
    )
except psycopg2.OperationalError as e:
    print(e)
    sys.exit(-1)

sys.exit(0)
