import cv2
import mediapipe as mp
import math
import time

def head_tilt(left_eye, right_eye, threshold=20):
	delta_y = right_eye[1] - left_eye[1]
	delta_x = right_eye[0] - left_eye[0]
	tilt = math.degrees(math.atan2(delta_y, delta_x))

	if tilt < -threshold:
		return "Left"
	elif tilt > threshold:
		return "Right"
	else:
		return "Center"

def head_dir(left_eye, right_eye, nose, threshold=20):
	nose_position = nose[0] - (left_eye[0] + right_eye[0]) // 2

	if nose_position < -threshold:
		return "Left"
	elif nose_position > threshold:
		return "Right"
	else:
		return "Center"

def mouth_open(left_eye, right_eye, upper_lip, lower_lip, threshold=0.30):
	return (lower_lip[1] - upper_lip[1]) / (right_eye[0] - left_eye[0]) > threshold

def eyebrow_raise(left_eyebrow, right_eyebrow, left_eye, right_eye, threshold=0.25):
	return (right_eye[1] - right_eyebrow[1]) / (right_eye[0] - left_eye[0]) > threshold

def left_wink(uleft_eyelid, bleft_eyelid, left_eye, right_eye, threshold=0.08):
	return (bleft_eyelid[1] - uleft_eyelid[1]) / (right_eye[0] - left_eye[0]) < threshold

face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
webcam = cv2.VideoCapture(0)
# webcam = cv2.VideoCapture("Gestures 02.mp4")


while webcam.isOpened():
	success, frame = webcam.read()
	# frame = cv2.flip(frame, 1)

	if not success:
		print("Empty camera frame.")
		break

	h, w, _ = frame.shape
	frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	results = face_mesh.process(frame_rgb)

	if results.multi_face_landmarks:
		for face_landmarks in results.multi_face_landmarks:
			landmarks = {
				"left_eyebrow": 66,
				"right_eyebrow": 296,
				"left_eye": 33,
				"right_eye": 263,
				"uleft_eyelid": 160,
				"bleft_eyelid": 144,
				"nose": 1,
				"upper_lip": 0,
				"lower_lip": 16,
			}
			landmarks_norm = dict()
			points = dict()

			for parts in landmarks:
				landmarks_norm[parts] = face_landmarks.landmark[landmarks[parts]]
				x = int(landmarks_norm[parts].x * w)
				y = int(landmarks_norm[parts].y * h)
				points[parts] = (x, y)

				cv2.circle(frame, points[parts], 3, (160, 255, 0), -1)

			tilt = head_tilt(points["left_eye"], points["right_eye"])
			dir = head_dir(points["left_eye"], points["right_eye"], points["nose"])
			open = mouth_open(points["left_eye"], points["right_eye"],
				points["upper_lip"], points["lower_lip"])
			raise_ = eyebrow_raise(points["left_eyebrow"], points["right_eyebrow"],
				points["left_eye"], points["right_eye"])
			wink = left_wink(points["uleft_eyelid"], points["bleft_eyelid"],
				points["left_eye"], points["right_eye"])

			cv2.rectangle(frame, (10, 10), (210, 120), (30, 30, 30), cv2.FILLED)
			cv2.putText(frame, f"Head Tilt: {tilt}", (20, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 255, 0), 2)
			cv2.putText(frame, f"Head Direction: {dir}", (20, 50),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 255, 0), 2)
			cv2.putText(frame, f"Mouth Open: {open}", (20, 70),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 255, 0), 2)
			cv2.putText(frame, f"Eyebrow Raise: {raise_}", (20, 90),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 255, 0), 2)
			cv2.putText(frame, f"Left Wink: {wink}", (20, 110),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 255, 0), 2)

	cv2.imshow("Real-time Expression Detector", frame)
	time.sleep(1/30)

	# Escape key to end
	if cv2.waitKey(1) & 0xFF == 27:
		break

webcam.release()
cv2.destroyAllWindows()