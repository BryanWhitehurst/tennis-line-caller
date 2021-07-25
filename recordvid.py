import numpy as np
import cv2
import multiprocessing
import time
from processvideo import binary_search, getMask, inOrOut
import constant
import calculate_avg_green
import sys

def recordVideo(vidNum):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 

    #adjust these values so that the camera records just around the line
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, constant.RES_A)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, constant.RES_B)

    fourcc = cv2.VideoWriter_fourcc(*constant.FOURCC_CODE)
    out = cv2.VideoWriter(constant.VIDEO_PATH +str(vidNum) + '.avi', fourcc, 60.0, (constant.RES_A, constant.RES_B))

    while(1):
        ret, frame = cap.read() 
        out.write(frame)
    
    cap.release()
    out.release()

def lineCaller(vidNum): 
    print("starting line call on vid " + str(vidNum))
    cap = cv2.VideoCapture(constant.VIDEO_PATH + str(vidNum) + '.avi') 
    
    i = 0
    #skip 5 frames, let camera adjust
    while(i < 5): 
        cap.read()
        i = i+1

    ret, first = cap.read()
    frames = []
    j = 0

    #repeat process on every shot in video
    while(ret):
        #read in frames until ball is found
        while(1):
            ret, cur_frame = cap.read()
            if(not(ret)): break
            opening_ball, contours_ball = getMask(cur_frame, np.array(GREEN_LOW), np.array(GREEN_HIGH))
            if(len(contours_ball) != 0):
                frames.append(cur_frame) #if ball in this frame, append to list
                break #ball found so break out of this loop

        #read in frames until ball is no longer in the frame
        while(1): 
            ret, frame = cap.read()
            if(not(ret)): break
            opening_ball, contours_ball = getMask(frame, np.array(GREEN_LOW), np.array(GREEN_HIGH))
            if(len(contours_ball) == 0): break #ball no longer found so break out of this loop
            frames.append(frame) 

        print(len(frames))
        if(len(frames) != 0):
            #binary search to find the frame where the ball is at its lowest point
            smallest_frame = binary_search(frames, 0, len(frames) - 1, 0, first, False, 0)

            #make the call on the lowest frame
            inOrOut(first, smallest_frame, j + vidNum)

            #reset frames list
            frames.clear()
            j = j + 1 #increment result number
    print("end line call on vid " + str(vidNum))

# main function
if __name__ == '__main__':

    #calibrate color range for ball color
    avgGreen = calculate_avg_green.avgGreen(sys.argv[1]); #pass in from command line path to image
    GREEN_LOW = [avgGreen[0] - 20, avgGreen[1] - 20, avgGreen[2] - 20]
    GREEN_HIGH = [avgGreen[0] + 20, avgGreen[1] + 20, avgGreen[2] + 20]
    

    i = 1
    while(1):
        p = multiprocessing.Process(target=recordVideo, name="recording", args=(i,)) #process created to record video, pass in vid number
        p.start()
        time.sleep(10) #recording terminated after 10 seconds
        p.terminate()
        p.join()
        q = multiprocessing.Process(target=lineCaller, name="lineCaller" + str(i),args=(i,)) #create a new process for each video, pass in video number
        q.start()
        i = i + 1
