from airflow import DAG
from airflow.operators.python import PythonOperator  #used to define task in which is nothing but python function in short
from datetime import datetime


#define our task 
def preprocess_data():
    print("preprocess... data")

#task 2
def train_model():
    print("training the model") 


def evaluate_model():
    print("Evaluting the Model")




#define the DAG 
with DAG(
    "ml_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval='@weekly'
) as dag:
    #define the Task

    preprocess=PythonOperator(task_id="preprocess_task",python_callable=preprocess_data)
    train=PythonOperator(task_id="train_task",python_callable=train_model)
    evaluate=PythonOperator(task_id="Evaluate_task",python_callable=evaluate_model )


    #set Dependancies
    preprocess >> train >>evaluate