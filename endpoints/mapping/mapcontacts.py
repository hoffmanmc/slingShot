import json
import csv

CSV = './csv/contacts_maps.csv'

def load_csv(csv_file):
    '''loads csv as list of dicts containing 'internal_tag' and 'external_tag' values'''
    with open(csv_file, 'r', newline='') as openedcsv:
        reader = csv.DictReader(openedcsv)
        tag_map = []
        for row in reader:
            tag_map.append(row)
        return tag_map

def map_hs_tag(old_tag):
    '''returns a list of hubspot internal property values to be updated'''
    #Get map values from .csv
    tag_map = load_csv(CSV)
    
    #check if old_tag matches map values, if so add to tag_list and return
    tag_list = []
    for tag in tag_map:
        length = len(tag['external_tag'])
        check_from = old_tag[:length] #Account for trailing characters / loose name conventions
        check_to = tag['external_tag']
        if check_from == check_to:
            new_tag = tag['internal_tag']
            tag_list.append(new_tag)
    return tag_list

def make_prop(hsname):
    '''creates a prop dictionary with following format'''
    prop = {'property': hsname, 'value': 'true',}
    return prop
 
def build_json(HsId, old_tag):
    '''Create json blob from record'''
    #Log some info
    print("HS ID: " + HsId)
    print("Old tag: " + old_tag)

    #map old tag to new 
    tags = map_hs_tag(old_tag)
    
    #build json blob
    properties = {'properties': [],}
    for tag in tags:
        prop = make_prop(tag)
        properties['properties'].append(prop)
    payload = json.dumps(properties)
    
    print(payload)

    return payload
