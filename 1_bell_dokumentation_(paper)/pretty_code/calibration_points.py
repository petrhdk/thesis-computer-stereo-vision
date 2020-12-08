# --TASK-- manages calibration point data

import numpy as np
from helper_functions import *

# calibration points
measured_calibration_points = [
	{'lat': 51.032952522, 'lon': 13.709240147, 'ele': 131+1.68, 'x_A': (903,428), 'x_B': (725,457)},
	{'lat': 51.032914426, 'lon': 13.709200348, 'ele': 131+1.68, 'x_A': (793,336), 'x_B': (689,346)},
	{'lat': 51.032875435, 'lon': 13.709159880, 'ele': 131+1.68, 'x_A': (711,262), 'x_B': (666,260)},
	{'lat': 51.032900885, 'lon': 13.708986442, 'ele': 131+1.51, 'x_A': (1158,174), 'x_B': (1202,186)},
	{'lat': 51.032900885, 'lon': 13.708986442, 'ele': 131+0.00, 'x_A': (1157,237), 'x_B': (1200,254)},
	{'lat': 51.032941878, 'lon': 13.709030178, 'ele': 131+1.51, 'x_A': (1282,226), 'x_B': (1300,250)},
	{'lat': 51.032941878, 'lon': 13.709030178, 'ele': 131+0.00, 'x_A': (1278,296), 'x_B': (1294,328)},
	{'lat': 51.032983504, 'lon': 13.709072909, 'ele': 131+1.51, 'x_A': (1443,294), 'x_B': (1429,338)},
	{'lat': 51.032983504, 'lon': 13.709072909, 'ele': 131+0.00, 'x_A': (1436,371), 'x_B': (1420,424)},
	{'lat': 51.033037829, 'lon': 13.709166331, 'ele': 131+0.00, 'x_A': (1689,583), 'x_B': (1584,700)},
	{'lat': 51.033019650, 'lon': 13.709327787, 'ele': 131+0.00, 'x_A': (1173,909), 'x_B': (748,1048)}
]

# randomly selected origin point
measured_origin = {'lat': 51.03302354862048, 'lon': 13.709257663085804, 'ele': 131+0.00}

# gives access to calibration points
def get_calibration_points():
	calibration_points = []
	Oa_spheric = (6371000+measured_origin['ele'], np.deg2rad(90-measured_origin['lat']), np.deg2rad(measured_origin['lon']))
	for mcp in measured_calibration_points:
		X_spheric = (6371000+mcp['ele'], np.deg2rad(90-mcp['lat']), np.deg2rad(mcp['lon']))
		OaX = global_to_local(X_spheric, Oa_spheric)
		calibration_points.append({
			'x_A': mcp['x_A'],
			'x_B': mcp['x_B'],
			'X': OaX
		})
	return calibration_points
