import json
import calendar
from datetime import datetime
from math import pi
from pvt import (
    WeekSecond,
    LLH,
    XYZ,
    ElAz,
    SatElAz,
    LlhToEcef,
    calc_sat_pv_ek,
    load_eph_from_string
)


def _day_of_year(d: datetime):
    return d.timetuple().tm_yday


def _datetime_to_timestamp(d: datetime):
    return calendar.timegm(d.timetuple())


def download_kolmo_eph(start_stamp):
    import requests
    HOUR_INTERVAL = 2
    url = '{}?satellites=GC&from={}&to={}'.format(
        EPH_SERVER_ADDRESS, start_stamp, start_stamp + 3600 * HOUR_INTERVAL
    )
    print(url)
    response = requests.get(url, verify=False)
    return json.loads(response.text)['content']


class ElAzCalculator:

    def __init__(self, llh: LLH):
        self.sat_list = []
        self.eph_storage = {}
        self.reference = llh

    def set_reference_point(self, ref):
        self.reference = ref

    def work(self, record_time, constellation, svid):
        eph_time = record_time.replace(
            hour=record_time.hour//2*2, minute=0, second=0, microsecond=0)
        if eph_time not in self.eph_storage:
            self.prepare_eph(eph_time)
        eph = self.eph_storage[eph_time]

    def prepare_eph(self, eph_time):
        eph_str = download_kolmo_eph(_datetime_to_timestamp(eph_time))
        # 'load_eph_from_string' will choose ephemeris whose seconde of week
        # is nearest with the given time. Since Kolmo's server only provide
        # the nearest ephemeris, there is no need to pass an accurate second
        # of week to the function.
        self.eph_storage[eph_time] = load_eph_from_string(eph_str, 0)

