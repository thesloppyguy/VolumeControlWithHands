# IMPORTS
import cv2 as cv
import mediapipe as mp
import time
import numpy as np
import HTmodule
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

vol_range = volume.GetVolumeRange()

minvol = vol_range[0]
maxvol = vol_range[1]

t1 = 0
t2 = 0
cam = cv.VideoCapture(0)
Module = HTmodule.Hand_Detector(detection_conf=0.75)

while True:
    success, frame = cam.read()
    Module.find_hands(frame, draw=False)
    lmlist = Module.find_position(frame)
    try:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        xm, ym = (x1+x2)//2, (y1+y2)//2
        cv.circle(frame, (x1, y1), 5, (255, 255, 0), cv.FILLED)
        cv.circle(frame, (x2, y2), 5, (255, 255, 0), cv.FILLED)
        cv.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
        cv.circle(frame, (xm, ym), 5, (255, 0, 0), cv.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        # print(length)  200-50
        if length < 50:
            cv.circle(frame, (xm, ym), 5, (255, 225, 0), cv.FILLED)
        vol = np.interp(length, [50, 200], [minvol, maxvol])
        print(vol, length)
        volume.SetMasterVolumeLevel(vol, None)
    except:
        pass
    # fps counter
    t1 = time.time()
    fps = 1/(t1-t2)
    t2 = t1
    cv.putText(frame, str(int(fps)), (10, 70),
               cv.FONT_HERSHEY_DUPLEX, 1.0, (255, 0, 255), 1)
    cv.imshow("video", frame)
    # fps counter ends

    # exit
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
