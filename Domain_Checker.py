"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators import SSHExecuteOperator
from airflow.contrib.hooks import SSHHook
from airflow.operators import HttpSensor, SimpleHttpOperator
from datetime import datetime, timedelta
from airflow.models import Variable


AIRFLOW_HOME=#set here data path

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'domain_checker', default_args=default_args, schedule_interval=timedelta(1))

#define ssh01 on Admin > Configuration >
ssh_hook_01 = SSHHook(conn_id='ssh01')

t0 = BashOperator(
    task_id='transfer_files_to_remote',
    bash_command= AIRFLOW_HOME + '/dags/transfer_files.sh',
    params={},
    retries=1,
    dag=dag)

t1 = SSHExecuteOperator(
    task_id='verify_transfer_to_remote',
    ssh_hook = sssh_hook_01,
    bash_command= AIRFLOW_HOME + '/dags/echo_date.sh',
    params={},
    retries=1,
    dag=dag)

domain01_sensor = HttpSensor(
    task_id='domain01_sensor',
    endpoint='',
    http_conn_id='http_domain01',
    retries=1,
    params={},
    dag=dag)

domain02_sensor = HttpSensor(
    task_id='domain02_sensor',
    endpoint='',
    http_conn_id='http_domain02',
    retries=1,
    params={},
    dag=dag)

domain03_sensor = HttpSensor(
    task_id='domain03_sensor',
    endpoint='',
    http_conn_id='http_domain03',
    retries=1,
    params={},
    dag=dag)

domain02_sensor.set_upstream(domain01_sensor)
domain03_sensor.set_upstream(domain02_sensor)
t0.set_upstream(domain03_sensor)
t1.set_upstream(t0)
