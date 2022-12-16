import serial
import mediapipe as mp
import cv2
import time
import math
movement_dictionary = {
    "f":"forward",
    "l":"left",
    "r":"right",
    "s":"stop"
}
# arduino interface connection and function
comport = 'COM4'  #change this comport to your systems comport before running
arduinoVar = serial.Serial(comport, 9600)
def send_to_arduino(prev_c, next_c):
    if not prev_c == next_c:
        print("sent-->",movement_dictionary[next_c])
        arduinoVar.write(next_c.encode())
    return next_c

# for video capture and calculation
cap = cv2.VideoCapture(0)
mpFace = mp.solutions.face_mesh
face = mpFace.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
mpDraw = mp.solutions.drawing_utils
mpDraw_style = mp.solutions.drawing_styles
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)
pTime = 0
cTime = 0
idList = [263, 473, 362, 386, 374, 133, 468, 33, 159, 145] 
 # list of id to represent the eye corner and iris

prev = ""
eye_open = True
blinkC = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face.process(imgRGB)
    if not success:
        continue

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:

            arr = [None] * 10

            for id, lm in enumerate(faceLms.landmark):
                for el in idList:
                    if id == el:
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.circle(img, (cx, cy), 1, (255, 0, 255), cv2.FILLED)
                        arr[idList.index(id)] = [cx, cy]

            # distance from iris to left, right, up and down corner
            e_l = math.dist(arr[0], arr[1])
            e_r = math.dist(arr[1], arr[2])
            e_u = math.dist(arr[3], arr[1])
            e_d = math.dist(arr[1], arr[4])

            # horizontal ratio for driving left and right
            ratio_h = e_l / e_r * 100

            # full ratio to calculate blink
            ratio = int((math.dist(arr[0], arr[2]) / math.dist(arr[3], arr[4]))*100)

            if ratio_h < 40:    #ratio<40
                prev = send_to_arduino(prev, "l")
            elif ratio_h > 150:
                prev = send_to_arduino(prev, "r")

            # one blink drive one blink stop code
            # elif(ratio > 800):
            #     if eye_open:
            #         if blinkC == 0:
            #             prev = send_to_arduino(prev, "s")
            #             blinkC = 1
            #         else:
            #             prev = send_to_arduino(prev, "f")
            #             blinkC = 0
            #         eye_open = False

            # one blink stop double blink drive code
            elif ratio > 800:
                if eye_open:
                    cTime = time.time()
                    if cTime - pTime < 0.5:
                        prev = send_to_arduino(prev, "f")
                        
                    else:
                        prev = send_to_arduino(prev, "s")
                    pTime = cTime
                    eye_open = False
            elif ratio < 800:
                eye_open = True
    img = cv2.flip(src=img, flipCode=1)
    cv2.imshow("Camera", img)
    cv2.waitKey(1)
    
  
  
""" Multi-line comment used
print("Python Comments") 

    
    
Output Obtained:
PS C:\Users\2000k\OneDrive\Desktop\BTP> python3 .\main.py
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
sent--> right
sent--> stop
sent--> forward
sent--> left
sent--> stop
sent--> forward
sent--> left
sent--> right
sent--> stop
sent--> left
sent--> stop
sent--> left
sent--> right
sent--> stop
Traceback (most recent call last):
  File "C:\Users\2000k\OneDrive\Desktop\BTP\main.py", line 38, in <module>
    success, img = cap.read()
KeyboardInterrupt
PS C:\Users\2000k\OneDrive\Desktop\BTP>

#Multiline comment ends here
"""  
    
