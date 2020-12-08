# --TASK-- applies object detection
# --TASK-- matches detections
# --TASK-- locates objects by triangulation

# command line arguments:
#     <source_video_A_path>
#     <source_video_B_path>
#     <target_video_A_path>
#     <target_video_B_path>
#     <target_datafile_path>


import sys, time, json, cv2, numpy as np
from calibration import get_calibration
from helper_functions import *

# load recorded videos
vcap_A = cv2.VideoCapture(sys.argv[1])
vcap_B = cv2.VideoCapture(sys.argv[2])

# open video write stream for detection output
vwriter_A = cv2.VideoWriter(sys.argv[3], cv2.VideoWriter_fourcc(*'mp4v'), 30.0, (960,540))
vwriter_B = cv2.VideoWriter(sys.argv[4], cv2.VideoWriter_fourcc(*'mp4v'), 30.0, (960,540))

# load MobileNetSSD object detection algorithm
mobile_net_ssd = cv2.dnn.readNetFromCaffe('MobileNetSSD.prototxt.txt', 'MobileNetSSD.caffemodel')
object_classes = ('background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor')
object_classes_wanted = {'bicycle','cat','cow','dog','horse','person','sheep'}

# global data storage (saved to file at the end)
data = {
	# <frame_number>: {objects: [{object_class, X, intersection_angle}, ..], unpaired_detections, processing_time}
	# ..
}

# iterate video frames
frame_count = 0
frame_count_end = int(vcap_A.get(cv2.CAP_PROP_FRAME_COUNT))
while vcap_A.isOpened() and vcap_B.isOpened() and frame_count<frame_count_end:
	
	# start time measure
	timestamp_start = time.time()
	
	# read next frame
	vcap_A.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
	vcap_B.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
	_, frame_A = vcap_A.read()
	_, frame_B = vcap_B.read()

	# apply MobileNetSSD object detection
	blob_A = cv2.dnn.blobFromImage(frame_A, 0.007843, (1920, 1080), 127.5)
	mobile_net_ssd.setInput(blob_A)
	detections_A = mobile_net_ssd.forward()
	detections_A = [ {
		'object_class': object_classes[int(detection[1])],
		'confidence': detection[2],
		'startX_percentage': detection[3],
		'startY_percentage': detection[4],
		'endX_percentage': detection[5],
		'endY_percentage': detection[6]
	} for detection in detections_A[0][0] ]
	detections_A = list_filter(detections_A, lambda detection: detection['confidence']>0.65 and detection['object_class'] in object_classes_wanted)
	
	blob_B = cv2.dnn.blobFromImage(frame_B, 0.007843, (1920, 1080), 127.5)
	mobile_net_ssd.setInput(blob_B)
	detections_B = mobile_net_ssd.forward()
	detections_B = [ {
		'object_class': object_classes[int(detection[1])],
		'confidence': detection[2],
		'startX_percentage': detection[3],
		'startY_percentage': detection[4],
		'endX_percentage': detection[5],
		'endY_percentage': detection[6]
	} for detection in detections_B[0][0] ]
	detections_B = list_filter(detections_B, lambda detection: detection['confidence']>0.65 and detection['object_class'] in object_classes_wanted)
	
	# show detections, write to file stream
	cv2.imshow('frame A', cv2.resize(draw_detections(frame_A, detections_A), (480,270)))
	cv2.imshow('frame B', cv2.resize(draw_detections(frame_B, detections_B), (480,270)))
	vwriter_A.write(cv2.resize(draw_detections(frame_A, detections_A), (960,540)))
	vwriter_B.write(cv2.resize(draw_detections(frame_B, detections_B), (960,540)))

	# load calibration
	calibration = get_calibration()
	locals().update(calibration)

	# add ray directions to the detections
	for detection_A in detections_A:
		detection_A['a'] = np.reshape(double_dot( RT_A, KI_A , to_homogeneous(center_point(detection_A,frame_A)) ),3)
	for detection_B in detections_B:
		detection_B['b'] = np.reshape(double_dot( RT_B, KI_B , to_homogeneous(center_point(detection_B,frame_B)) ),3)

	# correspondence matching (by image class and coplanarity check (gives intersection angle alpha))
	# and triangulation
	data[frame_count] = {"objects": [], "unpaired_detections": 0}
	for detection_A in detections_A:
		detections_B_copy = detections_B[:]
		detections_B_copy = list_filter(detections_B_copy, lambda detection_B: detection_B['object_class']==detection_A['object_class'])
		for detection_B in detections_B_copy:
			detection_B['intersection_angle'] = intersection_angle(X0_A, X0_B, detection_A['a'], detection_B['b'])
		detections_B_copy = list_filter(detections_B_copy, lambda detection_B: np.rad2deg(detection_B['intersection_angle']) < 1.0)
		if len(detections_B_copy) == 0:
			data[frame_count]['unpaired_detections'] += 1
		else:
			detections_B_copy.sort(key = lambda detection_B: detection_B['intersection_angle'])
			detection_B = detections_B_copy[0]
			X = triangulate(X0_A, X0_B, detection_A['a'], detection_B['b'])
			data[frame_count]['objects'].append({"object_class": detection_A['object_class'], "X": tuple(X), "intersection_angle": detection_B['intersection_angle']})
			detections_B.remove(detection_B)
	data[frame_count]['unpaired_detections'] += len(detections_B)

	# end time measure
	timestamp_end = time.time()
	data[frame_count]['processing_time'] = timestamp_end-timestamp_start

	# log
	print("done frame "+str(frame_count))

	# next frame
	frame_count += 1
	cv2.waitKey(1)


# write data to json file
data_file = open(sys.argv[5], 'w+')
data_file.write(json.dumps(data, indent=4))
data_file.close()

# clean up
vcap_A.release()
vcap_B.release()
vwriter_A.release()
vwriter_B.release()
cv2.destroyAllWindows()
