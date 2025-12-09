
import logging
import sys
from tkinter import Tk, messagebox
import eel
import base64
import cv2
import numpy as np
from camera import VideoCamera

pause = 0
previous_pause = 0

label_cb = False
contour_cb = False
circle_cb = False
center_cb = False

# Set name of Video file to open. Leave name "" to open camera
#video_name = "./web/image/sky.mp4"
video_name = "./web/image/Assignment 1 Sample Videos/Sample Videos/brick1_01.mp4"
# video_name = ""


startBool= False

# Read Images
img = cv2.imread("./web/image/empty.png",cv2.IMREAD_ANYCOLOR)

# Setup the images to display in html file
@eel.expose
def setup():
  img_send_to_js(img, "video")
 
#  Your code depend on image processing
# This is a sample code to change 
# and send processed image to JavaScript  
@eel.expose
def video_feed():
  global x

  text_send_to_js("0", "green2x8")
  text_send_to_js("0", "grey2x8")
  text_send_to_js("0", "light_grey2x4")
  text_send_to_js("0", "lime2x2")
  text_send_to_js("0", "lime2x4")
  text_send_to_js("0", "medium_azure4x6")
  text_send_to_js("0", "medium_blue2x4")
  text_send_to_js("0", "orange2x2")
  text_send_to_js("0", "orange2x4")
  text_send_to_js("0", "yellow2x2")
  text_send_to_js("0", "yellow2x3")
  text_send_to_js("0", "yellow2x4")
  text_send_to_js("0", "total")

  option = eel.get_Option()()
  video_name = "./web/image/Assignment 1 Sample Videos/Sample Videos/" + str(option) + ".mp4"
  x = VideoCamera(video_name)
  process(x)


@eel.expose
def label():
  global label_cb
  if label_cb == False:
    label_cb = True
  else:
    label_cb = False

@eel.expose
def contour():
  global contour_cb
  if contour_cb == False:
    contour_cb = True
  else:
    contour_cb = False

@eel.expose
def circle():
  global circle_cb
  if circle_cb == False:
    circle_cb = True
  else:
    circle_cb = False

@eel.expose
def center():
  global center_cb
  if center_cb == False:
    center_cb = True
  else:
    center_cb = False


