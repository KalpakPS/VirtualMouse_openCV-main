from pathlib import Path
import cv2 as cv
import numpy as np
import autopy
import time
import sys
from tkinter import *
import threading
import pyautogui
import HandTrackingModule as htm  # Import HandTrackingModule


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\My Files\Programming\Mini project\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

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
    151.0,
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

###########################


wCam, hCam = 640, 480
wScr, hScr = autopy.screen.size()
frameR = 150
smootheing = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.HandDetector()

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
        Xmidel, Ymidel = lmlist[12][1], lmlist[12][2]
        Xthumb, Ythumb = lmlist[4][1], lmlist[4][2]
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
            cv.circle(img, (Xindex, Yindex), 15, (20, 180, 90), cv.FILLED)
            plocY, plocX = clocY, clocX

        # 8. both are up : cliking mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. finding distance
            length, bbox = detector.findDistance(8, 12, img)
            print(length)
            # 10. click if distance was short
            if length < 25:
                autopy.mouse.click()
                time.sleep(0.2)
                # 11. three fingers are up : right clicking mode
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
            # 12. finding distance
            length, bbox = detector.findDistance(8, 12, img)
            print(length)
            # 13. right click if distance was short
            if length < 25:
                autopy.mouse.click(button=autopy.mouse.Button.RIGHT)
                time.sleep(0.5)
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            # Middle mouse button click
            length, bbox = detector.findDistance(8, 12, img)
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
        cv.imshow("result", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


def start_main_loop():  # Function to run main() in a separate thread
    threading.Thread(target=main).start()


def stop_program():
    global running
    running = False
    sys.exit()


window.mainloop()
