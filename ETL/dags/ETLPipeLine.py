from airflow import DAG
from airflow.providers.http.operators.http import SimpleHTTPOperator
from airflow.operators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json 

with DAG(
    dag_id="Nasa_apod_postgress",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False


     
) as dag:
    #step 1: create the table if it doesnt exist
    @task
    def create_table():
        #initialize the Postgress Hook: it is used to intract with the Postgress server
        postgress_Hook = PostgresHook(postgress_conn_id="my_postgress_connetion")

        create_table_query="""CREATE TABLE IF NOT EXIST apod_data (
        id SERIAL PRIMARY KEY,
        title  VARCHAR(255),
        explanation TEXT,
        url TEXT,
        date DATE,
        media_type VARCHAR(50)
        );


        """

        postgres_hook.run(create_table_query)

    #step 2: Extract the NASA api Data(APOD)-Astronomy picrure of the day
 
    extract_apod=SimpleHTTPOperator(
        task_id='task_id',
        http_conn_id='nasa_api',
        endpoint='planetary/apod'
    )
    #Step 3: Transform the Data ,Pick the information that i need to save
    
    #Step:4  : Load the Data Into PostgressSql


    #step5: Verify the data DBViewer



    #step 6: Define the Task Dependancies
     
