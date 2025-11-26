import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
from time import sleep

# Initialize camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Initialize hand detector
detector = HandDetector(detectionCon=0.8)
keyboard = Controller()

# Define keys
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["Space", "Backspace"]]

finalText = ""

# Define Button Class
class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# Create button list
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# Draw all buttons
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (x, y, w, h), colorC=(255, 0, 255), colorR=(0, 255, 0))
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    return img

# Main loop
while True:
    success, img = cap.read()
    if not success or img is None:
        print("No frame captured from webcam")
        continue

    hands, img = detector.findHands(img, flipType=False)  # Only ONE call to findHands

    img = drawAll(img, buttonList)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # Check if index finger tip (8) is inside button
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                index_finger = hand["lmList"][8][:2]  # Get (x, y) coordinates of index finger tip
                middle_finger = hand["lmList"][12][:2]

                l, _, _ = detector.findDistance(index_finger, middle_finger, img)

                click_threshold = 30

                if l < click_threshold:
                    for button in buttonList:
                        x, y = button.pos
                        w, h = button.size

        # Check if the index finger tip is inside the button area
                        if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
            # Simulate pressing the button by typing the corresponding letter
                            if button.text == "Space":
                                finalText += " "
                                keyboard.press(Key.space) 
                                keyboard.release(Key.space) # Simulate space key press
                            elif button.text == "Backspace":
                                finalText = finalText[:-1]
                                keyboard.press(Key.backspace)  # Use Key.backspace for backspace
                                keyboard.release(Key.backspace)  # Simulate backspace key press
                            else:
                                finalText += button.text
                                keyboard.press(button.text.lower())  # Simulate key press for letter
                                keyboard.release(button.text.lower())  # Simulate key press for letter
                                sleep(0.3)
    # Draw the typed text
    cv2.rectangle(img, (50, 500), (1200, 600), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 570),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
