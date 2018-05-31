import os
import unittest

import pandas as pd
from mock import patch

from crypto_analysis.controllers import newcomers
from crypto_analysis.databases import Connection
from crypto_analysis_tests import TEST_ROOT


class TestNewcomers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = Connection.get_connection('test')

    def setUp(self):
        self.df_last = pd.read_csv(os.path.join(TEST_ROOT, 'test_files', 'test_newcomers_df_last'), index_col=0)
        # create a new coin and add it to the last ones
        self.df_last['id'][0] = "my_coin"
        self.df_tail = pd.read_csv(os.path.join(TEST_ROOT, 'test_files', 'test_newcomers_df_tail'), index_col=0)

    @patch('crypto_analysis.databases.queries.get_unique_ids_below_uuid')
    @patch('crypto_analysis.databases.queries.get_data_for_uuid')
    def test_get_newcomer_for_uuid(self, m_last, m_tail):
        m_last.return_value = self.df_last
        m_tail.return_value = self.df_tail
        newcomer = newcomers._get_newcomer_for_uuid(self.conn, 1526408353, 100)
        self.assertEqual("my_coin", newcomer["id"][0])
        self.assertEqual(1, newcomer.shape[0])

        # create my coin in tail so that it is not a newcomer
        self.df_tail['id'][0] = "my_coin"
        self.newcomer = newcomers._get_newcomer_for_uuid(self.conn, 1526408353, 100)
        self.assertTrue(self.newcomer.empty)

    @patch('crypto_analysis.databases.queries.get_unique_ids_below_uuid')
    @patch('crypto_analysis.databases.queries.get_data_for_uuid')
    @patch('crypto_analysis.controllers.newcomers._enrich_with_latest_data')
    def test_get_newcomers(self, m_last, m_tail, m_enrich):
        m_last.return_value = self.df_last
        m_tail.return_value = self.df_tail
        newcomer = newcomers.get_newcomers(self.conn, 10)
        self.assertEqual("my_coin", newcomer["id"][0])
