"""
get newcomers and dump in a table. we expect the rank as 1st argument.
"""
import logging
from collections import OrderedDict

import pandas as pd
from coinmarketcap import Market
from dateutil.parser import parse as parse_date

from crypto_analysis.databases import queries


def _get_newcomer_for_uuid(conn, uuid, rank):
    logging.info('getting newcomers for uuid {}'.format(uuid))
    df_last = queries.get_data_for_uuid(conn, uuid, rank)
    df_tail = queries.get_unique_ids_below_uuid(conn, uuid, rank)
    newcomers = df_last[~df_last["id"].isin(df_tail["id"])]
    return newcomers


def _get_uuids(conn, rank, latest_only):
    if latest_only:
        table_name = build_newcomers_table_name(rank)
        latest_uuid = queries.get_max_uuid_from_newcomers(conn, table_name)
        return queries.get_unique_uuids_above_latest_newcomer_uuid(conn, latest_uuid, rank)
    return queries.get_uuids(conn)


def _get_newcomers(conn, rank, no, latest_only):
    uuids = _get_uuids(conn, rank, latest_only)
    ret_val = OrderedDict()
    for uuid in uuids:
        newcomer = _get_newcomer_for_uuid(conn, uuid, rank)
        if newcomer.empty:
            logging.info("no newcomers found for uuid {}".format(uuid))
            continue
        for index, row in newcomer.iterrows():
            ret_val[row.id] = row.to_dict()
            logging.info('newcomers found : {}'.format(ret_val))
            if len(ret_val) >= no:
                return ret_val
    return ret_val


def _enrich_with_latest_data(conn, newcomers):
    kwargs = {'newcomers': newcomers}
    coinmarketcap = Market()
    date_coin_mapping = {}
    for coin in newcomers.keys():
        current_results = coinmarketcap.ticker(coin)
        kwargs['newcomers'][coin]['current_rank'] = current_results[0]['rank']
        kwargs['newcomers'][coin]['percent_change_24h'] = current_results[0]['percent_change_24h']
        highest_rank = queries.get_highest_rank_for_coin(conn, coin)
        kwargs['newcomers'][coin]['highest_rank'] = highest_rank
        date_coin_mapping[coin] = parse_date(newcomers[coin]["date"])
        # cleaning - fixme move this to seperate function
        newcomer_name = kwargs['newcomers'][coin].get('name')
        kwargs['newcomers'][coin]['name'] = kwargs['newcomers'][coin].get(
            'id').capitalize() if newcomer_name is None else newcomer_name
        kwargs['newcomers'][coin]['date'] = kwargs['newcomers'][coin]['date'][:10]
    kwargs['newcomers'] = [kwargs['newcomers'][name] for name in
                           sorted(date_coin_mapping, key=date_coin_mapping.get, reverse=True)]
    return kwargs


def _construct_db_path(db_path):
    return 'sqlite:///{}'.format(db_path)


def create_table(df, table_name, conn, if_exists):
    logging.info('dumping data in table {}'.format(table_name))
    df.to_sql(table_name, conn, if_exists=if_exists)
    logging.info('dump ok.')


def build_newcomers_table_name(rank):
    table_name = 'newcomers_top{}'.format(str(rank))
    logging.info('table name {}'.format(table_name))
    return table_name


def create_newcomers_table(df, rank, conn, latest_only):
    table_name = build_newcomers_table_name(rank)
    if_exists = 'replace'
    if latest_only:
        if_exists = 'append'
    create_table(df, table_name, conn, if_exists)


def get_newcomers(conn, rank, no=10, latest_only=True):
    logging.info('getting {} newcomers in rank {}'.format(no, rank))
    newcomers = _get_newcomers(conn, rank, no, latest_only)
    newcomers = _enrich_with_latest_data(conn, newcomers)
    df_newcomers = pd.DataFrame(newcomers.get('newcomers'))
    logging.info('{} newcomers found'.format(df_newcomers.shape[0]))
    logging.info('{}'.format(df_newcomers.to_string()))
    create_newcomers_table(df_newcomers, rank, conn, latest_only='replace')
    logging.info('done.')
    return newcomers
