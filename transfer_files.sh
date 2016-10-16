#!/bin/sh
AIRFLOW_HOME=/home/airflow/airflow_home
REMOTE_SSH=<add_your_remote_server_here>
/usr/bin/scp $AIRFLOW_HOME/dags/echo_date.sh $REMOTE_SSH:/tmp/
