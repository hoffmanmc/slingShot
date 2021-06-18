import psycopg2
from datetime import datetime
import logging
import concurrent.futures
from endpoints.send import *
#import tqdm
#import time
#import thread
#import json
#import calendar
#import csv
#import requests

##################################################
##  Change below constants using the .env file  ##
##################################################

MIGRATIONNAME = 'files_to_production' # names save data and log files 
hapikey = '' # hubspot api key
LIMIT = '' # Num of rows to send (mind the api limit)
OFFSET = '0' # offset, choose where to start database query
ORDERBY = '' # order query 
host = '' # database url
port = 25060 # " port 
database = '' # " database
dbuser = '' # " user 
dbpasswd = '' # " password 
TABLE = '' # " table
#T/P <= to implement, thread or process?
THREADS = 2 # Number of threads to execute 


##################################################
##                Connections                   ##
##################################################

#DB Connection
db = psycopg2.connect(host=host, database=database, user=dbuser, password=dbpasswd, port=port)
db.autocommit = True
cursor = db.cursor()

#HS api connection
file_url = "https://api.hubapi.com/filemanager/api/v3/files/upload"
note_url = "https://api.hubapi.com/engagements/v1/engagements"
querystring = { "hapikey" : hapikey }

#Logging config
logging.basicConfig(filename='./logs/' + MIGRATIONNAME + '.log', level=logging.INFO)

#Open csv for logging
records_uploaded = './logs/' + MIGRATIONNAME + '.csv'

##################################################
##                Functions                     ##
##################################################

def query(table, orderby, limit, offset):
    '''Query a single table of postgres db, return a 'chunk' of selected records to process'''
    print("Querying database...")
    cursor.execute("SELECT * FROM " + table + " ORDER BY " + orderby + " LIMIT (%s) OFFSET (%s)", (limit, offset))
    pgdb_chunk = cursor.fetchall()
    print("Database chunk selected.")
    return pgdb_chunk

def exec_pool(THREADS, pgdb_chunk, send_it):
    '''takes number of threads, database chunk to iter over, and send_it function'''
    '''executes send_it func on each row of pgdb_chunk'''
    #Execute thread pool
    executor = concurrent.futures.ThreadPoolExecutor(THREADS) #Select number of threads to use 
    futures = [executor.submit(send_it, num, row) for num, row in enumerate(pgdb_chunk)]
    concurrent.futures.wait(futures)

def save_state():
    '''save upload state to resume progress later'''
    #save some data to a file to be loaded later

def run():
    '''Main logic: acces db, select record, map ids, build request, send'''
    # get / load data from user
    selection = 'foo'
    
    send_it = make_send(make, send = select_request(selection))
    print('Querying database...')
    pgdb_chunk = query(TABLE, ORDERBY, LIMIT, OFFSET)
    print('Database chunk selected.')

    #Give some info 
    print("Entering loop...    " + str(datetime.now()))
    start_time = str(datetime.now())
    exec_pool(THREADS, pgdb_chunk, send_it)
    
    #Finished info
    print("Finished. Start time " + start_time + ", time now " + str(datetime.now()))

#########################################################

run()
db.close()
