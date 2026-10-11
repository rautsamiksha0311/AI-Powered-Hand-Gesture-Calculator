
import cv2
import mediapipe as mp
import numpy as np

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    model_complexity=1
)

canvas = None
previous_point = None
smooth_x, smooth_y = None, None
last_valid_point = None
unknown_frames = 0
clear_frames = 0

SMOOTHING = 0.65
MAX_GAP_FRAMES = 5
BRUSH_SIZE = 6
DRAW_COLOR = (255, 0, 255)

def recognize_gesture(hand):
    lm = hand.landmark
    index_up = lm[8].y < lm[6].y
    middle_up = lm[12].y < lm[10].y
    ring_up = lm[16].y < lm[14].y
    pinky_up = lm[20].y < lm[18].y

    if index_up and not middle_up and not ring_up and not pinky_up:
        return "Drawing"
    if index_up and middle_up and not ring_up and not pinky_up:
        return "Victory Sign"
    if all([index_up, middle_up, ring_up, pinky_up]):
        return "Open Palm"
    if not any([index_up, middle_up, ring_up, pinky_up]):
        return "Closed Fist"
    return "Unknown"

if not camera.isOpened():
    print("Error: Could not open camera.")
    raise SystemExit

print("Virtual Drawing Started")
print("Index finger: Draw | Open palm: Stop | Fist: Clear | Q: Quit")

try:
    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]

        if canvas is None:
            canvas = np.zeros_like(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        gesture = "No Hand Detected"

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(
                frame, hand, mp_hands.HAND_CONNECTIONS
            )

            gesture = recognize_gesture(hand)
            tip = hand.landmark[8]
            point = (int(tip.x * width), int(tip.y * height))

            if gesture == "Drawing":
                unknown_frames = 0

                if smooth_x is None:
                    smooth_x, smooth_y = point
                else:
                    smooth_x = int(
                        SMOOTHING * point[0]
                        + (1 - SMOOTHING) * smooth_x
                    )
                    smooth_y = int(
                        SMOOTHING * point[1]
                        + (1 - SMOOTHING) * smooth_y
                    )

                current_point = (smooth_x, smooth_y)

                if previous_point is not None:
                    cv2.line(
                        canvas,
                        previous_point,
                        current_point,
                        DRAW_COLOR,
                        BRUSH_SIZE,
                        cv2.LINE_AA
                    )
                else:
                    cv2.circle(
                        canvas,
                        current_point,
                        BRUSH_SIZE // 2,
                        DRAW_COLOR,
                        -1,
                        cv2.LINE_AA
                    )

                previous_point = current_point
                last_valid_point = current_point
                clear_frames = 0

            elif gesture == "Closed Fist":
                clear_frames += 1
                unknown_frames = 0

                if clear_frames >= 10:
                    canvas[:] = 0
                    previous_point = None
                    smooth_x, smooth_y = None, None
                    last_valid_point = None

            elif gesture == "Open Palm":
                previous_point = None
                smooth_x, smooth_y = None, None
                last_valid_point = None
                unknown_frames = 0
                clear_frames = 0

            else:
                unknown_frames += 1
                clear_frames = 0

                if unknown_frames > MAX_GAP_FRAMES:
                    previous_point = None
                    smooth_x, smooth_y = None, None
                    last_valid_point = None

        else:
            unknown_frames += 1
            clear_frames = 0

            if unknown_frames > MAX_GAP_FRAMES:
                previous_point = None
                smooth_x, smooth_y = None, None
                last_valid_point = None

        combined = cv2.addWeighted(frame, 0.7, canvas, 1.0, 0)

        cv2.putText(
            combined,
            "Gesture: " + gesture,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        cv2.putText(
            combined,
            "Index: Draw | Palm: Stop | Fist: Clear | Q: Quit",
            (20, height - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        cv2.imshow("AI Virtual Drawing", combined)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    hands.close()
    camera.release()
    cv2.destroyAllWindows()
