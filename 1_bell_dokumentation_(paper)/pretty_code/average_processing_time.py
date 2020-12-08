# --TASK-- determines the average processing time of frame pair based on the datafile

# command line arguments:
#     <source_datafile_path>

import sys, json

# counters
duration = 0
number = 0

# load data
data_file = open(sys.argv[1], 'r')
data = json.loads(data_file.read())
data_file.close()

# iterate frames
for framecount, frame_data in data.items():
	duration += frame_data['processing_time']
	number += 1

# output
print('average processing time:', duration/number)
