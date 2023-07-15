from Service import insert_data,update_data
import sys 
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance/storageService/entites_APi_yf')
from init_database import insert_txt_into_object,updated_object_from_txt
from tickets import Ticket
'''
ticket=insert_txt_into_object('EURUSD=X')

insert_data(ticket)
'''





ticket=updated_object_from_txt('EURUSD=X')

update_data(ticket)
