from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('lakehouse_etl',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    bronze = BashOperator(
        task_id='bronze_load',
        bash_command='docker exec spark /opt/spark/bin/spark-submit --master local[*] /opt/spark/scripts/bronze_load.py'
    )

    silver = BashOperator(
        task_id='silver_transform',
        bash_command='docker exec spark /opt/spark/bin/spark-submit --master local[*] /opt/spark/scripts/silver_transform.py'
    )

    gold = BashOperator(
        task_id='gold_aggregate',
        bash_command='docker exec spark /opt/spark/bin/spark-submit --master local[*] /opt/spark/scripts/gold_aggregate.py'
    )

    bronze >> silver >> gold
