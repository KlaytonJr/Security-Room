import os
import numpy as np
import cv2
import time

# CASCADES
fullbodyCascade = cv2.CascadeClassifier("Resources/haarcascade_fullbody.xml")
upperbodyCascade = cv2.CascadeClassifier("Resources/haarcascade_upperbody.xml")
frontalFaceCascade = cv2.CascadeClassifier(
    "Resources/haarcascade_frontalface_default.xml")

filename = "video.avi"
frames_per_seconds = 4.0
my_res = '480p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/016qmh


def change_res(cap, width, height):
	cap.set(3, width)
	cap.set(4, height)


# Standard Video Dimensions Sizes
STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

# grab resolution dimensions and set video capture to it.


def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
    # change the current caputre device
    # to the resulting resolution
    change_res(cap, width, height)
    return width, height


# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    # 'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'avi': cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
    # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    # 'mp4': cv2.VideoWriter_fourcc('M','J','P','G'),
}


def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


cap = cv2.VideoCapture(0)
dims = get_dims(cap, res=my_res)
video_type_cv2 = get_video_type(filename)

out = cv2.VideoWriter(filename, video_type_cv2,
                      frames_per_seconds, dims)  # Whidth, height

def detector (frame):
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bodys = fullbodyCascade.detectMultiScale(grayFrame, 1.1, 4)
    faces = frontalFaceCascade.detectMultiScale(grayFrame, 1.1, 4)
    uppers = upperbodyCascade.detectMultiScale(grayFrame, 1.1, 4)

    if faces != ():
        return True
    elif bodys != ():
        return True
    elif uppers != ():
        return True
    else:
        return False

time.sleep(5)
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if detector(frame):
        out.write(frame)

	# Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# python3 liveRecord.py
