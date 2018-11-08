import os
import pymongo

class Config(object):
    BOOTSTRAP_SERVE_LOCAL = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    MONGO_URI = "mongodb://localhost:27017/crudT"

    sortOrder = pymongo.DESCENDING
    tablePagitation = {
        'limit': {
            'key': 'limit',
            'val': 10
        },
        'skip': 'skip' 
        
    }