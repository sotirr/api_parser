import json
from typing import Dict, List, Any
from dynaconf import settings
from importlib import resources
from datetime import datetime
import hashlib
from functools import wraps
from abc import ABC


def none_value(method):
    @wraps(method)
    def wrapper(*args, if_none: str = 'raise_error', **kwargs):
        if all(args) and all(kwargs.values()):
            return method(*args, **kwargs)
        else:
            if if_none == 'raise_error':
                raise ValueError('Value cannot be None')
            return if_none
    return wrapper


class Row(ABC):
    '''
    base row
    '''
    def __init__(self,  json_dict: dict) -> None:
        self.hub_smp_hk: bytes = self._to_hash(json_dict['ID_KT'],
                                               if_none='raise_error')
        self.record_source: int = 5
        self.load_date: datetime.date = datetime.now().date()
        self.load_datetime: datetime = datetime.now()

    @none_value
    def _to_hash(self, value: str) -> bytes:
        '''
        make md5 hash from str
        '''
        return hashlib.md5(value.encode('UTF-8')).digest()

    @none_value
    def _to_int(self, value: str) -> int:
        '''
        convert str to int
        '''
        return int(value)

    @none_value
    def _to_float(self, value: str) -> float:
        '''
        convert str to float
        '''
        return float(value)

    @none_value
    def _to_datatime(self, value: str) -> datetime:
        '''
        convert str to datetime
        '''
        return datetime.strptime(value, "%d.%m.%Y %H:%M:%S")

    @none_value
    def _to_str(self, value: str) -> str:
        '''
        convert value to str
        '''
        return str(value)

    @none_value
    def _to_seconds(self, time_str: str) -> int:
        '''
        convert str with time to seconds
        '''
        time = datetime.strptime(time_str.strip(), "%H:%M:%S").time()
        seconds = time.hour * 60 * 60 + time.minute * 60 + time.second
        return seconds

    @none_value
    def _from_hdbk(self, key: str, hdbk_name: str) -> str:
        '''
        Decode values by handbooks
        '''
        handbook: str = self.__load_hdbk(hdbk_name)
        return handbook[key]

    def __load_hdbk(self, handbook_name):
        '''
        load handbook from json
        '''
        with resources.open_text('api_parser.resources', handbook_name) as json_hdbk:
            handbook: Dict[str, str] = json.load(json_hdbk)
        return handbook


class HbSmpRow(Row):
    '''
    one row for the hb_smp table
    '''
    def __init__(self, json_dict: dict) -> None:
        super().__init__(json_dict)
        self.id_kt: int = self._to_int(json_dict['ID_KT'], if_none='raise_error')
        self.applied_datetime: datetime = self._make_applied_datetime(json_dict['DATERECEIVED'],
                                                                      json_dict['TIMERECEIVED'],
                                                                      if_none='raise_error')

    @none_value
    def _make_applied_datetime(self, date_str: str, time_str: str) -> datetime:
        '''
        convert str to datetime for the applied_datetime column
        '''
        datetime_str: str = f'{date_str} {time_str}'
        return self._to_datatime(datetime_str)


