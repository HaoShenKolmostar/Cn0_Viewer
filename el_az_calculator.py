import json
from config import REFERENCE_POINT, EPH_SERVER_ADDRESS
from time_utils import datetime_to_timestamp
from pvt_utils import pick_eph, calculate_elaz, parse_eph_str


def download_kolmo_eph(start_time):
    start_stamp = datetime_to_timestamp(start_time)
    import requests
    hour_interval = 2
    url = '{}?satellites=GC&from={}&to={}'.format(
        EPH_SERVER_ADDRESS, start_stamp, start_stamp + 3600 * hour_interval
    )
    response = requests.get(url, verify=False)
    return json.loads(response.text)['content']


def get_elaz(self, record_time, constellation, svid):
    eph_time = record_time.replace(
        hour=record_time.hour//2*2, minute=0, second=0, microsecond=0)
    if eph_time not in self.eph_storage:
        eph_str = download_kolmo_eph(eph_time)
        self.eph_storage[eph_time] = parse_eph_str(eph_str)
    eph = pick_eph(self.eph_storage[eph_time], constellation, svid)
    return calculate_elaz(eph, record_time, REFERENCE_POINT)
