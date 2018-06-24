from datetime import timedelta

import airflow
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
    dagrun_timeout=timedelta(minutes=60),
    catchup=False
)

get_coinmarketcap_data = BashOperator(
    task_id='get_coinmarketcap_data',
    bash_command='sudo python /home/ec2-user/projects/coinmarketcap_data/coinmarketcap_data.py',
    dag=dag)

create_newcomers_top100 = SSHExecuteOperator(
    task_id="create_newcomers_top100",
    bash_command="""sudo python /home/ec2-user/projects/crypto-analysis/entry.py newcomers --rank 100 --no 10 --latest""",
    ssh_hook=sshHook,
    xcom_push=True,
    dag=dag)

tweet_newcomers_top100 = SSHExecuteOperator(
    task_id='tweet_newcomers_top100',
    provide_context=True,
    bash_command="""sudo python /home/ec2-user/projects/crypto-analysis/entry.py tweet --rank 100 --id {{ ti.xcom_pull(task_ids='create_newcomers_top100') }}""",
    ssh_hook=sshHook,
    dag=dag)

create_newcomers_top200 = SSHExecuteOperator(
    task_id="create_newcomers_top200",
    bash_command="""sudo python /home/ec2-user/projects/crypto-analysis/entry.py newcomers --rank 200 --no 10 --latest""",
    ssh_hook=sshHook,
    xcom_push=True,
    dag=dag)

tweet_newcomers_top200 = SSHExecuteOperator(
    task_id='tweet_newcomers_top200',
    provide_context=True,
    bash_command="""sudo python /home/ec2-user/projects/crypto-analysis/entry.py tweet --rank 200 --id {{ ti.xcom_pull(task_ids='create_newcomers_top200') }}""",
    ssh_hook=sshHook,
    dag=dag)

get_coinmarketcap_data.set_downstream(create_newcomers_top100)
create_newcomers_top100.set_downstream(tweet_newcomers_top100)
tweet_newcomers_top100.set_downstream(create_newcomers_top200)
create_newcomers_top200.set_downstream(tweet_newcomers_top200)
