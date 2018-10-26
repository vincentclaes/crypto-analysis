import os
from datetime import timedelta

import airflow
from airflow.contrib.hooks import SSHHook
from airflow.contrib.operators.ssh_execute_operator import SSHExecuteOperator
from airflow.models import DAG

sshHook = SSHHook(conn_id="delta-crypto")

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),
    'catchup': False
}
DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")  # airflow-log-cleanup

dag = DAG(
    dag_id=DAG_ID, default_args=args,
    schedule_interval="*/5 * * * *",
    dagrun_timeout=timedelta(minutes=60),
    catchup=False
)

newcomers_bittrex = SSHExecuteOperator(
    task_id="newcomers_bittrex",
    bash_command="""sudo python /home/ec2-user/projects/crypto-analysis/entry.py newcomers_bittrex""",
    ssh_hook=sshHook,
    xcom_push=True,
    dag=dag)
