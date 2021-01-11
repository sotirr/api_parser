import unittest
from importlib import resources
from datetime import datetime, date
import json

from api_parser.common.json_parser import HbSmpTable, StlSmpTable


class TestJsonParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with resources.open_text('tests.resources', 'resp_example.json') as data_json:
            resp_json = json.load(data_json)
        cls.hb_smp_table = HbSmpTable(resp_json)
        cls.stl_smp_table = StlSmpTable(resp_json)

    def test_values_not_null(self):
        for row in self.hb_smp_table.as_list():
            for value in row.values():
                self.assertTrue(value is not None)

        for row in self.stl_smp_table.as_list():
            for value in row.values():
                self.assertTrue(value is not None)

    def test_casing_stl_smp_table(self):
        for row in self.stl_smp_table.as_list():
            self.assertIsInstance(row['hub_smp_hk'], bytes)
            self.assertIsInstance(row['record_source'], int)
            self.assertIsInstance(row['load_date'], date)
            self.assertIsInstance(row['load_datetime'], datetime)
            self.assertIsInstance(row['name_kind'], str)
            self.assertIsInstance(row['res_call_status'], str)
            self.assertIsInstance(row['number_one'], str)
            self.assertIsInstance(row['number_day'], str)
            self.assertIsInstance(row['name_attribute'], str)
            self.assertIsInstance(row['lastname'], str)
            self.assertIsInstance(row['firstname'], str)
            self.assertIsInstance(row['surname'], str)
            self.assertIsInstance(row['patient_birthday'], int)
            self.assertIsInstance(row['age_str'], int)
            self.assertIsInstance(row['gender'], str)
            self.assertIsInstance(row['address'], str)
            self.assertIsInstance(row['mkb_code'], str)
            self.assertIsInstance(row['mkb_name'], str)
            self.assertIsInstance(row['diagnos_res'], str)
            self.assertIsInstance(row['date_time_received'], datetime)
            self.assertIsInstance(row['date_time_call_transfer'], datetime)
            self.assertIsInstance(row['date_time_take_call'], datetime)
            self.assertIsInstance(row['date_time_process_finish'], datetime)
            self.assertIsInstance(row['time_took'], int)
            self.assertIsInstance(row['time_come_lpu'], int)
            self.assertIsInstance(row['time_card_open'], int)
            self.assertIsInstance(row['time_hosp'], int)
            self.assertIsInstance(row['time_coming_to_patient'], int)
            self.assertIsInstance(row['brigada_name'], str)
            self.assertIsInstance(row['call_result'], str)
            self.assertIsInstance(row['lat'], float)
            self.assertIsInstance(row['lon'], float)
            self.assertIsInstance(row['snils'], str)
            self.assertIsInstance(row['is_city'], int)
            self.assertIsInstance(row['id_mo_smp'], int)
            self.assertIsInstance(row['oms_care_form'], str)
            self.assertIsInstance(row['applied_datetime'], datetime)
            self.assertIsInstance(row['diff_op_doc_reg_hk'], bytes)
            self.assertIsInstance(row['load_end_datetime'], datetime)

    def test_casing_hb_smp_table(self):
        for row in self.hb_smp_table.as_list():
            self.assertIsInstance(row['hub_smp_hk'], bytes)
            self.assertIsInstance(row['record_source'], int)
            self.assertIsInstance(row['load_date'], date)
            self.assertIsInstance(row['load_datetime'], datetime)
            self.assertIsInstance(row['id_kt'], int)
            self.assertIsInstance(row['applied_datetime'], datetime)
