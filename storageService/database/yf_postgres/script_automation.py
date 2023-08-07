import sys
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance/storageService/database')
from postgres import insert_data,update_data
import sys 
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance/storageService/entites_APi_yf')
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