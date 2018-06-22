from datetime import timedelta

import airflow
import requests
from airflow.contrib.hooks import SSHHook
from airflow.contrib.operators.ssh_execute_operator import SSHExecuteOperator
from airflow.models import DAG

sshHook = SSHHook(conn_id="delta-crypto")

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1)
}

dag = DAG(
    dag_id='newcomers_update', default_args=args,
    schedule_interval="*/20 * * * *",
    dagrun_timeout=timedelta(minutes=60))


def create_newcomers(rank, no, *args, **kwargs):
    url = "http://0.0.0.0:5004/newcomers"
    querystring = {"rank": rank, "no": no}
    result = requests.request("POST", url, params=querystring)
    print(result.content)


update_newcomers_top100 = SSHExecuteOperator(
    task_id="update_newcomers_top100",
    bash_command="""sudo python /home/ec2-user/projects/crypto-analysis/entry.py newcomers_update --rank 100""",
    ssh_hook=sshHook,
    dag=dag)

update_newcomers_top200 = SSHExecuteOperator(
    task_id="update_newcomers_top200",
    bash_command="""sudo python /home/ec2-user/projects/crypto-analysis/entry.py newcomers_update --rank 200""",
    ssh_hook=sshHook,
    dag=dag)

update_newcomers_top100.set_downstream(update_newcomers_top200)
