import sys
import os
path=os.getcwd()
last_stalsh=path[-1::-1].index('/')
precedent_folder=path[:-1*last_stalsh]  # get the precedent directory
sys.path.append(os.path.join(precedent_folder,'database'))
from postgres import insert_data,update_data
sys.path.append(s.path.join(precedent_folder,'entites_API')) # Add entites_API folder  in the models paths
from init_database import insert_txt_into_object,updated_object_from_txt,get_ticket
from tickets import Ticket
'''
ticket=insert_txt_into_object('EURUSD=X')

insert_data(ticket)
'''




ticket=get_ticket('EURUSD=X')
ticket=updated_object_from_txt(ticket)

update_data(ticket)
