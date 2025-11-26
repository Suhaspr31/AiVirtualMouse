import cv2
import numpy as np
import HandTrackingModule as htm
import time
# import autopy
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


##########################
wCam, hCam = 1280, 720
frameR = 100 # Frame Reduction
smoothening = 5
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1, detectionCon=0.7, trackCon=0.7)
wScr, hScr = pyautogui.size()
# print(wScr, hScr)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    if success:
        img = detector.findHands(img)

        lmList, bbox = detector.findPosition(img)

        # 2. Get the tip of the index and middle fingers
        if len(lmList) != 0:
            print(f"Hands detected: {len(lmList)} landmarks")
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            fingers = detector.fingersUp()
            print(f"Fingers up: {fingers}")
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                        (255, 0, 255), 2)
        
        # 4. Only Index Finger : Moving Mode
            if fingers[1] == 1 and fingers[2] == 0:
                print("Moving mode")
            # 5. Convert Coordinates
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
                print(f"Moving mouse to: {wScr - clocX}, {clocY}")
                pyautogui.moveTo(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY
            
        # 8. Both Index and middle fingers are up : Clicking Mode
            if fingers[1] == 1 and fingers[2] == 1:
                print("Clicking mode")
            # 9. Find distance between fingers
                length, img, lineInfo = detector.findDistance(8, 12, img)
                print(f"Distance: {length}")
            # 10. Click mouse if distance short
                if length < 40:
                    print("Clicking")
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),
                            15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()

        # 10        # 9.5 Scrolling with 3 fingers up
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                print("Scrolling up")
                pyautogui.scroll(200)  # Scroll up
                time.sleep(0.2)  # Small delay to avoid super fast scrolling

        # 9.6 Scrolling with 4 fingers up
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                print("Scrolling down")
                pyautogui.scroll(-200)  # Scroll down
                time.sleep(0.2)
        
        
        # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        print(f"FPS: {int(fps)}")
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        
        # 12. Display
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    else:
        print("Failed to capture image from webcam.")
