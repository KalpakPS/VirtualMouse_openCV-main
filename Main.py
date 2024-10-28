import mediapipe as mp
import math
from pathlib import Path
import cv2 as cv
import numpy as np
import autopy
import time
import sys
from tkinter import *
import threading
import pyautogui

OUTPUT_PATH = Path(__file__).parent
<<<<<<< HEAD:Main.py
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")  # gui assets path
=======
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")  # gui assets path
>>>>>>> e0a77b6b3c6541545bea1dff48d40b660e2585c9:gui.py


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

####################################


window = Tk()
window.title("Virtual Mouse")
window.geometry("700x500")
window.configure(bg="#252525")
canvas = Canvas(
    window,
    bg="#252525",
    height=500,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    350.0,
    250.0,
    image=image_image_1
)

canvas.create_text(
    180.0,
    61.0,
    anchor="nw",
    text="VIRTUAL MOUSE",
    fill="#FFFFFF",
    font=("Arial BoldMT", 40 * -1)
)

canvas.create_rectangle(
    42.979949951171875,
    132.50570678710938,
    657.0199279785156,
    133.50570678710938,
    fill="#FFFFFF",
    outline="")

# stop
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: stop_program(),
    relief="flat"
)
button_1.place(
    x=265.0,
    y=306.0,
    width=170.0,
    height=51.0
)

# start
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: start_main_loop(),
    relief="flat"
)
button_2.place(
    x=265.0,
    y=224.0,
    width=170.0,
    height=51.0
)

window.resizable(False, False)


<<<<<<< HEAD:Main.py
class HandDetector :
    def __init__(self ,mode=False , maxHand=2 , detectCon=0.5 ,trackCon=0.5):
        self.mode = mode
        self.maxHand = maxHand
        self.detectCon = detectCon
        self.trackCon = trackCon

        #############################
        self.mpHand = mp.solutions.hands
        self.Hands = self.mpHand.Hands(self.mode,self.maxHand,1,self.detectCon,self.trackCon)  # it has detection mode and Tracking mode when we dont have any thing to trackn in goes to detection mode
                                                                                             # Hands = mpHand.Hands(False,2,min_tracking_confidence=0.5) it can be like that but these are already set as defult so we can leave them
                                                                                             # please note thet this library (hand) just take RGB img
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        #############################


    def findhands(self, img, draw = True):
        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.processHand = self.Hands.process(imgRGB)
        # print(processHand.multi_hand_landmarks)
        if self.processHand.multi_hand_landmarks:  # you can use processHand.multi_hand_landmarks[0] or [1] this hand.no
            for handLMS in self.processHand.multi_hand_landmarks:
                if draw :
                    self.mpDraw.draw_landmarks(img, handLMS, self.mpHand.HAND_CONNECTIONS)

    def findPosition(self ,img ,handsNo=0 ):
        self.lmlist=[]
        xList=[]
        ylist=[]
        bbox=[]
        if self.processHand.multi_hand_landmarks:  # you can use processHand.multi_hand_landmarks[0] or [1] this hand.no
            try:
                myHand = self.processHand.multi_hand_landmarks[handsNo]
                for id, lm in enumerate(myHand.landmark):
                    # print(id, lm)  # the hands has 21 points [0 to 20] each point indicate some part of hand
                    # the problem is that the lm is in decimal and we need pixel ex:(200 w,300 h)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)  # now we have the (id,cx,cy) so we can do anything
                    self.lmlist.append([id,cx,cy])
                    xList.append(cx)
                    ylist.append(cy)
                xmin,xmax = min(xList),max(xList)
                ymin,ymax = min(ylist),max(ylist)
                bbox=xmin,ymin,xmax,ymax
            except:
                pass

        return self.lmlist,bbox

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmlist[self.tipIds[0]][1] > self.lmlist[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=10, t=3):
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv.circle(img, (x1, y1), r, (255, 0, 255), cv.FILLED)
            cv.circle(img, (x2, y2), r, (255, 0, 255), cv.FILLED)
            cv.circle(img, (cx, cy), r, (0, 0, 255), cv.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length,[x1, y1, x2, y2, cx, cy]
    
###########################
=======
def check_s_pressed(event):
    if event.char == 's':
        start_main_loop()


window.bind("<KeyPress>", check_s_pressed)  # start if 's' is pressed in the keyboard
####################################
>>>>>>> e0a77b6b3c6541545bea1dff48d40b660e2585c9:gui.py


wCam, hCam = 640, 480
wScr, hScr = autopy.screen.size()
frameR = 150
smootheing = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv.VideoCapture(0)  # webcam video capturing
cap.set(3, wCam)
cap.set(4, hCam)
detector = HandDetector()

running = True  # Added running flag to control the main loop


def Mouse(img):
    global frameR, smootheing, plocX, plocY, clocX, clocY, wScr, wCam, hScr, hCam
    # finding hands
    detector.findhands(img)

    lmlist, bbox = detector.findPosition(img)
    cv.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    # 2. get the tip of index and midel finger
    if len(lmlist) != 0:
        Xindex, Yindex = lmlist[8][1], lmlist[8][2]
        #Xmidel, Ymidel = lmlist[12][1], lmlist[12][2]
        #Xthumb, Ythumb = lmlist[4][1], lmlist[4][2]
        # 3. check which one is up?
        fingers = detector.fingersUp()
        # 4. index: moving mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. cordinates the position (cam :640*480) to (screen :2560 × 1600)
            xMOUSE = np.interp(Xindex, (frameR, wCam - frameR), (0, wScr))
            yMOUSE = np.interp(Yindex, (frameR, hCam - frameR), (0, hScr))
            # 6. smoothen value
            clocX = plocX + (xMOUSE - plocX) / smootheing
            clocY = plocY + (yMOUSE - plocY) / smootheing
            # 7. move mouse
            autopy.mouse.move(clocX, clocY)
            cv.circle(img, (Xindex, Yindex), 10, (20, 180, 90), cv.FILLED)
            plocY, plocX = clocY, clocX

        # 8. both are up : cliking mode
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] != 1 and fingers[4] != 1:
            # 9. finding distance
            length, bbox = detector.findDistance(8, 12, img)
            print(length)
            # 10. click if distance was short
            if length < 25:
                autopy.mouse.click()
                time.sleep(0.2)
        # 11. three fingers are up : right clicking mode
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] != 1:
            # 12. finding distance
            length, bbox = detector.findDistance(8, 12, img)
            print(length)
            detector.findDistance(12, 16, img)
            # 13. right click if distance was short
            if length < 25:
                autopy.mouse.click(button=autopy.mouse.Button.RIGHT)
                time.sleep(0.5)
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            # Middle mouse button click
            length, bbox = detector.findDistance(8, 12, img)
            detector.findDistance(12, 16, img)
            detector.findDistance(16, 20, img)
            if length < 25:
                pyautogui.click(button='middle')
                time.sleep(0.7)
    return img


def main():
    global running
    while running:  # Modified to use the running flag
        success, img = cap.read()
        img = cv.flip(img, 1)
        img = Mouse(img)

        # display
        cv.imshow("Webcam", img)
        cv.waitKey(1)


global thread


def start_main_loop():  # Function to run main() in a separate thread
    global running, thread
    running = True  # Reset the flag before starting a new thread
    thread = threading.Thread(target=main)
    thread.start()


def stop_program():
    global running
    running = False
    # Release the webcam resource
    cap.release()
    thread.join()  # Wait for the thread to finish
    sys.exit()  # close all window


window.mainloop()
