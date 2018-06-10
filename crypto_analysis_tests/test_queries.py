import os
import unittest

import pandas as pd

from crypto_analysis.controllers import newcomers
from crypto_analysis.databases import Connection
from crypto_analysis.databases import queries
from crypto_analysis_tests import TEST_ROOT


class TestQueries(unittest.TestCase):
    MAX_UUID = 1526408353

    @classmethod
    def setUpClass(cls):
        cls.conn = Connection.get_connection('test')

    def test_verify_valid_newcomers(self):
        uuids = queries.get_uuids(self.conn)
        self.assertEqual(TestQueries.MAX_UUID, uuids[0])

    def test_get_data_for_uuid(self):
        df = queries.get_data_for_uuid(self.conn, TestQueries.MAX_UUID, 100)
        self.assertEqual(TestQueries.MAX_UUID, df["uuid"].loc[0])
        self.assertEqual(df.shape[0], 100)

    def test_get_unique_ids_below_uuid(self):
        df = queries.get_unique_ids_below_uuid(self.conn, TestQueries.MAX_UUID, 100)
        self.assertEqual(df.shape[0], 37)

    def test_check_if_newcomers_table_exists_and_get_max_uuid(self):
        df = pd.read_csv(os.path.join(TEST_ROOT, 'test_files', 'test_newcomers_top100'), index_col=0)
        newcomers.create_newcomers_table(df, 100, self.conn, False)
        table_name = newcomers.build_newcomers_table_name(100)
        max_uuid_newcomers = queries.get_max_uuid_from_newcomers(self.conn, table_name)
        self.assertEqual(max_uuid_newcomers, 1526409999)
        # fixme - queries.drop_table(self.conn, table_name)


if __name__ == '__main__':
    unittest.main()
