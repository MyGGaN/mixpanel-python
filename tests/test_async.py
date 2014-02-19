__author__ = 'Fredrik Svensson'

# TODO:
# - Add negative test cases
# - Add tests with unicode chars
# - Test so Exceptions are raised

import contextlib
from unittest.mock import MagicMock, patch
import mixpanel
from mixpanel.consumer_tornado import AsyncConsumer, BufferedAsyncConsumer
import unittest
import urllib.parse
import base64
import json

try:
    import tornado.testing
    from tornado.concurrent import TracebackFuture
    from tornado import stack_context
except ImportError:
    tornado_loaded = False
else:
    tornado_loaded = True


@unittest.skipUnless(tornado_loaded, "tornado module not loaded")
class AsyncTest(tornado.testing.AsyncTestCase):
    def mock_fetch(self, request, callback=None, **kwargs):
        future = TracebackFuture()
        if callback is not None:
            callback = stack_context.wrap(callback)

            def handle_future(future):
                response = future.result()
                self.io_loop.add_callback(callback, response)
            future.add_done_callback(handle_future)

        res = MagicMock()
        future.set_result(res)

        return future

class ConsumerAsyncTestCase(AsyncTest):
    def setUp(self):
        super(ConsumerAsyncTestCase, self).setUp()
        self.consumer = AsyncConsumer()

    @contextlib.contextmanager
    def _assertSends(self, expect_url, expect_data):

        with patch('tornado.httpclient.AsyncHTTPClient.fetch',
                   return_value=self.mock_fetch) as http_client:
            yield

            self.assertEqual(http_client.call_count, 1)
            ((url, _), req) = http_client.call_args
            self.assertEqual(url, expect_url)
            body = req['body'].decode('utf-8')
            self.assertEqual(set(body.split('&')),
                             set(expect_data.split('&')))

    @tornado.testing.gen_test
    def test_send_events(self):
        with self._assertSends('https://api.mixpanel.com/track', 'ip=0&data=IkV2ZW50Ig%3D%3D&verbose=1'):
            self.consumer.send('events', '"Event"')

    @tornado.testing.gen_test
    def test_send_people(self):
        with self._assertSends('https://api.mixpanel.com/engage','ip=0&data=IlBlb3BsZSI%3D&verbose=1'):
            self.consumer.send('people', '"People"')


class FunctionalAsyncTestCase(AsyncTest):
    def setUp(self):
        super(FunctionalAsyncTestCase, self).setUp()
        self.TOKEN = '12345'
        self.mp = mixpanel.Mixpanel(self.TOKEN, consumer=AsyncConsumer())
        self.mp._now = lambda : 1000

    @contextlib.contextmanager
    def _assertRequested(self, expect_url, expect_data):
        with patch('tornado.httpclient.AsyncHTTPClient.fetch',
                   return_value=self.mock_fetch) as http_client:
            yield

            self.assertEqual(http_client.call_count, 1)
            ((url, _), req) = http_client.call_args
            self.assertEqual(url, expect_url)
            body = req['body'].decode('utf-8')
            data = urllib.parse.parse_qs(req['body'].decode('utf-8'))
            self.assertEqual(len(data['data']), 1)
            payload_encoded = data['data'][0]
            payload_json = base64.b64decode(payload_encoded).decode('utf-8')
            payload = json.loads(payload_json)
            self.assertEqual(payload, expect_data)

    @tornado.testing.gen_test
    def test_track_functional(self):
        expect_data = {'event': {'color': 'blue', 'size': 'big'}, 'properties': {'mp_lib': 'python', 'token': self.TOKEN, 'distinct_id': 'button press', '$lib_version': mixpanel.VERSION, 'time': 1000}}
        with self._assertRequested('https://api.mixpanel.com/track', expect_data):
            self.mp.track('button press', {'size': 'big', 'color': 'blue'})


    @tornado.testing.gen_test
    def test_people_set_functional(self):
        expect_data = {'$distinct_id': 'amq', '$set': {'birth month': 'october', 'favorite color': 'purple'}, '$time': 1000000, '$token': self.TOKEN}
        with self._assertRequested('https://api.mixpanel.com/engage', expect_data):
             self.mp.people_set('amq', {'birth month': 'october', 'favorite color': 'purple'})


class BufferedConsumerAsyncTestCase(AsyncTest):
    def setUp(self):
        super(BufferedConsumerAsyncTestCase, self).setUp()
        self.MAX_LENGTH = 10
        self.consumer = BufferedAsyncConsumer(self.MAX_LENGTH)

    def test_buffer_hold_and_flush(self):
        with patch('tornado.httpclient.AsyncHTTPClient.fetch',
                   return_value=self.mock_fetch) as http_client:
            self.consumer.send('events', '"Event"')
            self.assertEqual(http_client.call_count, 0)

            self.consumer.flush()

            self.assertEqual(http_client.call_count, 1)
            ((url, _), req) = http_client.call_args
            self.assertEqual(url, 'https://api.mixpanel.com/track')
            body = req['body'].decode('utf-8')
            self.assertEqual(set(body.split('&')),
                             set('ip=0&data=WyJFdmVudCJd&verbose=1'.split('&')))

    def test_buffer_fills_up(self):
        with patch('tornado.httpclient.AsyncHTTPClient.fetch',
                   return_value=self.mock_fetch) as http_client:
            for i in range(self.MAX_LENGTH - 1):
                self.consumer.send('events', '"Event"')
            self.assertEqual(http_client.call_count, 0)

            self.consumer.send('events', '"Last Event"')

            self.assertEqual(http_client.call_count, 1)
            ((url, _), req) = http_client.call_args
            self.assertEqual(url, 'https://api.mixpanel.com/track')
            body = req['body'].decode('utf-8')
            self.assertEqual(set(body.split('&')),
                             set('ip=0&data=WyJFdmVudCIsIkV2ZW50IiwiRXZlbnQiLCJFdmVudCIsIkV2ZW50IiwiRXZlbnQiLCJFdmVudCIsIkV2ZW50IiwiRXZlbnQiLCJMYXN0IEV2ZW50Il0%3D&verbose=1'.split('&')))


if __name__ == "__main__":
    unittest.main()
