from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator


from airflow.decorators import task

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json 

with DAG(
    dag_id="nasa_apod_postgres",
    start_date=days_ago(1),
    schedule="@daily",
    catchup=False


     
) as dag:
    #step 1: create the table if it doesnt exist
    @task
    def create_table():
        #initialize the Postgress Hook: it is used to intract with the Postgress server
        postgress_Hook = PostgresHook(postgres_conn_id='my_postgres_connection')

        create_table_query="""CREATE TABLE IF NOT EXISTS apod_data (
 
        id SERIAL PRIMARY KEY,
        title  VARCHAR(255),
        explanation TEXT,
        url TEXT,
        date DATE,
        media_type VARCHAR(50)
        );


        """

        postgress_Hook.run(create_table_query)

    #step 2: Extract the NASA api Data(APOD)-Astronomy picrure of the day
    #Api_key=https://api.nasa.gov/planetary/apod?api_key=HwhXybGdOhtHGVwmm0GLQ8biJaQ4Zhjdj9TVMsf7
 
    extract_apod=SimpleHttpOperator(
        task_id='task_id',
        http_conn_id='nasa_api',# connection id defined in Airflow for NASA API
        endpoint='planetary/apod', ## NASA API endpoint for APOD(Astronomy Picture Of the Day)
        method="GET",
        data={"api_key": "{{ conn.nasa_api.extra_dejson['api_key'] }}"}, # using the API key from the connection 
        response_filter=lambda response:response.json(), #convert response to the Json using Lambda
    )
    #Step 3: Transform the Data ,Pick the information that i need to save
    @task
    def transform_apod_data(response):
        apod_data = {
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),  # fixed typo
            'url': response.get('url', ''),
            'date': response.get('date', ''),  # fixed the key
            'media_type': response.get('media_type', ''),
        }
        return apod_data

    



    #Step:4  : Load the Data Into PostgressSql

    @task
    def load_data_to_postgres(apod_data):
        #initialize the PostgresHook
        postgres_hook=PostgresHook(postgres_conn_id='my_postgres_connection')

        #define SQL insert Query
        insert_query="""INSERT INTO apod_data (title,explanation, url ,date ,media_type) VALUES (%s,%s,%s,%s,%s);
                """

        #execute the SQL query
        postgres_hook.run(insert_query,parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type'],

        ))
    #step5: Verify the data DBViewer   
     



    #step 6: Define the Task Dependancies
    #Extract

    create_table() >> extract_apod
    api_response = extract_apod.output
    transform_data = transform_apod_data(api_response)
    load_data_to_postgres(transform_data)
     
