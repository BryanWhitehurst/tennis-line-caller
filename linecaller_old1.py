import numpy as np
import cv2
#poster: write down important details ex. calibration image


def binary_search(arr, low, high, miny, lowestFrame, ballSeen, numPasses): 
    # Check base case 
    if(numPasses == 2):
      return lowestFrame

    if high >= low: 
        mid = (high + low) // 2
        arr[mid] = arr[mid][0 + int((arr[mid].shape[0] * .25)): arr[mid].shape[0], 0:arr[mid].shape[1]]
        opening_ball, contours_ball = getMask(arr[mid], np.array([25, 75, 85]), np.array([50, 220,255]))

        if(ballSeen and len(contours_ball) == 0): return binary_search(arr, low, mid-1, miny, lowestFrame, ballSeen, numPasses)
        #elif(not(ballSeen) and len(contours_ball) == 0): return binary_search(arr, mid+1, high, miny, lowestFrame, ballSeen, numPasses)
        
        
        while len(contours_ball) == 0:
          mid = mid + 1
          arr[mid] = arr[mid][0 + int((arr[mid].shape[0] * .25)): arr[mid].shape[0], 0:arr[mid].shape[1]]
          opening_ball, contours_ball, = getMask(arr[mid], np.array([25, 75, 85]), np.array([50, 220,255]))
          #if(len(contours_ball) != 0): cv2.imwrite("middle.jpg", arr[mid])
        

        ballSeen = True
        #get lowest pixel in ball contour
        lowest = contours_ball[0][0]
        for i in contours_ball[0]:
            if(i[0][1] > lowest[0][1]):
                lowest = i
        
        
        lowest1 = lowest[0][1]

        arr[mid + 5] = arr[mid + 5][0 + int((arr[mid + 5].shape[0] * .25)): arr[mid + 5].shape[0], 0:arr[mid + 5].shape[1]]
        opening_ball, contours_ball = getMask(arr[mid + 5], np.array([25, 75, 85]), np.array([50, 220,255]))

        #5 pixels ahead, the ball isnt present anymo
        lowest = contours_ball[0][0]
        for i in contours_ball[0]:
            if(i[0][1] > lowest[0][1]):
                lowest = i
        
        
        lowest2 = lowest[0][1]

        if lowest1 < lowest2 and lowest1 < miny: 
            return binary_search(arr, low, mid - 1, miny, lowestFrame, ballSeen, numPasses + 1) 

        elif lowest1 < lowest2 and lowest1 > miny: 
            return binary_search(arr, mid + 1, high, lowest1, arr[mid],ballSeen, 0) 
        
        elif lowest1 > lowest2 and lowest1 > miny: 
            return binary_search(arr, low, mid - 1, lowest1, arr[mid], ballSeen, 0) 
        
        elif lowest1 > lowest2 and lowest1 < miny: 
            return binary_search(arr, low, mid - 1,  miny, lowestFrame, ballSeen, numPasses + 1) 
        
    else: 
        return lowestFrame

def getMask(img, lower, upper):
  img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  img_mask = cv2.inRange(img_hsv, lower, upper)
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
  opening = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel, iterations=3)

  contours, hierarchy = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

  return [opening, contours]


def inOrOut(line, ball):
  #crop the top 25% of the image out
  line = line[0 + int((line.shape[0] * .25)): line.shape[0], 0:line.shape[1]]


  #receive line contours
  opening_line, contours_line,  = getMask(line, np.array([0,0,255 - 30]), np.array([255,30,255]))
  opening_ball, contours_ball,  = getMask(ball, np.array([25, 75, 85]), np.array([50, 220,255]))


  #takes an arbitrary pixel from the ball and an arbitrary pixel from the line
  ball_in = True
  if(contours_ball[0][0][0][0] < contours_line[0][0][0][0]): ball_in = False

  overlap = cv2.bitwise_and(opening_ball, opening_line)

  numPixels = cv2.countNonZero(overlap)
  numPixelsInBall = cv2.countNonZero(opening_ball)

  #code to find x coordinate of bottom most point of ball contour
  lowest = contours_ball[0][0]
  for i in contours_ball[0]:
    if(i[0][1] > lowest[0][1]):
      lowest = i

  lowest_ballx = lowest[0][0]
  lowest_bally = lowest[0][1]
  leftmost = contours_line[0][0][0][0]
  for i in contours_line[0]:
    if((i[0][0] < leftmost) and (i[0][0] < (lowest_ballx + 10) and i[0][0] > (lowest_ballx - 10)) and (i[0][1] < (lowest_bally + 10) and i[0][1] > (lowest_bally - 10))):
      leftmost = i[0][0]

  #  5 pixel uncertainty
  if(numPixels != 0 and leftmost < lowest_ballx + 5):
    ball_in = False
    print("ball is in")
  else:
    if(not(ball_in)): 
      print("Ball is out")
    else: 
      print("Ball is in")

  #write in or out on the image
  cv2.imwrite("result.jpg", ball)
  contour_img = cv2.imread("result.jpg")
  contour_img = cv2.drawContours(contour_img, contours_line, 0, (0,255,0), 1)
  contour_img = cv2.drawContours(contour_img, contours_ball, -1, (0,255,0), 1)
  font = cv2.FONT_HERSHEY_SIMPLEX
  if(ball_in): cv2.putText(contour_img, 'IN', (10, contour_img.shape[1]//2), font, 10, (0, 0, 255), 8, cv2.LINE_AA)
  else: cv2.putText(contour_img, 'OUT', (10, contour_img.shape[1]//2), font, 10, (0, 0, 255), 8, cv2.LINE_AA)
  cv2.imwrite("result.jpg", contour_img)


#driving code
#read the frames of the video into an array
cap = cv2.VideoCapture('vid.mp4') 
ret, first = cap.read()
frames = []
while (cap.isOpened()): 
  ret, frame = cap.read()
  frames.append(frame)
  if(not(ret)): break

#binary search to find the frame where the ball is at its lowest point
smallest_frame = binary_search(frames, 0, len(frames) - 2, 0, frames[0], False, 0)

#make the call on the lowest frame
inOrOut(first, smallest_frame)