import logging
import sys

import pandas as pd
from sqlalchemy import create_engine

from controllers import get_newcomers
from databases import Connection
from databases import DB
from databases import db_path

"""
get newcomers and dump in a table. we expect the rank as 1st argument.
"""
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _construct_db_path(db_path):
    return 'sqlite:///{}'.format(db_path)


def create_table(df, table_name, engine):
    df.to_sql(table_name, engine, if_exists='replace')


def main(args):
    rank = args[0]
    no = args[1]
    logging.info('getting newcomers in rank {}'.format(rank))
    conn = Connection.get_connection(DB)
    newcomers = get_newcomers(conn, int(rank), int(no))
    df_newcomers = pd.DataFrame(newcomers.get('newcomers'))
    logging.info('{} newcomers found'.format(df_newcomers.shape[0]))
    logging.info('{}'.format(df_newcomers.to_string()))
    _db_path = _construct_db_path(db_path)
    disk_engine = create_engine(_db_path)
    table_name = 'newcomers_top{}'.format(str(rank))
    logging.info('dumping data in table {}'.format(table_name))
    create_table(df_newcomers, table_name, disk_engine)
    logging.info('dump ok.')
    logging.info('done.')


if __name__ == '__main__':
    main(sys.argv[1:])
