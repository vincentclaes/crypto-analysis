import unittest

from mock import patch

from crypto_analysis.controllers import tweets
from crypto_analysis.controllers.tweets import Twython


class TestTweets(unittest.TestCase):
    @patch.object(Twython, 'update_status')
    def test_run_several_ids(self, m_status):
        m_status.return_value = 'a response'
        tweets.tweet(['bitcoin', 'litecoin'], 100)

    @patch.object(Twython, 'update_status')
    def test_run_no_ids(self, m_status):
        m_status.return_value = 'a response'
        tweets.tweet()


if __name__ == '__main__':
    unittest.main()
