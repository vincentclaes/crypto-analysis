import os
from datetime import timedelta

import airflow
import pandas as pd
import requests
from airflow.models import DAG
from airflow.operators import PythonOperator

from crypto_analysis.databases import queries

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),
    'catchup': False
}
DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")  # airflow-log-cleanup

dag = DAG(
    dag_id=DAG_ID, default_args=args,
    schedule_interval="* * * * *",
    dagrun_timeout=timedelta(minutes=60),
    catchup=False
)


def newcomers_bittrex():
    data = get_bittrex_data()
    df_latest = pd.read_json(data)

    local_data = get_local_data()


def get_local_data(df_latest):
    df = queries.get_table('bittrex')


def get_bittrex_data():
    url = "https://bittrex.com/api/v1.1/public/getmarkets"
    return requests.request("GET", url)


run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=newcomers_bittrex,
    dag=dag)
