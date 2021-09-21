import psycopg2
from datetime import datetime
import logging
import concurrent.futures
from endpoints.send import *
import configparser
#import tqdm
#import time
#import thread
#import json
#import calendar
#import csv
#import requests



#Load config , later to be moved to interface
config = configparser.ConfigParser()
config.read('config.cfg')# change to accept user selected file

# Assign config vars
MIGRATIONNAME = config['SESSION']['MIGRATIONNAME']
apikey = config['SESSION']['apikey']
LIMIT = config['SESSION']['LIMIT'] 
OFFSET = config['SESSION']['OFFSET']
ORDERBY = config['SESSION']['ORDERBY']
THREADS = config['SESSION']['THREADS']
hosturl = config['DATABASE']['hosturl']
database = config['DATABASE']['database']
dbuser = config['DATABASE']['dbuser']
dbpasswd = config['DATABASE']['dbpasswd']
port = config['DATABASE']['port']


#Logging config
logging.basicConfig(filename='./logs/' + MIGRATIONNAME + '.log', level=logging.INFO)
records_uploaded = './logs/' + MIGRATIONNAME + '.csv'

#DB Connection
db = psycopg2.connect(host=hosturl, database=database, user=dbuser, password=dbpasswd, port=port)
db.autocommit = True
cursor = db.cursor()

#api connection
file_url = "https://api.hubapi.com/filemanager/api/v3/files/upload"
note_url = "https://api.hubapi.com/engagements/v1/engagements"
querystring = { "hapikey" : apikey }



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
