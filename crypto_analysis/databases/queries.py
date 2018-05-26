import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def get_uuids(conn):
    cur = conn.cursor()
    results = cur.execute("select uuid from crypto_data group by date order by uuid desc").fetchall()
    uuids = [element[0] for element in results]
    return uuids


def get_max_uuid(conn):
    cur = conn.cursor()
    cur.execute("SELECT MAX(uuid) FROM crypto_data")
    return cur.fetchall()[0][0]


def get_data_for_uuid(conn, uuid, rank=100):
    cur = conn.cursor()
    cur.execute("SELECT * FROM crypto_data where uuid=={}".format(uuid))
    df = pd.DataFrame(cur.fetchall())
    df.columns = [e[0] for e in cur.description]
    df = df[df['rank'].astype(int) <= rank]
    return df

def get_unique_ids_for_uuid(conn, uuid, rank=100):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT id FROM crypto_data where uuid=={}".format(uuid))
    df = pd.DataFrame(cur.fetchall())
    df.columns = [e[0] for e in cur.description]
    return df

def get_data_below_uuid(conn, uuid, rank=100):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM crypto_data where uuid<={} and rank <= {}".format(uuid, rank))
    df = pd.DataFrame(cur.fetchall())

    df.columns = [e[0] for e in cur.description]
    df = df[df['rank'].astype(int) <= rank]
    return df

def get_unique_ids_below_uuid(conn, uuid, rank=100):
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT id FROM crypto_data where uuid<={} and rank <= {}".format(uuid, rank))
    df = pd.DataFrame(cur.fetchall())
    df.columns = [e[0] for e in cur.description]
    return df

def get_highest_rank_for_coin(conn, coin):
    cur = conn.cursor()
    cur.execute("SELECT rank FROM crypto_data where id='{}'".format(coin))
    df = pd.DataFrame(cur.fetchall())
    return df[0].astype(int).min()


def get_marketcap_per_day(conn, rank=200):
    cur = conn.cursor()
    ret_val = {}
    results = cur.execute(
        "select date,uuid,id,market_cap_usd from crypto_data where rank <= {} group by date,id order by date asc".format(
            rank)).fetchall()
    df = pd.DataFrame(results, columns=['date', 'uuid', 'id', 'market_cap_usd'])
    for index, sub_df in df.groupby('date'):
        ret_val[index] = sub_df['market_cap_usd'].astype(float).sum()
    return ret_val


def get_newcomers(conn, rank=100, no=10):
    cur = conn.cursor()
    cur.execute("SELECT * FROM newcomers_top{} limit {}".format(rank, no))
    df = pd.DataFrame(cur.fetchall(), columns=[element[0] for element in cur.description])
    return df

