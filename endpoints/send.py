def build_note():
    return

def send_note():
    return

def map_note():
    return


def select_request(selection):
    '''given target endpoint, select functions for building json blob and sending'''
    select = {
        'note': [build_note, send_note, map_note],
        1: "one",
        2: "two",
    }
  
    # get() method of dictionary data type returns 
    # value of passed argument if it is present 
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    
    make = select.get(selection[0], 'nothing')
    send = select.get(selection[1], 'nothing')

    return make, send 


def make_send(make, send):
    def send_it(data):
        send(make(data))
       
    return send_it

def get_send():


#def send_it(num, row):
#    
#    try:
#        #Send file
#        file_response = send_file(file_id, file_name)
        #print(file_response)

        #Collect hs_id for associations 
#        file_response_json = json.loads(file_response.text)
#        file_hs_id = str(file_response_json['objects'][0]['id'])
#        print("HS ID: " + file_hs_id)

        #Create note engagement with associations
#        note_response = send_note(file_hs_id, description, company_hs_id)

        #Collect hs note id 
#        note_response_json = json.loads(note_response.text)
#        note_id = str(note_response_json['engagement']['id'])
        #print("Deal ID: " + str(note_deal_id))
        
        #Logging
#        filestatus = file_response.status_code
#        notestatus =  note_response.status_code
#        log_to_csv(file_hs_id, file_id, company_hs_id, note_id, filestatus, notestatus)
#        print("Uploaded file number " + str(num) + ", company id: " + company_hs_id +", file id: " + file_id) 
        
#    except:
#        logging.info(f'Error executing send for file: {file_id}')
