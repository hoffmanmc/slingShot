import sys
import csv
import base64

################
####:consts:####
################

ENCODED_FILE = 1 # column of encoded file
FILE_NAME = 19 # column of user facing filename
FILE_ID = 9 # column of files ID
LOAD_CSV_NAME = './files/sf_documents.csv' # name of csv file to read
NAME_ID_LOG = './files/sf_files_name_to_id.csv' # name of csv to log file id and filename 

################
####:setup:#####
################

csv.field_size_limit(sys.maxsize)

################
####:funcs:#####
################

def decode_file(thisid, thisfile):
    with open('./files/decoded/' + thisid, 'wb') as image:
        image.write(base64.b64decode(thisfile))

def name_id_to_csv(sf_id, file_name):
    with open(NAME_ID_LOG, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        data = [sf_id, file_name]
        writer.writerow(data)

def run(filename):
    '''load data from csv and run functions over it'''
    with open(filename, 'r', newline='', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data = list(row)
            thisid = data[FILE_ID]
            thisname = data[FILE_NAME]
            thisfile = data[ENCODED_FILE]
            
            #decode and log file id & name to csv 
            decode_file(thisid, thisfile) #decode base64 data
            name_id_to_csv(thisid, thisname) #send id and name to sf_files_name_to_id.csv

##############
####:run:#####
##############

run(LOAD_CSV_NAME)



