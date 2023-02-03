# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 18:21:34 2019

@author: Administrator
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 15:23:57 2019
@author: zhangguangwei

"""
from datetime import datetime
import time
import cv2
import numpy as np
#import matplotlib.pyplot as plt
import os
from math import hypot
from tkinter import Tk
import serial

arduinoData =serial.Serial('/dev/cu.usbmodem14101',9600)

def led_on():
    arduinoData.write(str.encode('1'))
    
def led_off():
    arduinoData.write(str.encode('0'))

starttime = datetime.now()
deltaseconds = datetime.now()-starttime
deltaminutes = int(deltaseconds.total_seconds()/60) 
    
dateT = str(datetime.now().year) + str(datetime.now().month)+str(datetime.now().day) + '_'+str(datetime.now().hour)+'_'+ str(datetime.now().minute)
    


cap = cv2.VideoCapture(1)

root = '/Users/zhangguangwei/'

font = cv2.FONT_HERSHEY_SIMPLEX


Moving_track = [(0,0)]

width = int(cap.get(3))
height = int(cap.get(4))

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')

################ 
out = cv2.VideoWriter(root+'VGAT_RTPP_3.mp4',fourcc,30,(width,height))
##################




Peak_speed = 0


while not cap.isOpened():
    cap = cv2.VideoCapture(1)
    cv2.waitKey(1000)
    #os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
    print("Can't load the file")
    break


a=[(0,0)]
i=0
Counting = 0
record = False


while deltaminutes < 21:
    deltaseconds = datetime.now()-starttime
    deltaminutes = int(deltaseconds.total_seconds()/60) 
    i+=1
    ret, img_raw =cap.read() #start capture images from webcam
    if ret == False:
        break
    out.write(img_raw)
    img_gray = cv2.cvtColor(img_raw,cv2.COLOR_BGR2GRAY)
    y_start = 1
    y_stop = height
    
    x_start = 1
    x_stop = width

    x_start_region4Counting = 1
    x_stop_region4Counting = int(width/2)
    
    y_start_region4Counting = 1
    y_stop_region4Counting = height


    blur = cv2.GaussianBlur(img_gray,(5,5),0)

    retval,img_bi = cv2.threshold(blur,50,255,cv2.THRESH_BINARY_INV)

    binary,contours,hierarchy = cv2.findContours(img_bi.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        try:
            M = cv2.moments(c)
            center = ((M["m10"] / M["m00"])+(y_start), (M["m01"] / M["m00"])+(x_start))

            if radius >10:
            
                Counting_temp = (float(center[0]) > x_start_region4Counting) & (float(center[0]) < x_stop_region4Counting)  & (float(center[1]) > y_start_region4Counting) & (float(center[1]) < y_stop_region4Counting)       
                if Counting_temp:
                    led_on()
                else:
                    led_off()

                cv2.putText(img_raw,str(Counting_temp),(50,50),font,1,(255,0,0),2,cv2.LINE_AA)
                #print(temp_percent)
                cv2.rectangle(img_raw,(x_start_region4Counting,y_start_region4Counting),(x_stop_region4Counting,y_stop_region4Counting),(255,0,0))
                cv2.imshow(r'img',img_raw)
                
                
            
        except ZeroDivisionError:
            print("error")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()

print("Processing Done!")
led_off()
cv2.destroyAllWindows()
out.release()