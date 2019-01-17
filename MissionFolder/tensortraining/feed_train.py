import cv2
import urllib 
import numpy as np


stream=urllib.urlopen('http://192.168.0.65:8081/mjpg/video.mjpg')
bytes=''

i = 0
base_name = 'training'

while True:
	image_data = 0
	while True:
		bytes+=stream.read(1024)
		a = bytes.find('\xff\xd8')
		b = bytes.find('\xff\xd9')
		if a!=-1 and b!=-1:
			jpg = bytes[a:b+2]
			bytes= bytes[b+2:]
			image_data = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
			break

	image_data = cv2.resize(image_data, dsize=(299,299), interpolation = cv2.INTER_CUBIC)
	image_data = np.asarray(image_data)
	image_data = cv2.normalize(image_data.astype('float'), None, -0.5, 0.5, cv2.NORM_MINMAX)
	image_data = np.expand_dims(image_data, axis=0)

	with file(base_name.join(str(i).join('.jpg')), 'wb') as f:
		f.write(image_data)
	i=i+1
