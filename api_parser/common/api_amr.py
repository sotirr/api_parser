import requests
from dynaconf import settings
from datetime import datetime, timedelta
from typing import List, Union

from api_parser.common.logger import get_logger


logger = get_logger(__name__)


class AmrApiRequester():
    '''
    interconnect with API
    '''
    def auth(self, auth_url, user: str, password: str, role='') -> None:
        '''
        get key and session_id
        '''
        payload: dict = {'name': user, 'password': password, 'role': role}
        headers: dict = {'Content-Type': 'application/json'}
        logger.debug('Sending authentication request')
        response = self._make_post_request(auth_url, headers=headers, payload=payload)
        resp_json: dict = response.json()[1]
        self.key: str = resp_json['1']
        self.session_id: str = resp_json['2']
        logger.debug('Authentication has been successful')

    def get_data(self, data_url, strt_time: datetime, end_time: datetime, card_status: str) -> List[dict]:
        '''
        return data in json format
        '''
        payload_params: list = self._make_payload_params(strt_time, end_time, card_status)
        payload: dict = {'id': self.session_id, 'key': self.key,
                         'query': 1809, 'params': payload_params}
        headers: dict = {'Content-Type': 'application/json'}
        logger.debug('Sending data request')
        response = self._make_post_request(data_url, headers=headers, payload=payload)
        logger.debug('data has been received')
        return response.json()

    def _make_payload_params(self, strt_time: datetime, end_time: datetime, card_status: str) -> List[Union[str, None]]:
        '''
        return a payload for the data request
        '''
        payload_params: list = [None for _ in range(111)]
        payload_params[6] = f"'{strt_time.strftime('%d.%m.%Y')}'"
        payload_params[7] = f"'{end_time.strftime('%d.%m.%Y')}'"
        payload_params[8] = f"'{strt_time.strftime('%H:%M')}'"
        payload_params[9] = f"'{end_time.strftime('%H:%M')}'"
        if card_status != '0':
            payload_params[62] = card_status
        return payload_params

    def _make_post_request(self, url: str, headers: dict, payload: dict):
        '''
        make request, handle error, return response
        '''
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logger.error(f'An Http Error occurred: {errh}\n message: {response.text}')
            raise SystemExit(f'An Http Error occurred: {errh}')
        except requests.exceptions.ConnectionError as errc:
            logger.error(f'An Error Connecting to the API occurred:: {errc}')
            raise SystemExit(f'An Error Connecting to the API occurred:: {errc}')
        except requests.exceptions.Timeout as errt:
            logger.error(f'A Timeout Error occurred: {errt}')
            raise SystemExit(f'A Timeout Error occurred: {errt}')
        except requests.exceptions.RequestException as err:
            logger.error(err, exc_info=True)
            raise SystemExit(f'An Unknown Error occurred: {err}')
        return response
