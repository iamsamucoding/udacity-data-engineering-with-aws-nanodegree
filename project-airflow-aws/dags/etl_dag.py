from datetime import datetime, timedelta
import os
from airflow.operators.empty import EmptyOperator

from operators import StageToRedshiftOperator

import logging


from airflow.decorators import dag, task

default_args = {
    'owner': 'Sparkify',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 31),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}


@dag(default_args=default_args)
def etl():
    begin_execution = EmptyOperator(task_id='Begin_execution')

    @task
    def inspect_operators_task():
        logging.info(f'\n\n######## INSPECT OPERATORS')
        logging.info(help(airflow.operators))
    inspect_operators = inspect_operators_task()

    end_execution = EmptyOperator(task_id='End_execution')

    begin_execution >> inspect_operators
    inspect_operators >> end_execution

etl_dag = etl()
