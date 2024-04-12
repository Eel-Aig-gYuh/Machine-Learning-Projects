import cv2
import hand as hnd
import time
import math
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)
# detector toc do xu li ban tay
detector = hnd.handDetector(detectionCon= int(0.5))


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange() # am luong cua may -65 - 0
#volume.SetMasterVolumeLevel(-20.0, None)

print(volRange[0], volRange[1])
minVol = volRange[0]
maxVol = volRange[1]

# ptime thoi gian bat dau
ptime = 0
font = cv2.FONT_HERSHEY_PLAIN

while True:
    ret, frame = cap.read()
    # frame gan ban tay
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)

    # xac dinh co ban tay trong cam
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])
        xDauNgonCai = lmList[4][1]
        yDauNgonCai = lmList[4][2]
        xDauNgonTro = lmList[8][1]
        yDauNgonTro = lmList[8][2]
        cv2.circle(frame, (xDauNgonCai,yDauNgonCai), 10, (255,255,255), -1)
        cv2.circle(frame, (xDauNgonTro,yDauNgonTro), 10, (255,255,255), -1)
        cv2.line(frame, (xDauNgonTro, yDauNgonTro), (xDauNgonCai,yDauNgonCai), (255,255,255), 2)
        # ve hinh tron tai trung diem
        tdx, tdy = (xDauNgonCai+xDauNgonTro) // 2, (yDauNgonCai + yDauNgonTro) // 2
        cv2.circle(frame, (tdx, tdy), 10, (255,255,255), -1)
        # tinh do dai duong thang
        d = math.hypot(xDauNgonTro - xDauNgonCai,yDauNgonTro - yDauNgonCai)
        # do dai ngon tro ngon cai tu 30 - 230
        # dai am thanh tu -65 - 0
        # interp: chuyen doi don vi thanh mot don vi tuong tu
        vol = np.interp(d,[30, 230], [minVol, maxVol])
        volBar = np.interp(d, [30, 230], [270, 100])
        percent = np.interp(vol, [minVol, maxVol], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        if d < 30:
            cv2.circle(frame, (tdx, tdy), 10, (0,100,0), -1)

        cv2.putText(frame, f"{int(percent)}%", (0, 300), font, 1, (184, 0, 100), 2)

        cv2.rectangle(frame, (10,100), (30, 270), (184,100,0), 2)

        cv2.rectangle(frame, (10,int(volBar)), (30, 270), (180,90,0), -1)



    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime

    cv2.putText(frame, f"FPS: {int(fps)}", (10, 50), font, 2, (184,131,73), 3)
    cv2.imshow("cam", frame)
    if cv2.waitKey(1) == ord('f'):
        break

cap.release()
cv2.destroyAllWindows()