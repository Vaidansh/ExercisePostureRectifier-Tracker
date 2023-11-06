import cv2
import mediapipe as mp
import numpy as np
from math import acos, degrees

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
posture = "Wrong"
cap = cv2.VideoCapture('squat1.mp4')


total_calories_burned = 0
# cap = cv2.VideoCapture(0)
up = False
down = False
count = 0

# sss = cv2.VideoCapture("squatsz.mp4")
with mp_pose.Pose(
        static_image_mode=False) as pose:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        # frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks is not None:
            x1 = int(results.pose_landmarks.landmark[24].x * width)
            y1 = int(results.pose_landmarks.landmark[24].y * height)

            x2 = int(results.pose_landmarks.landmark[26].x * width)
            y2 = int(results.pose_landmarks.landmark[26].y * height)

            x3 = int(results.pose_landmarks.landmark[28].x * width)
            y3 = int(results.pose_landmarks.landmark[28].y * height)

            p1 = np.array([x1, y1])
            p2 = np.array([x2, y2])
            p3 = np.array([x3, y3])

            l1 = np.linalg.norm(p2 - p3)
            l2 = np.linalg.norm(p1 - p3)
            l3 = np.linalg.norm(p1 - p2)

            angle = degrees(acos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))
            if angle >= 160:
                up = True
            
            elif up == True and down == False and angle <= 70:
                down = True
                posture = "Go Up Now!"
                # posture = "Correct"

            if up == True and down == True and angle >= 160:
                count += 1
                up = False
                down = False
                
                total_calories_burned = 0.32*count
                # if angle < 70:
                #     posture = "Wrong - You didn't complete the full squat!"
                #     count -= 1
            elif up == False and down == False and angle <= 170 or angle >=70:
                posture = "Go more down!"
            elif up == False and down == True and angle <= 70:
                posture = "Go up!"
            # if angle >= 160:
            #     up = True
            #     posture = "Correct"
            # elif up == True and down == False and angle <= 70:
            #     down = True
            #     posture = "Go Up Now!"
            # elif up == True and down == True and angle >= 160:
            #     count += 1
            #     up = False
            #     down = False
            #     posture = "Correct"
            #     total_calories_burned = 0.32*count
            # if angle < 70:
            #     posture = "Wrong - You didn't complete the full squat!"

            # if angle > 70 and angle < 160:
            #     posture = "Go more Down"
            aux_image = np.zeros(frame.shape, np.uint8)
            cv2.line(aux_image, (x1, y1), (x2, y2), (255, 255, 0), 20)
            cv2.line(aux_image, (x2, y2), (x3, y3), (255, 255, 0), 20)
            cv2.line(aux_image, (x1, y1), (x3, y3), (255, 255, 0), 5)
            contours = np.array([[x1, y1], [x2, y2], [x3, y3]])
            cv2.fillPoly(aux_image, pts=[contours], color=(128, 0, 250))

            output = cv2.addWeighted(frame, 1, aux_image, 0.8, 0)
            cv2.circle(output, (x1, y1), 6, (0, 255, 255), 4)
            cv2.circle(output, (x2, y2), 6, (128, 0, 250), 4)
            cv2.circle(output, (x3, y3), 6, (255, 191, 0), 4)
            cv2.rectangle(output, (0, 0), (60, 60), (255, 255, 0), -1)
            cv2.putText(output, str(int(angle)), (x2 + 30, y2),
                        1, 1.5, (128, 0, 250), 2)
            cv2.putText(output, str(count), (10, 50), 1, 3.5, (128, 0, 250), 2)
            cv2.putText(output, "posture = " + posture,
                        (50, 50), 1, 1.5, (128, 0, 250), 2)
            cv2.putText(output, "Total Calories Burned: " + str(total_calories_burned), (50, 100),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.namedWindow("output", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("output", 1280, 768)
            cv2.imshow("output", output)
        # cv2.imshow("Frame", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()