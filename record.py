from collections import namedtuple


SateInfo = namedtuple('SateInfo', ('constellation', 'svid', 'cn0', 'el', 'az'))


class Record:

    def __init__(self):
        self.lat = 0
        self.lng = 0
        self.alt = 0
        self.time = None
        self.server_time = None
        self.sat_infos = []
