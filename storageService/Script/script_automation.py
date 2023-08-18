import sys
import os
path=os.getcwd()
last_stalsh=path[-1::-1].index('/')
precedent_folder=path[:-1*last_stalsh]  # get the precedent directory
sys.path.append(os.path.join(precedent_folder,'database')) # Add database folder in the models paths


from postgres import insert_data,update_data
sys.path.append(os.path.join(precedent_folder,'entites_API')) # Add entites_API folder  in the models paths


from init_database import update_all_in_database
from tickets import Ticket
import time

i=0
while i<3:
    print('*********begin update process*********')
    tickets=update_all_in_database()

    update_data(tickets)
    print('*********end update process*********')
    i=i+1
    time.sleep(60)