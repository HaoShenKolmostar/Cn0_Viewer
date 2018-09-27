import calendar
from datetime import datetime


SYSTEM_GPS_OFFSET = 315964800
SECONDS_A_WEEK = 604800


def utc_to_gps_qzss_gal_week(utc_datetime):
    timestamp = calendar.timegm(utc_datetime.utctimetuple())
    return (timestamp - SYSTEM_GPS_OFFSET) // SECONDS_A_WEEK


def gps_time_to_utc(gps_week, gps_tow):
    timestamp = SYSTEM_GPS_OFFSET + gps_week * SECONDS_A_WEEK + gps_tow
    return datetime.utcfromtimestamp(timestamp).replace(microsecond=0)
