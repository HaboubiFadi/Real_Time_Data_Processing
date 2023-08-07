
import subprocess
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine







def initiate_database_yf():
    init_database='/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance/storageService/entites_APi/yf_init_database.py'
    database_script = ['python3', init_database]

    database_results = subprocess.run(database_script, capture_output=True, text=True)
    if database_results.returncode == 0:
    
        output = database_results.stdout
        print("Output:", output)
    else:
    
        error = database_results.stderr
        print("Error:", error) 

def insert_data(Data,database='finance_api'):

    engine_string='postgresql://airflow_user:airflow_pass@localhost/'+database

    engine = create_engine(engine_string) # engine for database information

    Session = sessionmaker(bind=engine) # Session for database manipulation
    session=Session()
    if isinstance(Data,list):
        session.add_all(Data)
    else:
        session.add(Data)  
    session.commit()
    session.close()


def update_data(updated_data,database='finance_api'):

    engine_string='postgresql://airflow_user:airflow_pass@localhost/'+database

    engine = create_engine(engine_string) # engine for database information

    
    Session = sessionmaker(bind=engine) # Session for database manipulation
    
    session=Session()
    if isinstance(updated_data,list):
        session.add_all(updated_data)
    else:
        session.add(updated_data)    
    session.commit()
    session.close()


def delete_data(data,database='finance_api'):
    engine_string='postgresql://airflow_user:airflow_pass@localhost/'+database

    engine = create_engine(engine_string) # engine for database information

    Session = sessionmaker(bind=engine) # Session for database manipulation
    session=Session()
    session.delete(data)
    session.close()

