import sys
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance/storageService/database')
from postgres import initiate_database_yf

if __name__=='__main__' :
    print('welcome To the Storage Service')

    initiate_database_yf()