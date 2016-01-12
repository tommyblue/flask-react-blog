from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_file = "./test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(db_file)
db = SQLAlchemy(app)
index = 1
