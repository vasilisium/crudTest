from flask import Flask
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

mongo = PyMongo(app)
Bootstrap(app)
csrf = CSRFProtect(app)

from crudTest import routes