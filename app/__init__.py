from flask import Flask
from app.config import Config
import logging
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

json_fname = 'survey.json'
results_fname = 'results_{}.csv'.format(datetime.now().strftime('%Y%m%d_%H%M'))
logging.basicConfig(level=logging.INFO)

from app import routes