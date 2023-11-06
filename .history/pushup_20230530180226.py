
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import time
import random
cap = cv2.VideoCapture('pushuplong.mp4')


def check_posture(landmarks, image):
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
    nose = landmarks[mp_pose.PoseLandmark.NOSE]

    # Calculate the distances between the landmarks
    nose_to_left_shoulder = np.sqrt(
        (nose.x - left_shoulder.x)**2 + (nose.y - left_shoulder.y)**2)
    nose_to_right_shoulder = np.sqrt(
        (nose.x - right_shoulder.x)**2 + (nose.y - right_shoulder.y)**2)
    left_shoulder_to_left_hip = np.sqrt(
        (left_shoulder.x - left_hip.x)**2 + (left_shoulder.y - left_hip.y)**2)
    right_shoulder_to_right_hip = np.sqrt(
        (right_shoulder.x - right_hip.x)**2 + (right_shoulder.y - right_hip.y)**2)

    # Check if the distances meet the criteria for a correct push-up posture
    if (nose_to_left_shoulder / left_shoulder_to_left_hip < 1.1 and
        nose_to_right_shoulder / right_shoulder_to_right_hip < 1.1 and
        left_shoulder.y > left_hip.y and
        right_shoulder.y > right_hip.y):
        cv2.putText(image, "Correct Pushup Posture", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return True
    else:
        if nose_to_left_shoulder / left_shoulder_to_left_hip >= 1.1:
            cv2.putText(image, "Warning: Nose too high", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        elif left_shoulder.y <= left_hip.y:
            cv2.putText(image, "Warning: Hips too high", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        elif right_shoulder.y <= right_hip.y:
            cv2.putText(image, "Warning: Hips too high", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else:
            cv2.putText(image, "Incorrect Pushup Posture", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return False



with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    count = 0
    total_calories_burned = 0
    prev_flip_flag = 150
    flip_flag = 150
    buffer_time = 100
    a = [0 for i in range(buffer_time)]
    a_up = [0 for i in range(buffer_time)]
    a_down = [0 for i in range(buffer_time)]
    a_pref_flip = [0 for i in range(buffer_time)]
    a_flip = [0 for i in range(buffer_time)]
    while cap.isOpened():  
        success, image = cap.read()
        if not success:
            break
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
            landmarks = results.pose_landmarks.landmark
            cY = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * \
                image.shape[0]
            a.pop(0)
            a.append(cY)
            a_max = 0.5 * np.max(a) + 0.5 * a[-1]
            a_up.pop(0)
            a_up.append(a_max)
            a_min = 0.5 * np.min(a) + 0.5 * a[-1]
            a_down.pop(0)
            a_down.append(a_min)
            prev_flip_flag = flip_flag
            a_pref_flip.pop(0)
            a_pref_flip.append(prev_flip_flag)
            if cY > 0.9*a_max and flip_flag == 150:
                flip_flag = 250
            if cY < 1.111*a_min and flip_flag == 250:
                flip_flag = 150
            a_flip.pop(0)
            a_flip.append(flip_flag)
            if prev_flip_flag > flip_flag:
                count = count + 1
                total_calories_burned = count * 0.36
                if check_posture(landmarks, image):

                    cv2.putText(image, "Correct Pushup Posture", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else:
                    cv2.putText(image, "Incorrect Pushup Posture", (50,  50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.putText(image, "count = " + str(count), (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(image, "Total Calories Burned: " + str(total_calories_burned), (50, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('Pushup Detection', image)
        except:
            pass
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
