from collections import namedtuple


LlhPoint = namedtuple('LlhPoint', ('lat', 'lon', 'height'))
REFERENCE_POINT = LlhPoint(
    lat=39.98,
    lon=116.34,
    height=50
)

