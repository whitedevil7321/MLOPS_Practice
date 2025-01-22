from airflow import DAG
from airflow.decorators import task
from datetime import datetime


#define the DAG
with DAG(
    dag_id="math_sequance_dag_with_airflow",
    start_date=datetime(2023,1,1),
    schedule_interval="@once",
    catchup=False,



) as dag:
    @task
    def start_number():
        initial_number=20
        print(f"The initial Number Is:{initial_number}")
        return initial_number
    
    @task
    def add_five(number):
        new_value=number+5
        print(f"Added 5 to the Number and then the Number is:{new_value}")
        return new_value
    
    @task
    def Multiply_by_2(number):
        new_value=number*2
        print(f"MUltiplied the Number by 2 and then the Number is:{new_value}")
        return new_value
    
    @task
    def Subtracted_by_3(number):
        new_value=number-3
        print(f"Subtracted 5 from the Number and then the Number is:{new_value}")
        return new_value
    
    

    @task
    def Squre_the_number(number):
        new_value=number**2
        print(f"Square Of the Number is:{new_value}")
        return new_value
    

    start_value=start_number()
    add_value=add_five(start_value)
    multiply_value=Multiply_by_2(add_value)
    subtract_value=Subtracted_by_3(multiply_value)
    Square_value=Squre_the_number(subtract_value)
    


    
