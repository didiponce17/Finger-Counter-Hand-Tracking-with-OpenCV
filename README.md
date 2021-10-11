# Finger Counter Hand Tracking with OpenCV

The idea to develop this code to track the hand is to complement the myoelectric circuit developed previously. Looking forward to being able to have a similar function using Microsoft products such as Azure Machine Learning and Azure Cognitive, the idea for this project is to merge both the signals captured by the sensor from the muscle’s natural movement and computer vision to create a hand detector object to track the hand and store each and possible fingers movements into a dataset that later will improve the way the motors that powered the prototype act based on the EMG signals. 

Most of the hand prostheses are entirely body-driven and purely mechanical which decreases the patients’ quality of life and does not allow refined motor control. however, the very high cost of robotic prosthetics prohibits the majority of upper limb amputees from obtaining these devices to make their life easier. 

We would like to develop a cost-effective hand/forearm prosthesis by reimagining the future of accessibility by exploring how technology can better empower people who need prosthetic. 

# Hand Tracing Module

This code will track in real-time the hand, it could be converted into a module to be used multiple times if needed. The framework used is the mediapipe library developed by Google that helps with very fundamental AI problems such as face detection, facial landmarks, hand tracking, object detection. 

The module used for this project is hand tracking which uses two main modules at the back:

- Palm Detection: it works on complete image and provides a cropped image of the hand.
- Hand Landmarks: it is a module that module finds 21 different landmarks on the copped image of the hand to train this hand landmark it manually annotated 30 000 images of different hands. 

# FingerCounter

Once the HandTrackingModule is imported, we need to specify where the Arduino or serial device will be connected. This code will create the hand detector object, using only 1 hand for control. We got the landmarks.png file from the Google GitHub https://google.github.io/mediapipe/solutions/hands we will reference the tip of each finger with this. 

The camera gets initialized as the serial communication too, so it captures an image from the videocapture and sends the image to the mediapipe library to identify hands and draw landmarks over the image (if hands are found) and finally returns the ID of the landmark, and their position on X and Y, for all landmarks.

# Arduino Communication 

Using serial communication to send zeros and ones based on which finger is opened or closed. Whenever a finder is open it will send “one” or if close “cero, it means that the string that we will send from the Python code will be “0 0 0 0 0” and then it will have a dollar sign “$” in front of it. At the starting it will be a $ 0 0 0 0 0, these five digits correspond to whether each finger is open or close. 

For each individual finger, we are going to open and close. When testing you can make any sign or anything with your hand and it will represent that exact same gesture.  

![](FingerImages/Imagen%20ceros%20.png)

# Important Note: 

- Make sure you select the right COM port in the python file, and also make sure you do not have the serial monitor opened in Arduino IDE or something else since that causes the port to be busy when you try to run the python file.

- The images and folder "FingerImages" are optional but are right now being used in the code - could be removed later.

# Needed files:

- FingerCounter.ino
- FingerCounter.py 
- HandTrackingModule.py
- utilities.py
