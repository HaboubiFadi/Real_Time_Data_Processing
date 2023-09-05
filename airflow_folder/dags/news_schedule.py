from airflow import DAG
from datetime import datetime,timedelta
#from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
import time
default_arg={
'owner': 'airflow',
'start_date': days_ago(1), 
'schedule_interval': '0 * * * *', 
'retries':2,
'retry_delay':timedelta(seconds=20)


}


def get_started():
    print('welcome to the airflow service manager')
    time.sleep(5)
def end_dags():
    print('Au revoir')
    time.sleep(5)    

with DAG (
    dag_id='schedule_news_extraction',
    description='schedule_news_extract',
    default_args=default_arg,
    catchup=False



) as dag :
    start_dags=PythonOperator(
        task_id='Get_started',
        python_callable=get_started

    )

    data_ingest_service=DockerOperator(
    task_id='data_ingest_service_container',
    image='final_dataingest:latest',
    docker_url='unix://var/run/docker.sock',
    api_version='auto',
    command=["python","-u","auto_news_script.py"],
    network_mode='rmoff_kafka',
    auto_remove=True 
   
)
    data_process_task=DockerOperator(
    task_id='data_process_service_container',
    image='final_dataprocess:latest',
    docker_url='unix://var/run/docker.sock',

    api_version='auto',
    environment={'reception_news': 'auto_ingest_news', 
       'emission_news' : 'auto_process_news'},
    network_mode='rmoff_kafka',
)

    data_storage_task=DockerOperator(
    task_id='data_storage_service_container',
    image='final_datastorage:latest',
    docker_url='unix://var/run/docker.sock',

    
    api_version='auto',
    command=["python","-u","auto_news_script.py"],
    network_mode='rmoff_kafka',
    )

    end_dag=PythonOperator(
        task_id='Au_revoir',
        python_callable=end_dags


    )

    
start_dags>>[data_ingest_service,data_process_task,data_storage_task]>>end_dag