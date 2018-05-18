import logging
from collections import OrderedDict

from coinmarketcap import Market
from dateutil.parser import parse as parse_date

from crypto_analysis.databases import queries


def _get_newcomer_for_uuid(conn, uuid, rank):
    df_last = queries.get_data_for_uuid(conn, uuid, rank)
    df_tail = queries.get_data_below_uuid(conn, uuid, rank)
    newcomers = df_last[df_last["id"].isin(df_tail["id"])]
    return newcomers


def _get_newcomers(conn, rank, no):
    uuids = queries.get_uuids(conn)
    ret_val = OrderedDict()
    for uuid in uuids:
        newcomer = _get_newcomer_for_uuid(conn, uuid, rank)
        if newcomer.empty:
            logging.info("no newcomers found for uuid {}".format(uuid))
            continue
        for index, row in newcomer.iterrows():
            ret_val[row.id] = row.to_dict()
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
    kwargs['newcomers'] = [kwargs['newcomers'][name] for name in
                           sorted(date_coin_mapping, key=date_coin_mapping.get, reverse=True)]
    return kwargs


def get_newcomers(conn, rank, no=10):
    newcomers = _get_newcomers(conn, rank, no)
    newcomers = _enrich_with_latest_data(conn, newcomers)
    return newcomers

