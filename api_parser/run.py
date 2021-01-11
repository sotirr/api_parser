from dynaconf import settings
from typing import Dict, Union
from datetime import datetime
import argparse

from api_parser.common.json_parser import HbSmpTable, StlSmpTable
from api_parser.common.db_interaction import write_to_db
from api_parser.common.logger import get_logger
from api_parser.common.api_amr import AmrApiRequester

logger = get_logger(__name__)


def main():
    # interconects with api
    args: argparse.Namespace = parse_args()
    amr_api = AmrApiRequester()
    amr_api.auth(settings['auth_url'],
                 user=settings['api_user'],
                 password=settings['api_password'])
    data: list = amr_api.get_data(settings['data_url'],
                                  args.strt_time, args.end_time,
                                  args.card_status)

    # create tables objects
    hb_smp_table = HbSmpTable(data)
    stl_smp_table = StlSmpTable(data)

    # Write to DB
    db_settings: Dict[str, Union[str, int]]
    db_settings = {
                   'host': settings['host'], 'port': settings['port'],
                   'database': settings['database'],
                   'user': settings['user'],
                   'password': settings['password'],
                  }
    write_hb_smp_table: str = write_to_db(hb_smp_table.as_list(),
                                          table_name=settings['hb_smp_table'],
                                          **db_settings)

    write_stl_smp_table: str = write_to_db(stl_smp_table.as_list(),
                                           table_name=settings['stl_smp_table'],
                                           **db_settings)


class argparse_logger(argparse.ArgumentParser):
    def error(self, message):
        '''
        add logging to argparse
        '''
        logger.error(f'Initial error ocurred : {message}')
        super().error(message)


def parse_args(*args, **kwargs) -> argparse.Namespace:
    '''
    Implement comand line arg parser
    '''
    parser = argparse_logger(description='Parses api for a certain range of time and writes the result in database',
                             prog=settings['name'])
    parser.add_argument('-v', '--version', action='version', version=settings['version'])
    parser.add_argument('-s', '--strt_time', type=datetime.fromisoformat,
                        help='sampling start time in iso format', required=True, metavar='')
    parser.add_argument('-e', '--end_time',  type=datetime.fromisoformat,
                        help='sampling end time in iso format', required=True, metavar='')
    parser.add_argument('-c', '--card_status', default='0', choices=['0', '1', '2'], required=False, metavar='',
                        help='''
                        filtering by ID_CALL_RESULT_STATUS field.
                        Choices: 0 - all cards 1 - draft, 2 - filled card.
                        Default 0.
                        ''')
    return parser.parse_args(*args, **kwargs)


if __name__ == "__main__":
    main()
