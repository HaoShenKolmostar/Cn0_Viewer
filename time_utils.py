import calendar
from datetime import datetime


SYSTEM_GPS_OFFSET = 315964800
SECONDS_A_WEEK = 604800


def datetime_to_timestamp(d: datetime):
    return calendar.timegm(d.timetuple())


def second_of_gps_week(d: datetime):
    timestamp = calendar.timegm(d.utctimetuple())
    return (timestamp - SYSTEM_GPS_OFFSET) % SECONDS_A_WEEK
