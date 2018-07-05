import ConfigParser
import logging
import os
import sys
from os.path import expanduser

import requests
from bs4 import BeautifulSoup
from coinmarketcap import Market
from twython import Twython


def get_tweet_id(id_):
    """
    we get the class twitter-timeline from the social page of coinmarketcap
    :param id_: coinmarketcap coin id
    :return: twitter id
    """
    r = requests.get("https://coinmarketcap.com/currencies/{}/#social".format(id_))
    soup = BeautifulSoup(r.text, 'lxml')
    twitter_cell = soup.find('a', class_='twitter-timeline')
    if twitter_cell is not None:
        twitter_id = '@' + twitter_cell.text.rsplit('@')[1]
        return twitter_id
    return ''


def get_tokens():
    home = expanduser("~")
    crypto_home = os.path.join(home, '.crypto')
    if not os.path.exists(crypto_home):
        os.mkdir(crypto_home)
    config = ConfigParser.ConfigParser()
    config_path = os.path.join(crypto_home, 'keys.conf')
    config.read(config_path)
    try:
        tokens = config_mapping(config, 'twitter')
    except ConfigParser.NoSectionError:
        print 'make sure you put your twitter tokens in the home directory {}'.format(config_path)
        sys.exit(1)
    return tokens


def config_mapping(config, section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        dict1[option] = config.get(section, option)
    return dict1


def tweet(ids=[], rank=100):
    """
    for each id we get the twitter name and tweet about them.
    :param ids: list of ids
    :param rank: rank 100 / 200 / ???
    :return: None
    """
    logging.info('following coins are eligable for tweets in rank {} : {}'.format(rank, ids))
    coinmarketcap = Market()
    tokens = get_tokens()
    if ids:
        for id_ in ids:
            coin_data = coinmarketcap.ticker(id_)
            name = coin_data[0].get('name')
            tweet_id = get_tweet_id(id_)
            twitter = Twython(**tokens)
            text = '{} is a #cryptonewcomer in the top {} coins for the first time ever. Congratulations {} !' \
                   '\nfollow @DeltaCryptoClu2 to know more newcomers'.format(name, rank, tweet_id)
            logging.info('tweet : {}'.format(text))
            response = twitter.update_status(status=text)
            logging.info(response)
