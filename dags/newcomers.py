
from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1)
}

dag = DAG(
    dag_id='newcomers', default_args=args,
    schedule_interval='0 * * * *',
    dagrun_timeout=timedelta(minutes=60))

get_coinmarketcap_data = BashOperator(
    task_id='get_coinmarketcap_data',
    bash_command='python /home/ec2-user/projects/coinmarketcap_data/coinmarketcap_data.py',
    dag=dag)

create_newcomers_top100 = BashOperator(
    task_id='create_newcomers_top100',
    bash_command='python /home/ec2-user/projects/crypto-analysis/scripts/get_newcomers.py 100 100',
    dag=dag)

create_newcomers_top200 = BashOperator(
    task_id='create_newcomers_top200',
    bash_command='python /home/ec2-user/projects/crypto-analysis/scripts/get_newcomers.py 200 100',
    dag=dag)

get_coinmarketcap_data >> create_newcomers_top100 >> create_newcomers_top200