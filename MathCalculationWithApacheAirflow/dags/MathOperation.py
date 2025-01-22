from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define Function for each task
def start_number(**context):
    context["ti"].xcom_push(key="current_value", value=10)
    print("10")

def add_five(**context):
    current_value = context["ti"].xcom_pull(key="current_value", task_ids="Start_task")
    new_value = current_value + 5
    context["ti"].xcom_push(key="current_value", value=new_value)
    print(f"Added 5 to the Current Value: {new_value}")

def multiply_by_two(**context):
    current_value = context["ti"].xcom_pull(key="current_value", task_ids="Add_five")
    new_value = current_value * 2
    context["ti"].xcom_push(key="current_value", value=new_value)
    print(f"Multiplied the Current Value by 2: {new_value}")

def subtract_by_three(**context):
    current_value = context["ti"].xcom_pull(key="current_value", task_ids="Multiplied_By_2")
    new_value = current_value - 3
    context["ti"].xcom_push(key="current_value", value=new_value)
    print(f"Subtracted 3 from the Current Value: {new_value}")

def squaring_the_value(**context):
    current_value = context["ti"].xcom_pull(key="current_value", task_ids="Subtracted_By_3")
    new_value = current_value ** 2
    context["ti"].xcom_push(key="current_value", value=new_value)
    print(f"Square of the Value is: {new_value}")

# Define the DAG
with DAG(
    dag_id="math_sequence_dag",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@once",
    catchup=False
) as dag:
    # Define the tasks
    start_number_task = PythonOperator(
        task_id="Start_task",
        python_callable=start_number,
    )

    add_five_task = PythonOperator(
        task_id="Add_five",
        python_callable=add_five,
    )

    multiply_by_two_task = PythonOperator(
        task_id="Multiplied_By_2",
        python_callable=multiply_by_two,
    )

    subtract_by_three_task = PythonOperator(
        task_id="Subtracted_By_3",
        python_callable=subtract_by_three,
    )

    squaring_the_value_task = PythonOperator(
        task_id="Square_Value",
        python_callable=squaring_the_value,
    )

    # Set task dependencies
    start_number_task >> add_five_task >> multiply_by_two_task >> subtract_by_three_task >> squaring_the_value_task
