
import cv2
import mediapipe as mp
import pyautogui
import math
import time

camera = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

previous_x, previous_y = None, None
smoothing = 0.25

PINCH_START = 0.045
PINCH_RELEASE = 0.075
PINCH_CONFIRM_TIME = 0.12
CLICK_COOLDOWN = 0.5

pinch_started = None
clicking = False
last_click_time = 0

if not camera.isOpened():
    print("Error: Could not open camera.")
    raise SystemExit

print("AI Hand Mouse Controller started.")
print("Move your index finger to move the cursor.")
print("Pinch thumb and index finger to click.")
print("Press Q in the camera window to quit.")

try:
    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        now = time.monotonic()

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(
                frame, hand, mp_hands.HAND_CONNECTIONS
            )

            index_tip = hand.landmark[8]
            index_joint = hand.landmark[6]
            thumb_tip = hand.landmark[4]

            target_x = int(index_tip.x * screen_width)
            target_y = int(index_tip.y * screen_height)

            if previous_x is None:
                previous_x, previous_y = target_x, target_y

            cursor_x = int(
                smoothing * target_x + (1 - smoothing) * previous_x
            )
            cursor_y = int(
                smoothing * target_y + (1 - smoothing) * previous_y
            )

            if index_tip.y < index_joint.y:
                pyautogui.moveTo(cursor_x, cursor_y)
                previous_x, previous_y = cursor_x, cursor_y

            distance = math.hypot(
                thumb_tip.x - index_tip.x,
                thumb_tip.y - index_tip.y
            )

            if distance < PINCH_START:
                if pinch_started is None:
                    pinch_started = now

                if (
                    now - pinch_started >= PINCH_CONFIRM_TIME
                    and not clicking
                    and now - last_click_time >= CLICK_COOLDOWN
                ):
                    pyautogui.click()
                    clicking = True
                    last_click_time = now
                    print("Click detected!")

            elif distance > PINCH_RELEASE:
                pinch_started = None
                clicking = False

            color = (0, 255, 0) if clicking else (0, 255, 255)

            cv2.putText(
                frame,
                f"Pinch distance: {distance:.3f}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            status = "CLICKED" if clicking else "Move or Pinch"
            cv2.putText(
                frame,
                status,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        else:
            previous_x, previous_y = None, None
            pinch_started = None
            clicking = False

        cv2.imshow("AI Hand Mouse Controller", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    hands.close()
    camera.release()
    cv2.destroyAllWindows()
