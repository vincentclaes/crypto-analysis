import requests
from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1)
}

dag = DAG(
    dag_id='newcomers', default_args=args,
    schedule_interval="@hourly",
    dagrun_timeout=timedelta(minutes=60))


def create_newcomers(rank, no, *args, **kwargs):
    url = "http://0.0.0.0:5004/newcomers"
    querystring = {"rank": rank, "no": no}
    result = requests.request("POST", url, params=querystring)
    print(result.content)

get_coinmarketcap_data = BashOperator(
    task_id='get_coinmarketcap_data',
    bash_command='sudo python /home/ec2-user/projects/coinmarketcap_data/coinmarketcap_data.py',
    dag=dag)

create_newcomers_top100 = PythonOperator(
    task_id='create_newcomers_top100',
    provide_context=True,
    python_callable=create_newcomers,
    op_kwargs={'rank': 100, 'no' : 100},
    dag=dag)

create_newcomers_top200 = PythonOperator(
    task_id='create_newcomers_top200',
    provide_context=True,
    python_callable=create_newcomers,
    op_kwargs={'rank': 200, 'no' : 100},
    dag=dag)


get_coinmarketcap_data.set_downstream(create_newcomers_top100)
create_newcomers_top100.set_downstream(create_newcomers_top200)