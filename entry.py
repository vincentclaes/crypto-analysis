import argparse
import logging

from crypto_analysis.controllers import newcomers
from crypto_analysis.databases import Connection
from crypto_analysis.databases import DB

if __name__ == '__main__':
    conn = Connection.get_connection(DB)
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rank", help="rank you want to use", type=int, required=True)
    parser.add_argument("-n", "--no", help="number of results you want", type=int, required=True)
    parser.add_argument("--latest", help="do i only want to get the latest newcomers", action="store_true")
    args = parser.parse_args()
    newcomers.get_newcomers(conn, args.rank, args.no, args.latest)
