from datetime import datetime

def check_access(user,name):
    access = user.user_access.all()
    if access:
        if getattr(access[0],name):
            return True
    return False


def convert_to_datetime_with_current_time(date_string):
    # Assuming the input date format is 'YYYY-MM-DD'
    date_format = "%Y-%m-%d"

    # Convert the string to a datetime object (just for the date)
    date_part = datetime.strptime(date_string, date_format).date()

    # Get the current time
    now_time = datetime.now().time()

    # Combine the date with the current time
    return datetime.combine(date_part, now_time)


