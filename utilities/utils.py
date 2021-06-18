
def format_unix_datetime(date_str):
    ''' if date_str is not empty string, return unix milliseconds '''
    if date_str != '':
        unix_mil = calendar.timegm(
            (datetime.strptime(date_str[:-1], '%Y-%m-%dT%H:%M:%S.%f').timetuple())) * 1000  # convert to unix milliseconds
        return unix_mil
    else:
        return ''

def log_push_to_csv(push, rownum):
    '''Load csv to log uploaded record ids'''
    with open(records_uploaded, 'a', newline='') as csvfile:
        log_csv = csv.writer(csvfile)
        data = [rownum, push]
        log_csv.writerow(data)

