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

REFERENCE = LLH()
REFERENCE.lat = 39.98
REFERENCE.lon = 116.34
REFERENCE.height = 50


def _day_of_year(d: datetime):
    return d.timetuple().tm_yday


def _datetime_to_timestamp(d: datetime):
    return calendar.timegm(d.timetuple())


def _dgr_to_arc(dgr):
    return dgr / 180 * pi


def _arc_to_dgr(arc):
    return arc / pi * 180


def pick_eph(eph_storage, constellation, svid):
    if constellation == 'G':
        return eph_storage.get_gps_eph(int(svid))
    else:
        raise ValueError(
            'Constellation {} is not supported now.'.format(constellation))


def second_of_gps_week(d: datetime):
    timestamp = calendar.timegm(d.utctimetuple())
    return (timestamp - SYSTEM_GPS_OFFSET) % SECONDS_A_WEEK


SYSTEM_GPS_OFFSET = 315964800
SECONDS_A_WEEK = 604800


def calculate_elaz(eph, record_time, ref):
    second_of_week = second_of_gps_week(record_time)
    sat_pv_ek = calc_sat_pv_ek(eph, WeekSecond(second_of_week))
    ecef = XYZ.from_degree_llh(ref.lat, ref.lon, ref.height)
    el_az = ElAz()
    SatElAz(sat_pv_ek.pos, ecef, el_az)
    return _arc_to_dgr(el_az.el), _arc_to_dgr(el_az.az)


def download_kolmo_eph(start_stamp):
    import requests
    HOUR_INTERVAL = 2
    url = '{}?satellites=GC&from={}&to={}'.format(
        EPH_SERVER_ADDRESS, start_stamp, start_stamp + 3600 * HOUR_INTERVAL
    )
    response = requests.get(url, verify=False)
    return json.loads(response.text)['content']


class ElAzCalculator:

    def __init__(self, llh: LLH):
        self.sat_list = []
        self.eph_storage = {}
        self.reference = llh

    def set_reference_point(self, ref):
        self.reference = ref

    def calculate(self, record_time, constellation, svid, ref):
        eph_time = record_time.replace(
            hour=record_time.hour//2*2, minute=0, second=0, microsecond=0)
        if eph_time not in self.eph_storage:
            self.prepare_eph(eph_time)
        eph = pick_eph(self.eph_storage[eph_time], constellation, svid)
        return calculate_elaz(eph, record_time, ref)

    def prepare_eph(self, eph_time):
        eph_str = download_kolmo_eph(_datetime_to_timestamp(eph_time))
        # 'load_eph_from_string' will choose ephemeris whose seconde of week
        # is nearest with the given time. Since Kolmo's server only provide
        # the nearest ephemeris, there is no need to pass an accurate second
        # of week to the function.
        self.eph_storage[eph_time] = load_eph_from_string(
            eph_str, WeekSecond(second_of_gps_week(eph_time)))


# provider = ElAzProvider(None)
# provider.prepare_eph_by_time_list([datetime(2018, 9, 28, 4, 0, 0), ])

# day_of_year = 221
# second_of_week = 388800
# svid = 1
# given_lat = 39.98
# given_lon = 116.34
# given_height = 50


# gps_time = WeekSecond(second_of_week)
# eph_str = ''
# with open('/Users/sol/Documents/KolmoStar/GitHub/assistnow_ephemeris/check_tool/brdm/brdm%03d0.18p' % day_of_year, 'rt') as f:
#     eph_str = f.read()
# eph_storage = load_eph_from_string(eph_str, gps_time)

# for i in range(1, 33):
#     svid = i
#     gps_eph = eph_storage.get_gps_eph(svid)
#     sat_pv_ek = calc_sat_pv_ek(gps_eph, gps_time)
#     sat_pos = sat_pv_ek.pos
#     given_llh = LLH()
#     given_llh.lat, given_llh.lon, given_llh.height = _dgr_to_arc(
#         given_lat), _dgr_to_arc(given_lon), given_height
#     ecef = XYZ()
#     LlhToEcef(given_llh, ecef)
#     el_az = ElAz()
#     SatElAz(sat_pos, ecef, el_az)
#     print(_arc_to_dgr(el_az.el), _arc_to_dgr(el_az.az))
