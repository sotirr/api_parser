from clickhouse_driver import Client
import clickhouse_driver
from typing import List, Dict

from api_parser.common.logger import get_logger

logger = get_logger(__name__)


def write_to_db(
                data: List[Dict[str, str]], table_name: str, **kwargs,
               ) -> str:
    '''
    Function connects to the db and writes the data to it.
    '''
    # Connect to DB
    client: clickhouse_driver.client.Client
    client = Client(**kwargs)
    # Write data to DB
    settings_dict: dict = {'strings_as_bytes': False}
    logger.debug(f'Writing Data to {table_name} table')
    try:
        result = client.execute(f'INSERT INTO {table_name} VALUES',
                                data, types_check=False,
                                settings=settings_dict)
    except clickhouse_driver.errors.TypeMismatchError as err:
        logger.error(f'db interact errors: {err}')
        raise SystemExit(err)
    logger.debug(f'have been added {result} row(s) to the {table_name} table')
    return result
