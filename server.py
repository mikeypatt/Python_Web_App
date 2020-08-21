from flask import Flask
from flask_caching import Cache
server = Flask(__name__)

cache = Cache(server, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': 'cloud-vm-42-77.doc.ic.ac.uk',
    'CACHE_REDIS_PASSWORD': 'UT9y&?_M^&jdAdR6M=QBY#fQJX56u!',
    'CACHE_REDIS_PORT': '6379',
    })

