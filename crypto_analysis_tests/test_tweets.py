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

    def test_get_tweet(self):
        list_ = ['name', 'tweet_id']
        _exception = None
        try:
            tweets.get_tweet(50, **dict(zip(list_, list_)))
            tweets.get_tweet(100, **dict(zip(list_, list_)))
            tweets.get_tweet(200, **dict(zip(list_, list_)))
        except Exception as e:
            _exception = e
        finally:
            self.assertIsNone(_exception)


if __name__ == '__main__':
    unittest.main()
