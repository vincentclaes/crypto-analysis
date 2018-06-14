from datetime import timedelta

import airflow
import requests
from airflow.contrib.hooks import SSHHook
from airflow.contrib.operators.ssh_execute_operator import SSHExecuteOperator
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator

sshHook = SSHHook(conn_id="delta-crypto")


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

create_newcomers_top100 = SSHExecuteOperator(
    task_id="create_newcomers_top100",
    bash_command="""sudo python /home/ec2-user/projects/crypto-analysis/entry.py --rank 100 --no 10 --latest""",
    ssh_hook=sshHook,
    dag=dag)

create_newcomers_top200 = SSHExecuteOperator(
    task_id="create_newcomers_top200",
    bash_command="""sudo python /home/ec2-user/projects/crypto-analysis/entry.py --rank 200 --no 10 --latest""",
    ssh_hook=sshHook,
    dag=dag)


get_coinmarketcap_data.set_downstream(create_newcomers_top100)
create_newcomers_top100.set_downstream(create_newcomers_top200)