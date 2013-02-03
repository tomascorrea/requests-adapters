requests-adapters
=================

Study of create adpater to use the super clean API of request to send a UWSIG request over a faster trasport like rabbitmq+celery or zeromq

this is simple example, of course you need to have a celery configurated and rabbit running



import request
from requests_adapters.adapters import CeleryAdapter

celery = Celery()

class Config:
    CELERY_ENABLE_UTC = True
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


celery.config_from_object(Config)

s = requests.Session()
s.mount('celery://', CeleryAdapter())

self.s.post('celery://myservice.com/resource')