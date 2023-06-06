from datetime import datetime, date

def combine_date_time(time_string):
    current_date = date.today()
    time_format = "%H:%M:%S"
    combined_datetime = datetime.combine(current_date, datetime.strptime(time_string, time_format).time())
    return combined_datetime
