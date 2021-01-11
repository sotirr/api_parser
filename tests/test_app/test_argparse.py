import unittest
from unittest.mock import patch
from io import StringIO
from datetime import datetime

from api_parser.run import parse_args


class TestArgParse(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('sys.stderr', new_callable=StringIO)
    def test_parsing_wrong_format_args(self, mock_stderr):
        input_args = ['-s', '2018-01-01T00:00:00+00:00', '-e', '123']
        with self.assertRaises(SystemExit):
            parse_args(input_args)
        self.assertIn('invalid fromisoformat value:', mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_parsing_empty_args(self, mock_stderr):
        input_args = []
        with self.assertRaises(SystemExit):
            parse_args(input_args)
        self.assertIn('the following arguments are required:', mock_stderr.getvalue())

    def test_parsing_date_args(self):
        input_args = ['-s', '2020-11-11T00:00:00+00:00', '-e', '2020-11-14T00:00:00+00:00']
        args = parse_args(input_args)
        self.assertIn('strt_time', args, msg='optional argument strt_time must be exist')
        self.assertIn('end_time', args, msg='optional argument end_time must be exist')
        self.assertIsInstance(args.strt_time, datetime)
        self.assertIsInstance(args.end_time, datetime)

    @patch('sys.stderr', new_callable=StringIO)
    def test_parsing_card_status_arg_wrong_choice(self, mock_stderr):
        input_args = ['-s', '2020-11-11T00:00:00+00:00', '-e', '2020-11-14T00:00:00+00:00', '-c', '4']
        with self.assertRaises(SystemExit):
            parse_args(input_args)
        self.assertIn('invalid choice:', mock_stderr.getvalue())

    def test_parsing_card_status_arg_empty(self):
        input_args = ['-s', '2020-11-11T00:00:00+00:00', '-e', '2020-11-14T00:00:00+00:00']
        args = parse_args(input_args)
        self.assertEqual('0', args.card_status)

    def test_parsing_card_status_arg_right_value(self):
        input_args = ['-s', '2020-11-11T00:00:00+00:00', '-e', '2020-11-14T00:00:00+00:00', '-c', '2']
        args = parse_args(input_args)
        self.assertEqual('2', args.card_status)
