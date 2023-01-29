def days_in_month(year, month):
    """Return the days in a given month for this year"""
    days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0: days[2] = 29
    return days[month]

def day_of_year(year, month, day):
    """Count the days this year to the given date"""
    total = 0
    cur = 1
    while cur < month:
        total += days_in_month(year, month)
        cur += 1
    total += day

def week_number(year, month, day):
    """Calculate the ISO Week for a given date"""
    doy = day_of_year(year, month, day)
    # count thursdays...

def month_key(year, month):
    """An offset for calculating the day of the week"""
    if month > 2:
        return [0, 0, 0, 4, 0, 2, 5, 0, 3, 6, 1, 4, 6][month]
    elif year % 4 == 0:
        return [0, 0, 3][month]
    else:
        return [0, 1, 4][month]

def day_of_week(year, month, day):
    """
    Calculate the day of the week, assumes 2000 <= year <= 2099, and returns
    with zero as Monday.
    """
    return (year % 100 + int(year % 100 / 4) + day + month_key(year, month) - 1 + 5) % 7

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
def day_str(day_of_week):
    """Strings for day of week"""
    return DAYS[day_of_week]

MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
def month_str(month):
    """Strings for month (long)"""
    return MONTHS[month - 1]

MONS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
def mon_str(mon):
    """Strings for month (short)"""
    return MONS[mon - 1]
