import json
import csv
import logging

MAPCSV = './csv/company_maps.csv'
TIERCSV = './csv/track_tiers.csv'
logging.basicConfig(filename='./logs/company_tag_to_production_errors.log', level=logging.INFO)

def load_csv(csv_file):
    '''loads csv as list of dicts containing values and keys (specified by first val in column)'''
    with open(csv_file, 'r', newline='') as openedcsv:
        reader = csv.DictReader(openedcsv)
        dict_list = []
        for row in reader:
            dict_list.append(row)
        
        #print(dict_list)
        return dict_list

def write_csv(dict_list, csv_file):
    '''writes list of dicts to a csv'''
    with open(csv_file, 'w', newline='') as openedcsv:
        fieldnames = ['identifier', 'value']
        writer = csv.DictWriter(openedcsv, fieldnames=fieldnames)
        writer.writeheader()
        for item in dict_list:
            writer.writerow(item)

def map_hs_tag(old_tag, mapcsv):
    '''returns a list of hubspot internal property values to be updated'''
    #Get map values from .csv
    tag_map = load_csv(mapcsv)
    #print(tag_map)
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

def track_tier(HsId, old_tag):
    digit = old_tag[5]
    num = int(digit)
    identifier = str(HsId)
    switch = 'off'
    updatedtiers = load_csv(TIERCSV)#returns a list of dicts
    #print(updatedtiers)
    if len(updatedtiers) == 0:
        updatedtiers.append({'identifier': identifier, 'value': num})
        
    #search previously updated tier records to assign proper value
    for item in updatedtiers:
        if item['identifier'] == identifier:#if item exists
            switch = 'off'
            old_num = item['value']
            old_num = int(old_num)
            #check if current num vs old num is lower, if so update
            if num < old_num and num >= 1:
                #update the record with new value
                item['value'] = num
            else:
                num = old_num
            break
        else:#else add to list
            switch = 'on'

    if switch == 'on' and num >=1: 
        updatedtiers.append({'identifier': identifier, 'value': num})

    write_csv(updatedtiers, TIERCSV)
    digit = str(num)
    val = 'tier_' + digit
    return val

def make_prop(hsname):
    prop = {'name': hsname, 'value': 'true',}
    return prop

def make_tier_prop(hsname, tier):
    prop = {'name': hsname, 'value': tier,}
    return prop
 
def build_json(HsId, old_tag):
    '''Create json blob from record'''
    #Log some info
    print("HS ID: " + HsId)
    print("Old tag: " + old_tag)

    #map old tag to new 
    tags = map_hs_tag(old_tag, MAPCSV) #list of tag
    print(tags)


    #build json blob
    properties = {'properties': [],}
    for tag in tags:
        if tag == 'hs_ideal_customer_profile':
            try:
                val = track_tier(HsId, old_tag)
                prop = make_tier_prop(tag, val)
            except:
                print("Error tracking tier!!!")
                logging.info(f'Error tracking tier for {HsId} tag {old_tag}')
                prop = {}
        else:
            prop = make_prop(tag)
        properties['properties'].append(prop)
    payload = json.dumps(properties)
    
    print(payload)

    return payload
