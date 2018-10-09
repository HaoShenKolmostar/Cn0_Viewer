import json
from config import REFERENCE_POINT, EPH_SERVER_ADDRESS
from time_utils import datetime_to_timestamp
from pvt_utils import pick_eph, calculate_elaz, parse_eph_str

EPH_STORAGE = {}


def download_kolmo_eph(start_time):
    start_stamp = datetime_to_timestamp(start_time)
    import requests
    hour_interval = 2
    url = '{}?satellites=GC&from={}&to={}'.format(
        EPH_SERVER_ADDRESS,
        start_stamp,
        start_stamp + 3600 * hour_interval + 300
    )
    response = requests.get(url, verify=False)
    return json.loads(response.text)['content']


def get_elaz(record_time, constellation, svid):
    eph_time = record_time.replace(
        hour=record_time.hour//2*2, minute=0, second=0, microsecond=0)
    if eph_time not in EPH_STORAGE:
        eph_str = download_kolmo_eph(eph_time)
        EPH_STORAGE[eph_time] = parse_eph_str(eph_str, eph_time)
    eph = pick_eph(EPH_STORAGE[eph_time], constellation, svid)
    return calculate_elaz(eph, record_time, REFERENCE_POINT)
