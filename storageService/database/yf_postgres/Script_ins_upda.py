import sys
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance/storageService/database')
from postgres import insert_data,update_data
import sys 
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance/storageService/entites_APi_yf')
from init_database import insert_txt_into_object,updated_object_from_txt,get_ticket
from tickets import Ticket
'''
ticket=insert_txt_into_object('EURUSD=X')

insert_data(ticket)
'''




ticket=get_ticket('EURUSD=X')
ticket=updated_object_from_txt(ticket)

update_data(ticket)
