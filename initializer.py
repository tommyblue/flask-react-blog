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

db_conf = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'.format(
    host=os.environ['POSTGRES_PORT_5432_TCP_ADDR'],
    port=os.environ['POSTGRES_PORT_5432_TCP_PORT'],
    db='postgres',
    user='postgres',
    password=password
)
app.config['SQLALCHEMY_DATABASE_URI'] = db_conf
db = SQLAlchemy(app)
