# Everything settings related goes here

import os


ROOT_DIR = '/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = (os.environ.get('DEBUG_VALUE') == 'True')

#DATABASES = {}