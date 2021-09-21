import json

def send_record(HsId, old_tag):
    ''' send json and log response '''
    payload = build_json(HsId, old_tag)
    url = 'https://api.hubapi.com/contacts/v1/contact/vid/' + HsId + '/profile'
    
    headers = {}
    headers['Content-Type'] = 'application/json'

    try:
        response = requests.post(url=url, headers=headers, data=payload, params=querystring)
        print("Response status: " + str(response.status_code) + " old_tag: " + old_tag)
        print(response.text)
        return response
    except:
        print("Something went wrong! check log file.")
        logging.info(f'Error sending tag {old_tag} for company {HsId}')
        return 

def build_file_json(file_id, file_name):
    '''Create json blob from record'''
    #print(file_id, file_name)
    #build json blob
    file_options = {
        'access': 'PUBLIC_INDEXABLE',
        "overwrite": False,
        #'duplicateValidationStrategy': 'NONE',
        #'duplicateValidationScope': 'EXACT_FOLDER'
    }
    #Cut off file_id after first space.
    split = file_id.split(" ")[0]
    filepath =str('./Agreements/'+split)
    files_data = {
        'file': (file_name, open(filepath, 'rb'), 'application/octet-stream'),
        'options': (None, json.dumps(file_options), 'text/strings'),
        'folderPath': (None, '/Agreements', 'text/strings')
    }
 
    print("file json created, id " + file_id + " name " + file_name)
    #print(files_data)
    #data = json.dumps(files_data)
    return files_data


def build_note_json(file_hs_id, description, company_hs_id):

    payload = json.dumps({
        "engagement": {
            "active": 'true',
            "ownerId": 1,
            "type": "NOTE",
            #"timestamp":
            },
        "associations": {
            "contactIds": [],
            "companyIds": [company_hs_id],
            "dealIds": [],
            "ownerIds": []
        },
        "attachments": [
            {
                "id": file_hs_id
            }
        ],
        "metadata": {
            "body": description
        }
    });
    
    return payload
