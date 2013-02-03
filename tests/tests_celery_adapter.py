# -*- encoding: utf-8 -*-

import unittest
import requests
import time
from celery import Celery

from flask import Flask, request

from requests_adapters.adapters import CeleryAdapter
from requests_adapters.workers.celery import flask_worker


# Flask simple page
app = Flask(__name__)

@app.route("/resource", methods=['POST'])
def resource():
    count = 1
    for a in range(30000):
        count = count + a
    print 'doing some work'
    print request.form.get('name')
    return 'Ok'


app.app_context().push()

celery = Celery()


class Config:
    CELERY_ENABLE_UTC = True
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


celery.config_from_object(Config)



class CeleryAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.s = requests.Session()
        self.s.mount('celery://', CeleryAdapter())

    def test_simple(self):
        response = self.s.post('celery://myservice.com/resource')
        self.assertTrue(response.json().get('task-id'))

    def test_post_with_data(self):
        response = self.s.post('celery://myservice.com/resource', data={'name':'name'})
        self.assertTrue(response.json().get('task-id'))

    def test_many(self):
        for a in range(10000):
            response = self.s.post('celery://myservice.com/resource', data={'name':'name'})
            self.assertTrue(response.json().get('task-id'))

