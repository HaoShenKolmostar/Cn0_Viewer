from math import pi
from pvt import (
    WeekSecond,
    XYZ,
    ElAz,
    SatElAz,
    calc_sat_pv_ek,
    load_eph_from_string
)
from time_utils import datetime_to_timestamp, second_of_gps_week


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


def calculate_elaz(eph, record_time, ref):
    second_of_week = second_of_gps_week(record_time)
    sat_pv_ek = calc_sat_pv_ek(eph, WeekSecond(second_of_week))
    ecef = XYZ.from_degree_llh(ref.lat, ref.lon, ref.height)
    el_az = ElAz()
    SatElAz(sat_pv_ek.pos, ecef, el_az)
    return _arc_to_dgr(el_az.el), _arc_to_dgr(el_az.az)


def parse_eph_str(eph_str, ref_time):
    time_stamp = datetime_to_timestamp(ref_time)
    return load_eph_from_string(eph_str,
                                WeekSecond(second_of_gps_week(time_stamp)))
