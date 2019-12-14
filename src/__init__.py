from flask import Flask
import os
import inspect

from src.lib import functions, exceptions

app = Flask(__name__)
DB_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/DesTapaIS.db"

from src import routes
