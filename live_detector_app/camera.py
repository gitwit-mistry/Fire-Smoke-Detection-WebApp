from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model,model_from_json
from tensorflow.keras.preprocessing import image
import json
import config
from imutils.video import VideoStream
import imutils
import cv2,os,urllib.request
import numpy as np
from django.conf import settings

json_file = open('models/model_mobilenet.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights('models/weights_mobilenet.h5')


class VideoCamera(object):
	def __init__(self):
		 self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)

	def __del__(self):
		self.video.release()

	def get_frame(self):

		success, image = self.video.read()
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()


class IPWebCam(object):
	def __init__(self):
		self.url = "http://192.168.0.100:8080/shot.jpg"

	def __del__(self):
		cv2.destroyAllWindows()

	def get_frame(self):
		imgResp = urllib.request.urlopen(self.url)
		imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
		img= cv2.imdecode(imgNp,-1)
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces_detected = face_detection_webcam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(img, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		resize = cv2.resize(img, (640, 480), interpolation = cv2.INTER_LINEAR) 
		frame_flip = cv2.flip(resize,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()


class MaskDetect(object):
	def __init__(self):
		self.vs = VideoStream(src=0 + cv2.CAP_DSHOW,).start()

	def __del__(self):
		cv2.destroyAllWindows()

	def get_frame(self):
		frame = self.vs.read()
		frame = imutils.resize(frame, width=650)
		frame = cv2.flip(frame, 1)

		imagesd = cv2.resize(frame ,(128,128))
		images = np.asarray(imagesd , 'float32')
		imagess = np.expand_dims(images , axis = 0)
		my_pred = model.predict(imagess)[0].argmax()

		if my_pred == 0:
			text = 'FIRE'
		elif my_pred == 1:
			text = 'Neutral'
		else:
			text = 'Smoke'

		cv2.putText(frame, text, (150, 150),
					cv2.FONT_HERSHEY_SIMPLEX, 3, (0,255,0), 3)


		ret, jpeg = cv2.imencode('.jpg', frame)
		return jpeg.tobytes()
		
class LiveWebCam(object):
	def __init__(self):
		self.url = cv2.VideoCapture("rtsp://admin:Mumbai@123@203.192.228.175:554/")

	def __del__(self):
		cv2.destroyAllWindows()

	def get_frame(self):
		success,imgNp = self.url.read()
		resize = cv2.resize(imgNp, (640, 480), interpolation = cv2.INTER_LINEAR) 
		ret, jpeg = cv2.imencode('.jpg', resize)
		return jpeg.tobytes()
