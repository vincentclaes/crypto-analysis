import unittest

import pandas as pd
from mock import patch

from crypto_analysis.controllers import newcomers_bittrex
from crypto_analysis.databases import Connection


class TestBittrex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = Connection.get_connection('test')

    @patch('crypto_analysis.controllers.newcomers_bittrex._get_bittrex_data')
    def test_run_several_ids(self, m_df_latest):
        df_latest = pd.read_csv(r'test_files/test_bittrex_df_latest.csv')
        m_df_latest.return_value = df_latest
        newcomers_bittrex.get_newcomers_bittrex(self.conn)

    @patch('crypto_analysis.controllers.tweets.post_tweet')
    @patch('crypto_analysis.controllers.newcomers_bittrex._get_local_data')
    @patch('crypto_analysis.controllers.newcomers_bittrex._get_bittrex_data')
    def test_run_several_ids(self, m_df_latest, m_df_local, m_tweet):
        df_latest = pd.read_csv(r'test_files/test_bittrex_df_latest.csv')
        df_local = df_latest.copy()
        m_df_latest.return_value = df_latest
        m_df_local.return_value = df_local[df_local['MarketCurrency'] != 'BTC']
        newcomers_bittrex.get_newcomers_bittrex(self.conn)
        self.assertTrue(m_tweet.call_count, 1)


if __name__ == '__main__':
    unittest.main()
