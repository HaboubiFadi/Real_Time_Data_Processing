
import subprocess
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os 
import numpy as np
from psycopg2.extensions import register_adapter, AsIs

register_adapter(np.int64, AsIs)




def initiate_database_yf():
    path=os.getcwd()
    init_database=os.path.join(path,'entites_APi/Service.py')
    database_script = ['python', init_database]

    database_results = subprocess.run(database_script, capture_output=True, text=True)
    if database_results.returncode == 0:
    
        output = database_results.stdout
        print("Output:", output)
    else:
    
        error = database_results.stderr
        print("Error:", error) 

def insert_data(Data,database='postgres'):

    engine_string='postgresql://airflow_user:airflow_pass@postgres:5432/'+database

    engine = create_engine(engine_string) # engine for database information

    Session = sessionmaker(bind=engine) # Session for database manipulation
    session=Session()
    if isinstance(Data,list):
        session.add_all(Data)
    else:
        session.add(Data)  
    session.commit()
    session.close()


def update_data(updated_data,database='postgres'):

    engine_string='postgresql://airflow_user:airflow_pass@postgres:5432/'+database

    engine = create_engine(engine_string) # engine for database information

    
    Session = sessionmaker(bind=engine) # Session for database manipulation
    
    session=Session()
    if isinstance(updated_data,list):
        session.add_all(updated_data)
    else:
        session.add(updated_data)    
    session.commit()
    session.close()


def delete_data(data,database='postgres'):
    engine_string='postgresql://airflow_user:airflow_pass@postgres:5432/'+database

    engine = create_engine(engine_string) # engine for database information

    Session = sessionmaker(bind=engine) # Session for database manipulation
    session=Session()
    session.delete(data)
    session.close()