class StlSmpRow(Row):
    '''
    one row for the stl_smp table
    '''
    def __init__(self, json_dict: dict) -> None:
        super().__init__(json_dict)
        self.name_kind: str = self._from_hdbk(json_dict['ID_KIND'],
                                              hdbk_name=settings['kind_hdbk'],
                                              if_none='')
        self.res_call_status: str = self._from_hdbk(json_dict['RES_CALL_STATUS'],
                                                    hdbk_name=settings['call_status_hdbk'],
                                                    if_none='')
        self.number_one: str = self._to_str(json_dict['NUMBER_ONE'], if_none='')
        self.number_day: str = self._to_str(json_dict['NUMBER_DAY'], if_none='')
        self.name_attribute: str = self._from_hdbk(json_dict['ID_ATTRIBUTE'],
                                                   hdbk_name=settings['id_attribute_hdbk'],
                                                   if_none='')
        self.lastname: str = self._to_str(json_dict['PAT_SURNAME_OUT'], if_none='')
        self.firstname: str = self._to_str(json_dict['PAT_NAME_OUT'], if_none='')
        self.surname: str = self._to_str(json_dict['PAT_PATRONYMIC_OUT'], if_none='')
        self.patient_birthday: int = self._make_patient_birthday(json_dict['PATIENT_BIRTHDAY'],
                                                                 if_none=11111111)
        self.age_str: int = self._make_age_str(json_dict['AGE_STR'], if_none=-1)
        self.gender: str = self._to_str(json_dict['GENDER_'], if_none='Не определено')
        self.address: str = self._to_str(json_dict['ADDRESS'], if_none='')
        self.mkb_code: str = self._make_mkb_code(json_dict['MKB_CODE_'], if_none='')
        self.mkb_name: str = self._make_mkb_name(json_dict['MKB_CODE_'], if_none='')
        self.diagnos_res: str = self._to_str(json_dict['DIAGNOS_RES'], if_none='')
        self.date_time_received: datetime = self._make_date_time_received(json_dict['DATERECEIVED'],
                                                                          json_dict['TIMERECEIVED'],
                                                                          if_none='raise_error')
        self.date_time_call_transfer: datetime = self._to_datatime(json_dict['DATE_TIME_CALL_TRANSFER'],
                                                                   if_none=datetime(2015, 12, 31))
        self.date_time_take_call: datetime = self._to_datatime(json_dict['DATE_TIME_TAKE_CALL'],
                                                               if_none=datetime(2015, 12, 31))
        self.date_time_process_finish: datetime = self._to_datatime(json_dict['DATE_TIME_PROCESS_FINISH'],
                                                                    if_none=datetime(2015, 12, 31))
        self.time_took: int = self._to_seconds(json_dict['TIME_TOOK'], if_none=-1)
        self.time_come_lpu: int = self._to_seconds(json_dict['TIME_COME_LPU'], if_none=-1)
        self.time_card_open: int = self._to_seconds(json_dict['TIME_CARD_OPEN'], if_none=-1)
        self.time_hosp: int = self._to_seconds(json_dict['TIME_HOSP'], if_none=-1)
        self.time_coming_to_patient: int = self._to_seconds(json_dict['TIMECOMING'], if_none=-1)
        self.brigada_name: str = self._to_str(json_dict['BRIGADA_NAME'], if_none='')
        self.call_result: str = self._to_str(json_dict['CALL_RESULT'], if_none='')
        self.lat: float = self._to_float(json_dict['LAT'], if_none=-1.0)
        self.lon: float = self._to_float(json_dict['LON'], if_none=-1.0)
        self.snils: str = self._to_str(json_dict['SNILS'], if_none='')
        self.is_city: int = self._to_int(json_dict['IS_CITY'], if_none=-1)
        self.id_mo_smp: int = self._to_int(json_dict['ID_MO_HOSP'], if_none=-1)
        self.oms_care_form: str = self._from_hdbk(json_dict['ID_OMS_CARE_FORM'],
                                                  hdbk_name=settings['oms_care_hdbk'],
                                                  if_none='Помощь не оказывалась')

        self.applied_datetime: datetime = self._make_applied_time(json_dict['DATE_UPDATE_OUT'],
                                                                  if_none='raise_error')

        column_for_hashing = [self.name_kind, self.res_call_status, self.number_one,
                              self.number_day, self.name_attribute, self.lastname,
                              self.firstname, self.surname, self.patient_birthday,
                              self.age_str, self.gender, self.address, self.mkb_code,
                              self.mkb_name, self.diagnos_res, self.date_time_received,
                              self.date_time_call_transfer, self.date_time_take_call,
                              self.date_time_process_finish, self.time_took, self.time_come_lpu,
                              self.time_card_open, self.time_hosp, self.time_coming_to_patient,
                              self.brigada_name, self.call_result, self.lat, self.lon, self.snils,
                              self.is_city, self.id_mo_smp]
        self.diff_op_doc_reg_hk: bytes = self._make_diff_op_doc_reg_hk(column_for_hashing)
        self.load_end_datetime: datetime = datetime(2105, 12, 31)

    @none_value
    def _make_patient_birthday(self, value: str) -> int:
        '''
        convert str to datetime and finally to int in the next format:
        int('YYYYMMDD')
        '''
        birthday: datetime.date = datetime.strptime('24.03.1976', "%d.%m.%Y").date()
        return int(birthday.strftime("%Y%m%d"))

    @none_value
    def _make_age_str(self, value: str) -> int:
        '''
        cuts patient age from str
        '''
        for number in value.split():
            if number.isdigit():
                return int(number)
                break
        return -1

    @none_value
    def _make_mkb_code(self, value: str) -> str:
        '''
        cut mkb_code from str
        '''
        return value.split()[0].strip('[]')

    @none_value
    def _make_mkb_name(self, value: str) -> str:
        '''
        cut mkb_name from str
        '''
        return value.split(maxsplit=1)[1]

    @none_value
    def _make_date_time_received(self, date_str: str, time_str: str) -> datetime:
        '''
        convert str to datetime for the date_time_received column
        '''
        datetime_str: str = f'{date_str} {time_str}'
        return self._to_datatime(datetime_str)

    def _make_diff_op_doc_reg_hk(self, *args) -> bytes:
        '''
        hash almost all data in the row
        '''
        value = ';'.join([str(item) for item in args])
        return hashlib.md5(value.encode('UTF-8')).digest()

    @none_value
    def _make_applied_time(self, value: str) -> datetime:
        '''
        convert str with format "%Y-%m-%d %H:%M:%S.%f" to datetime
        '''
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")


class Table(ABC):
    '''
    base table
    '''
    def row_as_dict(self, row: Row) -> dict:
        '''
        convert one row to dict format
        '''
        return vars(row)

    def as_list(self) -> List[dict]:
        '''
        convert all table to list of dicts format
        '''
        return [self.row_as_dict(row) for row in self.rows]

    def normalize_data(self, data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        '''
        normalize data that was received from API
        '''
        normalize_rows: List[Dict[str, str]] = []
        column_codes: Dict[str, str] = data[0]

        for row in data[1:]:
            normalize_row: Dict[str, str] = self._normalized_row(row, column_codes)
            normalize_rows.append(normalize_row)

        return normalize_rows

    def _normalized_row(self, row: Dict[str, str], column_codes: Dict[str, str]):
        '''
        normalize one row
        '''
        normalize_row: Dict[str, str] = {}
        for id in row:
            column_name: str = column_codes[id]
            value: str = row[id]
            normalize_row[column_name]: Any = value
        return normalize_row


class HbSmpTable(Table):
    '''
    hb_smp Table
    '''
    def __init__(self, json_with_data: List[dict]) -> None:
        data = self.normalize_data(json_with_data)
        self.rows = [HbSmpRow(row) for row in data]


class StlSmpTable(Table):
    '''
    stl_smp Table
    '''
    def __init__(self, json_with_data: List[dict]) -> None:
        data = self.normalize_data(json_with_data)
        self.rows = [StlSmpRow(row) for row in data]
