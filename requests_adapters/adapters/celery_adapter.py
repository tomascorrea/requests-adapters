# -*- encoding: utf-8 -*-

import json
from requests import Response
from requests.compat import urlparse, StringIO
from requests.adapters import BaseAdapter
from requests.hooks import dispatch_hook
from celery.execute import send_task


def build_response(request, data, code, encoding):
    '''Builds a response object from the data returned by ftplib, using the
    specified encoding.'''
    response = Response()

    response.encoding = encoding

    # Fill in some useful fields.

    raw = StringIO()
    raw.write(data)
    raw.seek(0)

    response.raw = raw
    response.url = request.url
    response.request = request
    response.status_code = code


    # Run the response hook.
    response = dispatch_hook('response', request.hooks, response)
    return response



class CeleryAdapter(BaseAdapter):
    '''
    Use the celery send_task to send a "wsgi" request to some server.
    The server that will handle this task need to run the 
    '''

    def _get_queue_name_from_request(self, request):
        """
        By convention the queue name will be the host name
        """
        queue = request.url.replace('celery://', '').replace(request.path_url, '')

    def send(self, request, **kwargs):
        queue = self._get_queue_name_from_request(request)
        task_response = send_task("request_adapters.requests_adapters_process_request", args=[request], kwargs=kwargs, queue=queue)

        data = json.dumps({'task-id': str(task_response)})
        return build_response(request, data, 200, 'ascii')

        