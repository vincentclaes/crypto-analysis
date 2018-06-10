import json
import os
import unittest

import pandas as pd
from mock import patch

from crypto_analysis.controllers import newcomers
from crypto_analysis.controllers.newcomers import Market
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
        self.newcomers = json.load(
            open(os.path.join(TEST_ROOT, 'test_files', 'test_newcomers_enrich_latest_data.json')))
        self.coinmarket_data_current_results = json.load(
            open(os.path.join(TEST_ROOT, 'test_files', 'coinmarket_data_current_results.json')))

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

    @patch('crypto_analysis.databases.queries.get_highest_rank_for_coin')
    @patch('crypto_analysis.databases.queries.get_unique_ids_below_uuid')
    @patch('crypto_analysis.databases.queries.get_data_for_uuid')
    @patch.object(Market, 'ticker')
    def test_get_newcomers(self, m_enrich, m_last, m_tail, m_highest):
        m_enrich.return_value = self.coinmarket_data_current_results
        m_last.return_value = self.df_last
        m_tail.return_value = self.df_tail
        m_highest.return_value = 100
        newcomer = newcomers.get_newcomers(self.conn, 10, latest_only=False)
        self.assertEqual("my_coin", newcomer["newcomers"][0]["id"])

    @patch('crypto_analysis.databases.queries.get_max_uuid_from_newcomers')
    @patch('crypto_analysis.databases.queries.get_unique_uuids_above_latest_newcomer_uuid')
    @patch('crypto_analysis.databases.queries.get_data_for_uuid')
    @patch('crypto_analysis.databases.queries.get_unique_ids_below_uuid')
    def test_get_newcomers_latest_only(self, m_tail, m_last, m_uuids_above, m_max_uuid):
        # the latest uuid in the newcomers table is 1526409999
        # when looking for newcomers we only get the latest data
        # for uuids > 1526409999
        self.df_last['uuid'][0] = 1526401000
        self.df_last['uuid'][1] = 1526401000
        self.df_last['uuid'][2] = 1526401000
        m_last.return_value = self.df_last[:3]
        m_tail.return_value = self.df_tail
        m_max_uuid.return_value = 1526409999
        m_uuids_above.return_value = [1526401000]
        newcomer = newcomers._get_newcomers(self.conn, 100, 10, latest_only=True)
        self.assertEqual("my_coin", newcomer['my_coin']['id'])

    @patch('crypto_analysis.databases.queries.get_highest_rank_for_coin')
    def test_enrich_with_latest_data(self, m_highest_rank):
        newcomers_enriched = newcomers._enrich_with_latest_data(self.conn, self.newcomers)
        df = pd.DataFrame(newcomers_enriched.get('newcomers'))
        self.assertTrue(all(df["name"].tolist()))
