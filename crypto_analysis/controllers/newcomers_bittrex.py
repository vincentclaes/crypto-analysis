import json
import logging

import pandas as pd
import requests

from crypto_analysis.controllers import tweets
from crypto_analysis.databases import queries

TABLE_NAME = 'bittrex'


def _get_newcomers(df_latest_data, df_local_data):
    latest = df_latest_data['MarketCurrencyLong'].tolist()
    local = df_local_data['MarketCurrencyLong'].tolist()
    return list(set(latest) - set(local))


def get_newcomers_bittrex(conn):
    df_latest_data = _get_bittrex_data()
    df_local_data = _get_local_data(conn, df_latest_data)
    newcomers = _get_newcomers(df_latest_data, df_local_data)
    if newcomers:
        logging.info('newcomers found ...')
        _tweet_newcomers_bittrex(newcomers)
        queries.create_table(df_latest_data, TABLE_NAME, conn, if_exists='replace', index=False)
        return
    logging.info('no newcomers found ...')


def _tweet_newcomers_bittrex(newcomers):
    for newcomer in newcomers:
        msg = 'bittrex just listed a new coin: {} \n it usually moons ...'.format(newcomer)
        logging.info('sending tweet: ' + msg)
        tweets.post_tweet(msg)


def _get_local_data(conn, df_latest_data):
    if not queries.table_exists(conn, TABLE_NAME):
        queries.create_table(df_latest_data, TABLE_NAME, conn, if_exists='replace', index=False)
    return queries.get_table(conn, TABLE_NAME)


def _get_bittrex_data():
    url = "https://bittrex.com/api/v1.1/public/getmarkets"
    data = requests.request("GET", url)
    df_latest = pd.DataFrame(json.loads(data.content).get('result'))
    return df_latest
