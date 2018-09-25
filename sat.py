from pvt import *


aa = GpslikeEphData()
aa.sqrt_a = 1

XYZ.from_degree_llh()

sat_el_az(sat_pos, receiver_xyz)b