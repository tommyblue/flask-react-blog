from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# db_file = "./test.db"
# db_conf = "sqlite:///{}".format(db_file)
try:
    password = os.environ['POSTGRES_ENV_POSTGRES_PASSWORD']
except:
    password = ''

try:
    port = os.environ['POSTGRES_PORT_5432_TCP_PORT']
except:
    port = '5432'

try:
    host = os.environ['POSTGRES_PORT_5432_TCP_ADDR']
except:
    host = 'localhost'

db_conf = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'.format(
    host=host,
    port=port,
    db='postgres',
    user='postgres',
    password=password
)
app.config['SQLALCHEMY_DATABASE_URI'] = db_conf
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
