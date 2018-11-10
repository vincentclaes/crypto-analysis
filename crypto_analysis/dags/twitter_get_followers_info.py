from __future__ import print_function

import json
import time
from datetime import datetime, timedelta
from pprint import pprint

from airflow.models import DAG
from airflow.models import Variable
from airflow.operators import PythonOperator
from builtins import range

seven_days_ago = datetime.combine(
    datetime.today() - timedelta(7), datetime.min.time())
MAX_COUNT = 3000
COUNT = 200
NAMES = Variable.get("twitter_users")

args = {
    'owner': 'airflow',
    'start_date': seven_days_ago,
}

dag = DAG(
    dag_id='twitter_get_followers_info',
    default_args=args,
    catchup=False,
    schedule_interval=None)


def get_followers_info(name, cursor, count):
    '''This is a function that will run within the DAG execution'''
    import requests

    url = "https://0wb3echzu8.execute-api.us-east-1.amazonaws.com/dev/twitter/twitter_followers_info_dump"

    querystring = {"name": name, "cursor": cursor, "count": count}

    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "9455272a-d753-4eec-b727-25abae3375d3"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    return json.loads(response.content).get('followers').get('next_cursor')


def get_paged_followers_info(names, count, max_count, *args, **kwargs):
    iterations = max_count / count
    for name in names:  
        cursor = -1 # default value to get the first list of users
        print('get user info for : {}'.format(name))
        for i in range(iterations):
            if i >= max_count:
                break
            time.sleep(10)
            print('running for cursor : {}'.format(cursor))
            cursor = get_followers_info(name, cursor, count)


PythonOperator(
    task_id='get_paged_followers_info',
    python_callable=get_paged_followers_info,
    op_kwargs={'count': COUNT, 'max_count': MAX_COUNT, 'name': NAMES},
    dag=dag,
    xcom_push=True,
    provide_context=True)

