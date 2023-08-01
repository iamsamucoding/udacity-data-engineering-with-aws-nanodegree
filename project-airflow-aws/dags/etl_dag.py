from datetime import datetime, timedelta

from airflow.operators.empty import EmptyOperator
from operators import StageToRedshiftOperator

from airflow.models import Variable

import logging


from airflow.decorators import dag, task

default_args = {
    'owner': 'Sparkify',
    'depends_on_past': False,
    'start_date': datetime(2018, 11, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}


@dag(default_args=default_args,
     schedule_interval='0 * * * *')
def etl():
    # airflow variables
    s3_bucket = Variable.get('s3_bucket')
    log_data_prefix = Variable.get('s3_prefix_log_data')
    song_data_prefix = Variable.get('s3_prefix_song_data')
    region = Variable.get('region')

    begin_execution = EmptyOperator(task_id='Begin_execution')

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        table='staging_events',
        s3_bucket=s3_bucket,
        s3_key=log_data_prefix,
        region=region,
        file_format='JSON')

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        table='staging_songs',
        s3_bucket=s3_bucket,
        s3_key=song_data_prefix,
        region=region,
        file_format='JSON')
    

    end_execution = EmptyOperator(task_id='End_execution')

    begin_execution >> [stage_events_to_redshift, stage_songs_to_redshift] >>\
    end_execution

etl_dag = etl()
