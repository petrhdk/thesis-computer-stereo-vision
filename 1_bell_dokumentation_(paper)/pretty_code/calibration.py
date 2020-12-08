# --TASK-- carries out the calibration procedure

import numpy as np
from calibration_points import get_calibration_points
from helper_functions import *

# gives access to calibration data
def get_calibration():
	
	# load calibration points
	calibration_points = get_calibration_points()

	# create empty M matrices
	M_A = M_B = np.empty((0,12))

	# fill M matrices
	for cp in calibration_points:
		# camera A
		line = np.concatenate([ -to_homogeneous(cp['X']), [0,0,0,0], cp['x_A'][0]*to_homogeneous(cp['X']) ])
		M_A = np.append(M_A, [line], axis=0)
		line = np.concatenate([ [0,0,0,0], -to_homogeneous(cp['X']), cp['x_A'][1]*to_homogeneous(cp['X']) ])
		M_A = np.append(M_A, [line], axis=0)

		# camera B
		line = np.concatenate([ -to_homogeneous(cp['X']), [0,0,0,0], cp['x_B'][0]*to_homogeneous(cp['X']) ])
		M_B = np.append(M_B, [line], axis=0)
		line = np.concatenate([ [0,0,0,0], -to_homogeneous(cp['X']), cp['x_B'][1]*to_homogeneous(cp['X']) ])
		M_B = np.append(M_B, [line], axis=0)

	# singular value decomposition
	U_A, s_A, VT_A = np.linalg.svd(M_A, full_matrices=False)
	U_B, s_B, VT_B = np.linalg.svd(M_B, full_matrices=False)

	# assemble P matrices
	P_A = np.reshape(VT_A[-1], (3,4))
	P_B = np.reshape(VT_B[-1], (3,4))

	# decompose P matrices
	X0_A = np.reshape( np.dot( np.linalg.inv(-P_A[:,:3]) , P_A[:,3:] ), 3)
	X0_B = np.reshape( np.dot( np.linalg.inv(-P_B[:,:3]) , P_B[:,3:] ), 3)
	RT_A, KI_A = np.linalg.qr(np.linalg.inv(P_A[:,:3]))
	RT_B, KI_B = np.linalg.qr(np.linalg.inv(P_B[:,:3]))

	return {
		'X0_A': X0_A,
		'RT_A': RT_A,
		'KI_A': KI_A,

		'X0_B': X0_B,
		'RT_B': RT_B,
		'KI_B': KI_B
	}
