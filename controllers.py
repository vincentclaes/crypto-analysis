import logging

from dateutil.parser import parse as parse_date

from databases import queries


def _get_newcomer_for_uuid(conn, uuid, rank):
    df_last = queries.get_data_for_uuid(conn, uuid, rank)
    df_tail = queries.get_data_below_uuid(conn, uuid, rank)
    newcomers = df_last[df_last["id"].isin(df_tail["id"])]
    if newcomers.empty:
        logging.info("no newcomers found for uuid {}".format(uuid))
    return newcomers


def _get_newcomers(conn, rank, no=10):
    uuids = queries.get_uuids(conn)
    counter = 0
    ret_val = {}
    for uuid in uuids:
        newcomer = _get_newcomer_for_uuid(conn, uuid, rank)
        if newcomer.empty:
            continue
        for index, row in newcomer.iterrows():
            ret_val[row.id] = row.to_dict()
            counter += 1  # number of rows = number of newcomers
            if counter > no:
                break
    return ret_val


def get_newcomers(conn, rank):
    ret_val = _get_newcomers(conn, rank)
    kwargs = {'newcomers': ret_val}
    from coinmarketcap import Market
    coinmarketcap = Market()
    date_coin_mapping = {}
    for coin in ret_val.keys():
        current_results = coinmarketcap.ticker(coin)
        kwargs['newcomers'][coin]['current_rank'] = current_results[0]['rank']
        kwargs['newcomers'][coin]['percent_change_24h'] = current_results[0]['percent_change_24h']
        highest_rank = queries.get_highest_rank_for_coin(conn, coin)
        kwargs['newcomers'][coin]['highest_rank'] = highest_rank
        date_coin_mapping[coin] = parse_date(ret_val[coin]["date"])
    kwargs['newcomers'] = [kwargs['newcomers'][name] for name in
                           sorted(date_coin_mapping, key=date_coin_mapping.get, reverse=True)]
    return kwargs
