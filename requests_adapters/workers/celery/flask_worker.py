# -*- encoding: utf-8 -*-

"""
A simple celery task that make a uwsig call to flask
"""

from requests.compat import StringIO

from flask import current_app as flask_current_app
from celery import current_app as celery_current_app


@celery_current_app.task(name='request_adapters.requests_adapters_process_request')
def requests_adapters_process_request(request, **kwargs):

    with flask_current_app.app_context():

        environ = {'SERVER_NAME':'localhost'}
        environ['wsgi.url_scheme'] = 'http'
        environ['SERVER_PORT'] = '80'
        environ['PATH_INFO'] = request.path_url
        environ['REQUEST_METHOD'] = request.method
        environ['CONTENT_LENGTH'] = request.headers.get('Content-Length')
        environ['CONTENT_TYPE'] = request.headers.get('Content-Type')

        body = StringIO()
        body.write(request.body)
        body.seek(0)

        environ['wsgi.input'] = body

        context_request = flask_current_app.request_context(environ)
        context_request.push()

        flask_current_app.dispatch_request()
