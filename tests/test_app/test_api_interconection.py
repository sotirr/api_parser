import unittest
from unittest.mock import patch
from datetime import datetime
import json
from importlib import resources
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

from api_parser.common.api_amr import AmrApiRequester


class TestApiIntercon(unittest.TestCase):
    @patch('api_parser.common.api_amr.requests.post')
    def test_auth(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = [
            {
                "1": "key",
                "2": "sessionId"
            },
            {
                "1": "key_value",
                "2": "sessionId_value"
            }
        ]
        api_parser = AmrApiRequester()
        api_parser.auth(user='user', password='password', auth_url='auth_url.ru')

        # test request parameters
        exp_headers = {'Content-Type': 'application/json'}
        exp_payload = {'name': 'user', 'password': 'password', 'role': ''}
        req_args, req_kwargs = mock_request.call_args
        self.assertEqual(req_args[0], 'auth_url.ru')
        self.assertEqual(req_kwargs['headers'], exp_headers)
        self.assertEqual(req_kwargs['json'], exp_payload)
        # test response handling
        self.assertEqual(api_parser.key, 'key_value')
        self.assertEqual(api_parser.session_id, 'sessionId_value')

    @patch('api_parser.common.api_amr.requests.post')
    def test_getting_data(self, mock_request):
        mock_request.return_value.status_code = 200
        with resources.open_text('tests.resources', 'resp_example.json') as data_json:
            resp_json = json.load(data_json)
        mock_request.return_value.json.return_value = resp_json

        api_parser = AurApiRequester()
        api_parser.key = 'key'
        api_parser.session_id = 'session_id'

        strt_time = datetime(2020, 11, 24)
        end_time = datetime(2020, 11, 25)
        card_status = '2'
        data = api_parser.get_data('data_url.ru', strt_time, end_time, card_status)
        # test request parameters
        exp_headers = {'Content-Type': 'application/json'}
        exp_payload_params = ["'24.11.2020'", "'25.11.2020'", "'00:00'", "'00:00'"]
        req_args, req_kwargs = mock_request.call_args
        self.assertEqual(req_args[0], 'data_url.ru')
        self.assertEqual(req_kwargs['headers'], exp_headers)
        self.assertEqual(req_kwargs['json']['id'], 'session_id')
        self.assertEqual(req_kwargs['json']['key'], 'key')
        self.assertEqual(req_kwargs['json']['query'], 1809)
        self.assertEqual(req_kwargs['json']['params'][6:10], exp_payload_params)
        self.assertEqual(req_kwargs['json']['params'][62], card_status)
        # test response handling
        self.assertEqual(data, resp_json)

    @patch('api_parser.common.api_amr.requests.post')
    def test_exceptions(self, mock_request):

        api_parser = AmrApiRequester()

        mock_request.return_value.raise_for_status.side_effect = HTTPError

        with self.assertRaises(SystemExit):
            api_parser.auth(user='user', password='password', auth_url='auth_url.ru')

        mock_request.side_effect = [ConnectionError, Timeout, RequestException]
        with self.assertRaises(SystemExit):
            api_parser.auth(user='user', password='password', auth_url='auth_url.ru')
        with self.assertRaises(SystemExit):
            api_parser.auth(user='user', password='password', auth_url='auth_url.ru')
        with self.assertRaises(SystemExit):
            api_parser.auth(user='user', password='password', auth_url='auth_url.ru')
