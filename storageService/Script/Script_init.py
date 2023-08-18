import sys
import os
path=os.getcwd()
last_stalsh=path[-1::-1].index('/')
precedent_folder=path[:-1*last_stalsh]  # get the precedent directory
print("this the directory:",precedent_folder)
sys.path.append(os.path.join(path,'database'))
from postgres import initiate_database_yf

if __name__=='__main__' :
    print('welcome To the Storage Service')

    initiate_database_yf()