import os
import cv2
import time
import requests

SERVER = ""
video = cv2.VideoCapture(0)
static_frame = None
counter = 0

while True:
  __, frame = video.read()

  motion = False
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (13, 13), 0)

  if static_frame is None:
    static_frame = gray

  diff_frame = cv2.absdiff(static_frame, gray)
  thres_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
  thres_frame = cv2.dilate(thres_frame, None, iterations=2)

  # Finding contour of moving object
  cnts,_ = cv2.findContours(thres_frame.copy(), 
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
  for cnt in cnts:
    if cv2.contourArea(cnt) < 10000:
      (x, y, w, h) = cv2.boundingRect(cnt)
      # making green rectangle around the moving object
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
      motion = True
      break

  # Displaying image in gray_scale
  # cv2.imshow("Gray Frame", gray)

  # Displaying the difference in currentframe to
  # the staticframe(very first_frame)
  # cv2.imshow("Difference Frame", diff_frame)

  # Displaying the black and white image in which if
  # intensity difference greater than 30 it will appear white
  cv2.imshow("Threshold Frame", thres_frame)

  # Displaying color frame with contour of motion of object
  # cv2.imshow("Color Frame", frame)

  key = cv2.waitKey(1)
  # if q entered whole process will stop
  if key == ord('q'):
    # if something is movingthen it append the end time of movement
    break
  if motion:
    file_name = "{}.png".format(time.time())
    cv2.imwrite(file_name, frame)
    # with open(file_name, "rb") as fin:
    #   resp = requests.post(SERVER + "/analyze", files={
    #     "image" : fin.read()
    #   })
    #   print(resp.status_code)
    os.remove(file_name)
  if counter == 3:
    counter = 0
    static_frame = gray 

  counter += 1