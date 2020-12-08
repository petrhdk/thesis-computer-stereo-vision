# --TASK-- defines functions that may be used across all scripts

import cv2, numpy as np
from functools import lru_cache

# --- Coordinate Type Conversion ----------
def to_homogeneous(x):
    return np.append(x, [1])

def to_euclidian(x):
    return np.array([x[i]/x[-1] for i in range(len(x)-1)])

def spherical_to_euclidian(X_spheric):
    r, theta, phi = X_spheric
    return np.array([
        r * np.sin(theta) * np.cos(phi),
        r * np.sin(theta) * np.sin(phi),
        r * np.cos(theta)
    ])

def euclidian_to_spherical(X):
    r = np.linalg.norm(X)
    theta = np.arccos(X[2]/r)
    phi = np.arctan(X[1]/X[0])
    return r, theta, phi


# --- Coordinate System Conversion ----------
@lru_cache()
def get_L(theta, phi):
    return np.array([
        [-np.sin(phi),   -np.cos(phi)*np.cos(theta),   np.cos(phi)*np.sin(theta) ],
        [ np.cos(phi),   -np.sin(phi)*np.cos(theta),   np.sin(phi)*np.sin(theta) ],
        [ 0,              np.sin(theta),               np.cos(theta)             ]
    ])

def local_to_global(OaX, Oa_spheric):
    ObOa_ = spherical_to_euclidian(Oa_spheric)
    L = get_L(Oa_spheric[1], Oa_spheric[2])
    ObX_ = np.dot(L, OaX) + ObOa_
    return euclidian_to_spherical(ObX_)
def global_to_local(X_spheric, Oa_spheric):
    ObX_ = spherical_to_euclidian(X_spheric)
    ObOa_ = spherical_to_euclidian(Oa_spheric)
    L = get_L(Oa_spheric[1], Oa_spheric[2])
    OaX = np.dot(L.T, ObX_ - ObOa_)
    return OaX


# --- Object Detection ----------
def detection_coordinates(detection, image):
	image_height, image_width = image.shape[:2]
	startX = int(detection['startX_percentage']*image_width)
	startY = int(detection['startY_percentage']*image_height)
	endX = int(detection['endX_percentage']*image_width)
	endY = int(detection['endY_percentage']*image_height)
	return startX, startY, endX, endY

def center_point(detection, image):
	startX, startY, endX, endY = detection_coordinates(detection, image)
	return (startX+endX)/2, (startY+endY)/2

def draw_detections(image, detections):
	for detection in detections:
		label = '{}: {}%'.format(detection['object_class'], int(detection['confidence']*100))
		startX, startY, endX, endY = detection_coordinates(detection, image)
		cv2.rectangle(image, (startX, startY), (endX, endY), color=(255,0,0), thickness=2)
		cv2.putText(image, label, (startX, startY-10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color=(255,0,0), thickness=2)
	return image


# --- Ray Geometry ----------
def ray_endpoint(X0, KI, RT, x, length=1):
	return X0 + vector_to_length(-double_dot( RT , KI , to_homogeneous(x) ), length)

def triangulate(X0_A, X0_B, a, b):
	la, mu = np.linalg.solve(np.array([
		[np.dot(a,a), -np.dot(a,b)],
		[np.dot(a,b), -np.dot(b,b)]
	]), np.array([
		np.dot(X0_B-X0_A, a),
		np.dot(X0_B-X0_A, b)
	]))
	return 0.5*(X0_A + la*a + X0_B + mu*b)

def intersection_angle(X0_A, X0_B, a, b):
	alpha = np.arcsin(
		np.dot( np.cross( a , X0_B-X0_A) , b )
		/ np.linalg.norm( np.cross( a , X0_B-X0_A) )
		/ np.linalg.norm( b )
	)
	return abs(alpha)


# --- Linear Algebra ----------
def double_dot(a,b,c):
	return np.dot(a,np.dot(b,c))

def vector_to_length(vector, length):
	return vector / np.linalg.norm(vector) * length


# --- Array Functions ----------
def list_filter(the_list, filter_function):
	return [ item for item in the_list if filter_function(item) ]