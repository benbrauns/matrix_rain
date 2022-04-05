#
import os
import logging
from datetime import datetime

now = datetime.now()
date_hours = now.strftime('%d-%m-%Y_%H-%M-%S')
SRC_DIR = os.path.abspath(os.path.dirname(__file__))
MAIN_DIR = SRC_DIR.rpartition(os.sep)[0]
LOG_DIR = os.path.join(MAIN_DIR, 'logs')
log_name = f'{date_hours}.log'
log_path = os.path.join(LOG_DIR, log_name)

if not os.path.exists(LOG_DIR):
    os.mkdir('logs')
logging.basicConfig(filename=log_path, filemode='w', format='[%(levelname)s] %(message)s', level=logging.DEBUG)