# Get Camera from video feed
# Add ur codes to process here
@eel.expose
def process(camera):
  global startBool, outmp4
  global pause, previous_pause
  previous_brick_mask = 0
  previous_detections = 0

  strFilename = "Ronith-SavedVideo.mp4"
  
  success, frame = camera.get_frame()
  if success == True:
    outmp4 = cv2.VideoWriter(strFilename, cv2.VideoWriter_fourcc(*'mp4v'), 24, (frame.shape[1], frame.shape[0]))

  while True:
    success, frame = camera.get_frame()
    
    if success == True:
      startBool = True
      text_send_to_js("Video started", "p1")
      if contour_cb == False and center_cb == False and label_cb == False and circle_cb == False:
        img_send_to_js(frame, "video")

      badge_update_dict={
        "lime2x2badge":"",
        "orange2x2badge":"",
        "yellow2x2badge":"",
        "yellow2x3badge":"", 
        "yellow2x4badge":"",
        "lime2x4badge":"",
        "light_grey2x4badge":"",
        "orange2x4badge":"",
        "medium_blue2x4badge":"",
        "green2x8badge":"",
        "grey2x8badge":"",
        "medium_azure4x6badge":""}

      # HSV Colour Thresholding
      imHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      low_grey = np.array([0, 0, 29])
      high_grey = np.array([179, 45, 74])
      grey_mask = cv2.inRange(imHSV, low_grey, high_grey)

      low_lime = np.array([26, 70, 76])
      high_lime = np.array([47, 209, 175])
      lime_mask = cv2.inRange(imHSV, low_lime, high_lime)

      low_green = np.array([39, 28, 50])
      high_green = np.array([70, 149, 117])
      green_mask = cv2.inRange(imHSV, low_green, high_green)

      low_medium_blue = np.array([106, 47, 85])
      high_medium_blue = np.array([117, 132, 161])
      medium_blue_mask = cv2.inRange(imHSV, low_medium_blue, high_medium_blue)

      low_orange = np.array([0, 114, 143])
      high_orange = np.array([16, 219, 205])
      orange_mask = cv2.inRange(imHSV, low_orange, high_orange)

      low_yellow = np.array([15, 93, 148])
      high_yellow = np.array([26, 212, 202])
      yellow_mask = cv2.inRange(imHSV, low_yellow, high_yellow)

      low_medium_azure = np.array([94, 50, 89])
      high_medium_azure = np.array([106, 182, 173])
      medium_azure_mask = cv2.inRange(imHSV, low_medium_azure, high_medium_azure)

      low_light_grey = np.array([0, 0, 50])
      high_light_grey = np.array([179, 40, 143])
      light_grey_mask = cv2.inRange(imHSV, low_light_grey, high_light_grey)
      # not good detection for light grey

      mask1 = cv2.bitwise_or(grey_mask, lime_mask)
      mask2 = cv2.bitwise_or(mask1, green_mask)
      mask3 = cv2.bitwise_or(mask2, medium_blue_mask)
      mask4 = cv2.bitwise_or(mask3, orange_mask)
      mask5 = cv2.bitwise_or(mask4, yellow_mask)
      mask6 = cv2.bitwise_or(mask5, medium_azure_mask)
      mask7 = cv2.bitwise_or(mask6, light_grey_mask)
      imMask = mask7

      # Contour Detection
      contours, hierarchy = cv2.findContours(imMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      detections = []
      all_bricks_mask = np.zeros(frame.shape[:-1], dtype='uint8')

      for i in range(len(contours)):
        area = cv2.contourArea(contours[i])

        if (area < 3000):
          continue

        rect = cv2.minAreaRect(contours[i])
        _, (width, height), _ = rect
        final_contour_area = width * height
        aspect_ratio = min(width, height) / max(width, height)

        box = cv2.boxPoints(rect)

        x_center = (box[0][0] + box[1][0] + box[2][0] + box[3][0]) / 4
        y_center = (box[0][1] + box[1][1] + box[2][1] + box[3][1]) / 4
        center = (x_center, y_center)

        box = np.int0(box)

        #contour_cb = eel.contour()()
        if contour_cb == True:
          cv2.drawContours(frame, [box], 0, (0,255,0), thickness=2)
        
        center = np.int0(center)

        #center_cb = eel.center()()
        if center_cb == True:
          cv2.circle(frame, center, 5, (0, 0, 0), -1)

        # Finding colour and type of bricks
        brick_mask = np.zeros(frame.shape[:-1], dtype='uint8')
        cv2.drawContours(brick_mask, [box], 0, 255, -1)
        cv2.drawContours(all_bricks_mask, [box], 0, 255, -1)

        grey_mask_overlap = cv2.bitwise_and(brick_mask, brick_mask, mask=grey_mask)
        lime_mask_overlap = cv2.bitwise_and(brick_mask, brick_mask, mask=lime_mask)
        green_mask_overlap = cv2.bitwise_and(brick_mask, brick_mask, mask=green_mask)
        medium_blue_mask_overlap = cv2.bitwise_and(brick_mask, brick_mask, mask=medium_blue_mask)
        orange_mask_overlap = cv2.bitwise_and(brick_mask, brick_mask, mask=orange_mask)
        yellow_mask_overlap = cv2.bitwise_and(brick_mask, brick_mask, mask=yellow_mask)
        medium_azure_mask_overlap = cv2.bitwise_and(brick_mask, brick_mask, mask=medium_azure_mask)
        light_grey_mask_overlap = cv2.bitwise_and(brick_mask, brick_mask, mask=light_grey_mask)

        overlaps = {np.sum(grey_mask_overlap):"grey", np.sum(lime_mask_overlap):"lime", np.sum(green_mask_overlap):"green", 
        np.sum(medium_blue_mask_overlap):"medium_blue", np.sum(orange_mask_overlap):"orange", np.sum(yellow_mask_overlap):"yellow", 
        np.sum(medium_azure_mask_overlap):"medium_azure", np.sum(light_grey_mask_overlap):"light_grey"}

        colour = overlaps.get(max(overlaps)) # finds the mask with which the lego has the largest area for thresholding

        if circle_cb == True:
          if colour == "grey":
            circleDetection(frame, grey_mask)
          if colour == "lime":
            circleDetection(frame, lime_mask)
          if colour == "green":
            circleDetection(frame, green_mask)
          if colour == "medium_blue":
            circleDetection(frame, medium_blue_mask)
          if colour == "orange":
            circleDetection(frame, orange_mask)
          if colour == "yellow":
            circleDetection(frame, yellow_mask)
          if colour == "medium_azure":
            circleDetection(frame, medium_azure_mask)
          if colour == "light_grey":
            circleDetection(frame, light_grey_mask)

        #print(colour)
        #print(final_contour_area)

        '''
        brick_type = "_x_" area        / aspect ratio / colours possible
        brick_type = "2x2" 3363-5500   / 0.83-1       / lime-orange-yellow
        brick_type = "2x3" 5018-7372   / 0.606-0.827  / yellow
        brick_type = "2x4" 6094-9783   / 0.444-0.628  / yellow-lime-light_grey-orange-medium_blue
        brick_type = "2x8" 12348-18540 / 0.248-0.312  / green-grey
        brick_type = "4x6" 19300-22859 / 0.665-0.71   / medium_azure

        only overlap: a yellow block with area 6094-7372 and aspect ratio 0.606-0.628 could be either brick types 2x3 or 2x4
        '''

        if colour == "medium_azure":
          brick_type = "4x6"
        elif (11000 < area < 19000) and (0.2 < aspect_ratio < 0.35):
          if colour == "green":
            brick_type = "2x8"
          else:
            colour = "grey"
            brick_type = "2x8"
        elif colour == "light_grey" or colour == "medium_blue":
          brick_type = "2x4"
        elif colour == "lime":
          if aspect_ratio > 0.73:
            brick_type = "2x2"
          else:
            brick_type = "2x4"
        elif colour == "orange":
          if aspect_ratio > 0.73:
            brick_type = "2x2"
          else:
            brick_type = "2x4"
        elif colour == "yellow":
          if aspect_ratio > 0.829 and 2500 < area < 5500:
            brick_type = "2x2"
          elif 0.6 < aspect_ratio < 0.829 and 4800 < area < 7380:
            brick_type = "2x3"
          elif 0.4 < aspect_ratio < 0.63 and 6090 < area < 10000:
            brick_type = "2x4"
          else:
            print("Unable to recognize yellow brick")
        else:
          print("Unable to recognize")

        brick_name = colour + brick_type

        if label_cb == True:
          cv2.putText(frame, brick_name, center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                      color=(255, 255, 255), thickness = 1, lineType=cv2.LINE_AA)

        detections.append(brick_name)
      
      if contour_cb == True or center_cb == True or label_cb == True or circle_cb == True:
        img_send_to_js(frame, "video")

      brick_mask_difference = cv2.bitwise_xor(brick_mask, previous_brick_mask)
      brick_mask_difference = np.sum(brick_mask_difference)

      if pause == previous_pause:
        if brick_mask_difference > 200000 or detections != previous_detections:
          #print(brick_mask_difference)
          print(detections)
          for detection in detections:
            addValue(detection)
            addValue("total")

            id = detection + "badge"
            badge_update_dict[id] = "new"
            for key, value in badge_update_dict.items():
              text_send_to_js(str(value), key)


      previous_brick_mask = brick_mask
      previous_detections = detections
      previous_pause = pause

      imDisplay = frame.copy()

      #Check if imDisplay is Grayscale. Convert to RGB if GrayScale                                                                                                                                                                      
      if(len(imDisplay.shape)<3):
       imDisplay = cv2.cvtColor(imDisplay, cv2.COLOR_GRAY2BGR) 
     
      # sText = "Your Name-Video Basic"
      # cv2.putText(imDisplay, sText, (20, 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255, 255, 255), thickness=1)
      # img_send_to_js(imDisplay,"video")
    
      #Write to File
      outmp4.write(imDisplay)
 

    else:
      if startBool == False:
       text_send_to_js("Error in Starting Video ", "p1")
      break


@eel.expose
def addValue(id):
  val=int(eel.get_Value(id)())
  val = val + 1
  text_send_to_js(str(val), id)

# Stop Video Caturing
# Do not touch
@eel.expose
def stop_video_feed():
  x.stop_capturing()
  text_send_to_js("Video paused", "p1")
  
# Restart Video Caturing
# Do not touch
@eel.expose
def restart_video_feed():
  x.restart_capturing()
  global pause
  pause += 1
  process(x)
  text_send_to_js("Video resumed", "p1")

@eel.expose
def save_video_feed():
  global outmp4
  outmp4.release()
  text_send_to_js("Video saved", "p1")

# Send text from python to Javascript 
# Do not touch
def text_send_to_js(val,id):
  eel.updateTextSrc(val,id)()

# Send image from python to Javascript 
# Do not touch
def img_send_to_js(img, id):
  if np.shape(img) == () :
    
    eel.updateImageSrc("", id)()
  else:
    ret, jpeg = cv2.imencode(".jpg",img)
    jpeg.tobytes()
    blob = base64.b64encode(jpeg) 
    blob = blob.decode("utf-8")
    eel.updateImageSrc(blob, id)()


@eel.expose
def circleDetection(frame, mask):
  imGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  imGray_blurred = cv2.blur(imGray, (3, 3))
  lego_mask = cv2.bitwise_and(imGray_blurred, imGray_blurred, mask=mask)
  circles_detected = cv2.HoughCircles(lego_mask, cv2.HOUGH_GRADIENT, 1, 15, param1 = 24, 
                                      param2 = 12, minRadius = 5, maxRadius = 10)

  if circles_detected is not None:
    detected_circles = np.round(circles_detected[0, :]).astype("int")

    for (x, y, r) in detected_circles:
      cv2.circle(frame, (x, y), r, (0, 255, 0), 3)


# Start function for app
# Do not touch
def start_app():
  try:
    start_html_page = 'index.html'
    eel.init('web')
    logging.info("App Started")

    eel.start('index.html', size=(1000, 800))

  except Exception as e:
    err_msg = 'Could not launch a local server'
    logging.error('{}\n{}'.format(err_msg, e.args))
    show_error(title='Failed to initialise server', msg=err_msg)
    logging.info('Closing App')
    sys.exit()

if __name__ == "__main__":
  x = VideoCamera(video_name)
  start_app()