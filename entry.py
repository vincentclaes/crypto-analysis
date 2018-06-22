import argparse
import logging

from crypto_analysis.controllers import newcomers
# from crypto_analysis.controllers import tweets
from crypto_analysis.databases import Connection
from crypto_analysis.databases import DB


def get_newcomers(args):
    newcomers.get_newcomers(conn, args.rank, args.no, args.latest)


def update_newcomers(args):
    newcomers.update_newcomers(conn, args.rank)


def tweet(args):
    # tweets.tweet(args.ids, args.rank)
    pass


if __name__ == '__main__':
    conn = Connection.get_connection(DB)
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='extra functions for newcomers, notifications etc.')

    get_newcomers_parser = subparsers.add_parser("newcomers")
    get_newcomers_parser.add_argument("-r", "--rank", help="rank you want to use", type=int, required=True)
    get_newcomers_parser.add_argument("-n", "--no", help="number of results you want", type=int, required=True)
    get_newcomers_parser.add_argument("--latest", help="do i only want to get the latest newcomers",
                                      action="store_true")
    get_newcomers_parser.set_defaults(func=get_newcomers)

    update_newcomers_parser = subparsers.add_parser("newcomers_update")
    update_newcomers_parser.add_argument("-r", "--rank", help="rank you want to use", type=int, required=True)
    update_newcomers_parser.set_defaults(func=update_newcomers)

    get_newcomers_parser = subparsers.add_parser("tweet")
    get_newcomers_parser.add_argument("-r", "--rank", help="rank you want to use", type=int, required=True)
    get_newcomers_parser.add_argument("-i", "--ids", help="ids you want to tweet", nargs='*')
    get_newcomers_parser.set_defaults(func=tweet)

    args = parser.parse_args()
    args.func(args)
