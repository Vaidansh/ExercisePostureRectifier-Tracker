import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np

class BufferList:
    def __init__(self, buffer_time, default_value=0):
        self.buffer = [default_value for _ in range(buffer_time)]

    def push(self, value):
        self.buffer.pop(0)
        self.buffer.append(value)

    def max(self):
        return max(self.buffer)

    def min(self):
        buffer = [value for value in self.buffer if value]
        if buffer:
            return min(buffer)
        return 0
# file
file_name = "ropeskip.mp4"

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
total_calories_burned = 0
# center y
selected_landmarks = [23, 24]

buffer_time = 80
center_y = BufferList(buffer_time)
center_y_up = BufferList(buffer_time)
center_y_down = BufferList(buffer_time)
center_y_pref_flip = BufferList(buffer_time)
center_y_flip = BufferList(buffer_time)

cy_max = 100
cy_min = 100
flip_flag = 250
prev_flip_flag = 250
count = 0
posture = "Wrong"
# For webcam input:
cap = cv2.VideoCapture('ropeskip.mp4')
# cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image_height, image_width, _ = image.shape

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
            )
            landmarks = [
                (lm.x * image_width, lm.y * image_height)
                for i, lm in enumerate(results.pose_landmarks.landmark)
                if i in selected_landmarks
            ]
            cx = int(np.mean([x[0] for x in landmarks]))
            cy = int(np.mean([x[1] for x in landmarks]))

            landmarks = [
                (lm.x * image_width, lm.y * image_height)
                for i, lm in enumerate(results.pose_landmarks.landmark)
                if i in [11, 12]
            ]
            cy_shoulder_hip = cy - int(np.mean([x[1] for x in landmarks]))
        else:
            cx = 0
            cy = 0
            cy_shoulder_hip = 0

        cy = int((cy + center_y.buffer[-1]) / 2)
        # set data
        center_y.push(cy)

        cy_max = 0.5 * cy_max + 0.5 * center_y.max()
        center_y_up.push(cy_max)

        cy_min = 0.5 * cy_min + 0.5 * center_y.min()
        center_y_down.push(cy_min)

        prev_flip_flag = flip_flag
        center_y_pref_flip.push(prev_flip_flag)

        dy = cy_max - cy_min
        if dy > 0.4 * cy_shoulder_hip:
            if cy > cy_max - 0.55 * dy and flip_flag == 150:
                flip_flag = 250
            if 0 < cy < cy_min + 0.35 * dy and flip_flag == 250:
                flip_flag = 150
        center_y_flip.push(flip_flag)

        if prev_flip_flag < flip_flag:
            count = count + 1
            posture = "Correct"
            total_calories_burned = 0.13*count

        cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)
        cv2.putText(
            image,
            "centroid",
            (cx - 25, cy - 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
        )
        cv2.putText(
            image,
            "Posture = " + posture ,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            image,
            "count = " + str(count),
            (int(image_width * 0.6), int(image_height * 0.4)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            2,
        )
        cv2.putText(image, "Total Calories Burned: " + str(total_calories_burned), (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.imshow("MediaPipe Pose", image)
        # out.write(image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
