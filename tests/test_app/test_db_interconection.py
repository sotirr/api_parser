import unittest
from clickhouse_driver import Client

from api_parser.common.db_interaction import write_to_db

from tests.resources.normalize_data_for_hb_smp_table import hb_smp_data
from tests.resources.normalize_data_for_stl_smp_table import stl_smp_data




class UserModelCase(unittest.TestCase):
    def setUp(self):
        create_hb_smp_table = '''
            create table hb_smp
            (
                hub_smp_hk       FixedString(16),
                id_kt            Int32,
                record_source    UInt8,
                load_date        Date,
                load_datetime    DateTime,
                applied_datetime DateTime
            )
                engine = Memory;
            '''
        create_stl_smp_table = '''
            create table stl_smp
            (
                hub_smp_hk               FixedString(16),
                name_kind                String,
                res_call_status          String,
                number_one               String,
                number_day               String,
                name_attribute           String,
                lastname                 String,
                firstname                String,
                surname                  String,
                patient_birthday         Int32,
                age_str                  Int16,
                gender                   String,
                address                  String,
                mkb_code                 String,
                mkb_name                 String,
                diagnos_res              String,
                date_time_received       DateTime,
                date_time_call_transfer  DateTime,
                date_time_take_call      DateTime,
                date_time_process_finish DateTime,
                time_took                Int32,
                time_come_lpu            Int32,
                time_card_open           Int32,
                time_hosp                Int32,
                brigada_name             String,
                call_result              String,
                lat                      Float64,
                lon                      Float64,
                snils                    String,
                is_city                  Int8,
                id_mo_smp                Int32,
                oms_care_form            String,
                record_source            UInt8,
                load_date                Date,
                load_datetime            DateTime,
                applied_datetime         DateTime,
                diff_op_doc_reg_hk       FixedString(16),
                load_end_datetime        DateTime
            )
                engine = Memory;
            '''
        db_settings = {'host': 'localhost'}
        self.client = Client(**db_settings)
        self.client.execute(create_hb_smp_table)
        self.client.execute(create_stl_smp_table)

    def tearDown(self):
        self.client.execute('DROP TABLE IF EXISTS hb_smp')
        self.client.execute('DROP TABLE IF EXISTS stl_smp')
        self.client.disconnect()

    def test_writing_to_db(self):
        hb_smp_table = write_to_db(hb_smp_data, table_name='hb_smp', host='localhost')
        stl_smp_table = write_to_db(stl_smp_data, table_name='stl_smp', host='localhost')
        self.assertEqual(hb_smp_table, 3)
        self.assertEqual(stl_smp_table, 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
