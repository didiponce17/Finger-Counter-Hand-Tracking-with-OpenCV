import cv2 #requires: pip install cvzone
import time
import os
import HandTrackingModule as htm
import utilities as utils

wCam, hCam = 640, 480

#PC specific metadata
#cameraIndex = 1  #Choose which PC camera should be used
portNo = "COM5"  #Specify where the Arduino or serial device is connected

#Initializes the cv camera and sets the resolution to display
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)

#Initializes the serial connection
utils.connectToRobot(portNo)

#Pulls the Finger Images from the folder and saves them to the overlayList array, their index and name follows the same number of open fingers
folderPath = "FingerImages"
myList = os.listdir(folderPath)
#print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

pTime = 0

#Creates the hand detector object, using only 1 hand for control
detector = htm.handDetector(detectionCon=0.75, maxHands=1)

#The tip of each finger, this is taken by referencing the landmarks.png file, https://google.github.io/mediapipe/solutions/hands
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()           #captures an image from the videocapture
    img = detector.findHands(img)       #sends the image to the mediapipe library to identify hands and draw landmarks over the image (if hands are found)
    lmList = detector.findPosition(img, draw=True) #Returns ID of the landmark, and their position on X and Y, for all landmarks
    # print(lmList)
    
    if len(lmList) != 0: #The control will be executed only when there is something returned in the list (Hands are present)
        fingers = []

        #Determine hand side or L/R by using landmarks 5 and 17
        handSide = ""
        if lmList[5][1] < lmList[17][1]:
            handSide="L"
        else:
            handSide="R"

        #print(handSide)

        # Thumb - The thumb position is determined horizontally (on the X Axis - [n][1])
        if handSide == "R":
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]: #compares position of landmarks on the tip vs tip-1
                fingers.append(1)
            else:
                fingers.append(0)
        if handSide == "L":
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]: #compares position of landmarks on the tip vs tip-1
                fingers.append(1)
            else:
                fingers.append(0)

        # 4 Fingers - The other fingers position are determined vertically (on the Y Axis - [n][2])
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]: #compares position of landmarks on the tip vs tip-2
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)
        print(fingers)
        utils.sendData(fingers)

        #Pulls the image from the overlayList based on total fingers and draws it on top of the video capture
        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]

        cv2.rectangle(img, (70, 325), (180, 475), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (75, 450), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    #This is used to calculate the frequency that frames are shown in screen
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (485, 40), cv2.FONT_HERSHEY_PLAIN,
                2, (255, 0, 0), 3)

    #Shows the image captured/arranged
    cv2.imshow("Image", img)
    cv2.waitKey(1)