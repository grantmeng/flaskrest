HOST = "localhost"
PORT = 5000
DEBUG = True

DB_HOST = 'localhost'
DB_PORT = '5432'
DB_USER = 'postgres'
DB_PASS = 'xxxx'
DB_NAME = 'postgres'
DB_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASS, DB_HOST, DB_NAME)
