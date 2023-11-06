# import cv2
# import mediapipe as mp
# import math
# import numpy as np

# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose

# cap = cv2.VideoCapture('bicep_curls.mp4')

# with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#     count = 0
#     posture = "neutral"
#     flip = 0
#     incorrect_count = 0
#     correct_count = 0
#     threshold_incorrect = 5
#     threshold_correct = 3
#     total_time = 0
#     while cap.isOpened():
#         ret, image = cap.read()
#         if not ret:
#             break
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#         image = cv2.flip(image, 1)
#         image.flags.writeable = False
#         results = pose.process(image)
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         mp_drawing.draw_landmarks(
#             image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
#         if results.pose_landmarks is not None:
#             left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
#             left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
#             left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
#             right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
#             right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
#             right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
#             left_angle = math.degrees(math.atan2(left_wrist.y - left_elbow.y, left_wrist.x - left_elbow.x) -
#                                       math.atan2(left_shoulder.y - left_elbow.y, left_shoulder.x - left_elbow.x))
#             left_angle = abs(left_angle)
#             right_angle = math.degrees(math.atan2(right_wrist.y - right_elbow.y, right_wrist.x - right_elbow.x) -
#                                        math.atan2(right_shoulder.y - right_elbow.y, right_shoulder.x - right_elbow.x))
#             right_angle = abs(right_angle)
#             if flip == 0 and (left_angle < 40 or right_angle < 40):
#                 flip = 1
#                 count += 1
#                 posture = "correct"
#                 correct_count += 1
#                 incorrect_count = 0
#                 total_calories_burned = count * 0.1
#             elif flip == 1 and (left_angle > 70 and right_angle > 70):
#                 flip = 0
#                 posture = "incorrect"
#                 incorrect_count += 1
#                 correct_count = 0
#             else:
#                 posture = "neutral"
#                 incorrect_count = 0
#                 correct_count = 0
#             total_calories_burned = count * 0.1
#             if incorrect_count >= threshold_incorrect:
#                 cv2.putText(image, "Correct your posture!", (50,
#                             50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#             elif correct_count >= threshold_correct:
#                 cv2.putText(image, "Great job!", (50, 50),
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#             cv2.putText(image, "Curl Count: " + str(count), (50, 100),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#             cv2.putText(image, "Posture: " + posture, (50, 150),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#             cv2.putText(image, "Total Calories Burned: " + str(total_calories_burned), (50, 200),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#         cv2.imshow('Bicep Curls', image)
#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break
# cap.release()
# cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def get_landmarks(pose_results):
    """Extracts pose landmarks from the Mediapipe results."""
    landmarks = {}
    for landmark in mp_pose.PoseLandmark:
        landmarks[landmark] = pose_results.pose_landmarks.landmark[landmark]
    return landmarks


def get_angle(a, b, c):
    """Calculates the angle between three points (a-b-c)."""
    radians = math.atan2(c.y - b.y, c.x - b.x) - \
        math.atan2(a.y - b.y, a.x - b.x)
    angle_degrees = abs(math.degrees(radians))
    return angle_degrees


def process_video(file_path):
    """Processes a video file and detects bicep curls."""
    cap = cv2.VideoCapture(file_path)
    if file_path == 0:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # set the frame width to 1280 pixels
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # set the frame height to 720 pixels
    count = 0
    posture = "neutral"
    flip = 0
    incorrect_count = 0
    correct_count = 0
    threshold_incorrect = 5
    threshold_correct = 3
    total_time = 0
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, image = cap.read()
            if not ret:
                break
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = cv2.flip(image, 1)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            if results.pose_landmarks is not None:
                landmarks = get_landmarks(results)
                left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
                left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
                # Calculate angles
                left_angle = math.degrees(math.atan2(left_wrist.y - left_elbow.y, left_wrist.x - left_elbow.x) -
                                       math.atan2(left_shoulder.y - left_elbow.y, left_shoulder.x - left_elbow.x))
                left_angle = abs(left_angle)
                right_angle = math.degrees(math.atan2(right_wrist.y - right_elbow.y, right_wrist.x - right_elbow.x) -
                                      math.atan2(right_shoulder.y - right_elbow.y, right_shoulder.x - right_elbow.x))
                right_angle = abs(right_angle)
                left_angle_shoulder = get_angle(left_shoulder, left_elbow, left_hip)
                right_angle_shoulder = get_angle(right_shoulder, right_elbow, right_hip)

                # Check for correct posture
                if flip == 0 and (left_angle < 20 or right_angle < 20):
                    flip = 1
                    count += 1
                    posture = "correct"
                    correct_count += 1
                    incorrect_count = 0
                    total_calories_burned = count * 0.1
                elif flip == 1 and (left_angle > 70 and right_angle > 70):
                    flip = 0
                    posture = "incorrect"
                    incorrect_count += 1
                    correct_count = 0
                else:
                    posture = "neutral"
                    incorrect_count = 0
                    correct_count = 0

                # Check for angle > 70 degrees and show warning
                if left_angle_shoulder > 220:
                    cv2.putText(image, "Put your Right arm closer!", (50, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if right_angle_shoulder < 145:
                    cv2.putText(image, "Put your Left arm closer!",
                                (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                total_calories_burned = count * 0.1
                if incorrect_count >= threshold_incorrect:
                    cv2.putText(image, "Correct your posture!", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                elif correct_count >= threshold_correct:
                    cv2.putText(image, "Great job!",
                                (50, 50), 1, (0, 255, 0), 2)
                cv2.putText(image, "Count: {}".format(count), (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "Posture: {}".format(
                    posture), (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "Calories burned: {}".format(
                    total_calories_burned), (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "Right angle: {:.2f}".format(
                    left_angle_shoulder), (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                cv2.putText(image, "Left angle: {:.2f}".format(right_angle_shoulder), (50, 300),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                cv2.putText(image, "Right arm angle: {:.2f}".format(
                    left_angle), (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                cv2.putText(image, "Left arm angle: {:.2f}".format(right_angle), (50, 400),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            cv2.imshow('Bicep Curl Detector', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()


process_video(0)
