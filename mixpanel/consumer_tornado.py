__author__ = 'Fredrik Svensson'

import base64
import json
import urllib.parse
from tornado.httpclient import AsyncHTTPClient
import mixpanel


class AsyncConsumer(mixpanel.Consumer):
    """Sends requests directly using AsyncHTTPClient."""
    def _write_request(self, request_url, json_message):
        def handle_request(response):
            if response.error:
                raise mixpanel.MixpanelException(response.error)
            else:
                try:
                    response = json.loads(response.body.decode('utf-8'))
                except ValueError:
                    raise mixpanel.MixpanelException('Cannot interpret Mixpanel server response: {0}'.format(response))

                if response['status'] != 1:
                    raise mixpanel.MixpanelException('Mixpanel error: {0}'.format(response['error']))

        data = urllib.parse.urlencode({
            'data': base64.b64encode(json_message.encode('utf-8')),
            'verbose': 1,
            'ip': 0
        }).encode('utf-8')

        http_client = AsyncHTTPClient()
        http_client.fetch(request_url, handle_request, method='POST', body=data)


class BufferedAsyncConsumer(mixpanel.BufferedConsumer):
    """Same as BufferedConsumer but uses AsyncConsumer as base.

    TODO: How to flush? Give example code!
    """
    def __init__(self, max_size=50, events_url=None, people_url=None):
        self._consumer = AsyncConsumer(events_url, people_url)
        self._buffers = {
            'events': [],
            'people': [],
        }
        self._max_size = min(50, max_size)
