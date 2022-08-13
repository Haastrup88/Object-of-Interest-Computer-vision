import cv2
import numpy as np
width=720
height=320
HueLow=10
HueHigh=20
SatLow=10
SatHigh=20
ValLow=10
ValHigh=20
x=0
y=0
def onHueLow(val):
    global HueLow
    HueLow=val
    print("HueLow: ",HueLow)
def onHueHigh(val):
    global HueHigh
    HueHigh=val
    print("HueHigh: ",HueHigh)
def onSatLow(val):
    global SatLow
    SatLow=val
    print("SatLow: ",SatLow)
def onSatHigh(val):
    global SatHigh
    SatHigh=val
    print("SatHigh: ",SatHigh)
def onValLow(val):
    global ValLow
    ValLow=val
    print("ValLow: ",ValLow)
def onValHigh(val):
    global ValHigh
    ValHigh=val
    print("ValHigh: ",ValHigh)
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*"MJPG"))
cv2.namedWindow("Trackbar")
cv2.resizeWindow("Trackbar",500,300)
cv2.moveWindow("Trackbar",width,0)
cv2.createTrackbar("Hue_low","Trackbar",10,179,onHueLow)
cv2.createTrackbar("Hue_high","Trackbar",20,179,onHueHigh)
cv2.createTrackbar("Sat_low","Trackbar",10,255,onSatLow)
cv2.createTrackbar("Sat_high","Trackbar",20,255,onSatHigh)
cv2.createTrackbar("val_low","Trackbar",10,255,onValLow)
cv2.createTrackbar("val_high","Trackbar",20,255,onValHigh)
while True:
    _,frame=cam.read()
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lowerbound=np.array([HueLow,SatLow,ValLow])
    upperbound=np.array([HueHigh,SatHigh,ValHigh])
    mask=cv2.inRange(frameHSV,lowerbound,upperbound)
    mask_resize=cv2.resize(mask,(int(width/2),int(height/2)))
    object=cv2.bitwise_and(frame,frame,mask=mask)
    object_resize=cv2.resize(object,(int(width/2),int(height/2)))
    contours,junk=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame,contour,-1,(255,0,0),3)
    for contour in contours:
        area=cv2.contourArea(contour)
        if(area>=200):
            #cv2.drawContours(frame,[contour],0,(255,0,0),3)
            x,y,w,h=cv2.boundingRect(contour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            xpos=x
            ypos=y
            xpos=int(xpos/width*1920)
            ypos=int(ypos/height*1080)

    cv2.imshow("Window",frame)
    cv2.moveWindow("Window",x,y)
    cv2.imshow("Mask",mask_resize)
    cv2.moveWindow("Mask",0,height)
    cv2.imshow("Object",object_resize)
    cv2.moveWindow("Object",int(width/2),height)
    if cv2.waitKey(1) & 0xff==ord("r"):
        break
cam.release()
