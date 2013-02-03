requests-adapters
=================

Study of create adpater to use the **super clean** API of [requests](http://docs.python-requests.org/en/latest/) to send a WSGI request over a faster trasport like rabbitmq+celery or zeromq - this first POC implements a adapter and a celery task.

this is simple example, of course you need to have a celery configurated and rabbit running


#### imports.

	import request
	from requests_adapters.adapters import CeleryAdapter

#### celery configuration.

	celery = Celery()

	class Config:
    	CELERY_ENABLE_UTC = True
    	BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    	CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

	celery.config_from_object(Config)

#### mounting the adapter.

	s = requests.Session()
	s.mount('celery://', CeleryAdapter())

#### actualy making a request.

	s.post('celery://myservice.com/resource')