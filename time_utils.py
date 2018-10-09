import calendar
from datetime import datetime


SYSTEM_GPS_OFFSET = 315964800
SECONDS_A_WEEK = 604800


def datetime_to_timestamp(d: datetime):
    return calendar.timegm(d.timetuple())


def second_of_gps_week(d: datetime):
    timestamp = calendar.timegm(d.utctimetuple())
    return (timestamp - SYSTEM_GPS_OFFSET) % SECONDS_A_WEEK


def gps_time_to_utc(gps_week, gps_tow):
    timestamp = SYSTEM_GPS_OFFSET + gps_week * SECONDS_A_WEEK + gps_tow
    return datetime.utcfromtimestamp(timestamp).replace(microsecond=0)
