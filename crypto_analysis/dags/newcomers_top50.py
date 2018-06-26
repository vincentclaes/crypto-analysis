from datetime import timedelta

import airflow
from airflow.contrib.hooks import SSHHook
from airflow.contrib.operators.ssh_execute_operator import SSHExecuteOperator
from airflow.models import DAG

sshHook = SSHHook(conn_id="delta-crypto")

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1)
}

dag = DAG(
    dag_id='newcomers_top50', default_args=args,
    schedule_interval="30 * * * *",
    dagrun_timeout=timedelta(minutes=60),
    catchup=False
)

create_newcomers_top50 = SSHExecuteOperator(
    task_id="create_newcomers_top50",
    bash_command="""sudo python /home/ec2-user/projects/crypto-analysis/entry.py newcomers --rank 50 --no 10 --latest""",
    ssh_hook=sshHook,
    xcom_push=True,
    dag=dag)

tweet_newcomers_top50 = SSHExecuteOperator(
    task_id='tweet_newcomers_top50',
    provide_context=True,
    bash_command="""sudo python /home/ec2-user/projects/crypto-analysis/entry.py tweet --rank 50 --id {{ ti.xcom_pull(task_ids='create_newcomers_top50') }}""",
    ssh_hook=sshHook,
    dag=dag)

create_newcomers_top50.set_downstream(tweet_newcomers_top50)
