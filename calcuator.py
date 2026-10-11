
import cv2
import mediapipe as mp
import math

camera = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.65
)

number1 = None
number2 = None
operation = "+"
result = None

last_number_count = None
current_action = None
action_frames = 0
release_frames = 0
action_locked = False

HOLD_FRAMES = 15
RELEASE_FRAMES = 8

def finger_states(hand):
    lm = hand.landmark

    index = lm[8].y < lm[6].y
    middle = lm[12].y < lm[10].y
    ring = lm[16].y < lm[14].y
    pinky = lm[20].y < lm[18].y

    return index, middle, ring, pinky

def is_rock(hand):
    index, middle, ring, pinky = finger_states(hand)
    return index and not middle and not ring and pinky

def is_shaka(hand, handedness):
    lm = hand.landmark
    index, middle, ring, pinky = finger_states(hand)

    if handedness == "Right":
        thumb = lm[4].x < lm[3].x
    else:
        thumb = lm[4].x > lm[3].x

    return thumb and pinky and not index and not middle and not ring

def is_ok_sign(hand):
    lm = hand.landmark

    thumb_index_distance = math.hypot(
        lm[4].x - lm[8].x,
        lm[4].y - lm[8].y
    )

    palm_size = math.hypot(
        lm[9].x - lm[0].x,
        lm[9].y - lm[0].y
    )

    index, middle, ring, pinky = finger_states(hand)

    fingers_up = middle and ring and pinky

    return (
        palm_size > 0 and
        thumb_index_distance < palm_size * 0.35 and
        fingers_up
    )

def detect_action(hand_list, handedness_list):
    actions = []

    for hand, handedness in zip(hand_list, handedness_list):
        label = handedness.classification[0].label

        if is_rock(hand):
            actions.append("SAVE")
        elif is_shaka(hand, label):
            actions.append("CALCULATE")
        elif is_ok_sign(hand):
            actions.append("RESET")

    # Do not act if two different control gestures appear together.
    if len(actions) == 1:
        return actions[0]

    return None

def calculate():
    global result

    if number1 is None or number2 is None:
        print("Save both numbers first!")
        return

    if operation == "+":
        result = number1 + number2
    elif operation == "-":
        result = number1 - number2
    elif operation == "*":
        result = number1 * number2
    elif operation == "/":
        if number2 == 0:
            result = None
            print("Cannot divide by zero!")
            return
        result = number1 / number2

    print("Result:", result)

try:
    while camera.isOpened():
        success, frame = camera.read()

        if not success:
            print("Could not read camera.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detected = hands.process(rgb)

        hand_list = detected.multi_hand_landmarks or []
        handedness_list = detected.multi_handedness or []

        for hand in hand_list:
            mp_draw.draw_landmarks(
                frame, hand, mp_hands.HAND_CONNECTIONS
            )

        # Count fingers only when no control gesture is detected.
        detected_action = detect_action(hand_list, handedness_list)

        if detected_action is None and hand_list:
            total_fingers = 0

            for hand, handedness in zip(hand_list, handedness_list):
                lm = hand.landmark
                index, middle, ring, pinky = finger_states(hand)

                label = handedness.classification[0].label
                if label == "Right":
                    thumb = lm[4].x < lm[3].x
                else:
                    thumb = lm[4].x > lm[3].x

                total_fingers += sum(
                    [thumb, index, middle, ring, pinky]
                )

            last_number_count = total_fingers

        # Require a gesture to remain steady for several frames.
        if detected_action == current_action and detected_action is not None:
            action_frames += 1
        else:
            current_action = detected_action
            action_frames = 1 if detected_action is not None else 0

        if detected_action is None:
            release_frames += 1
            if release_frames >= RELEASE_FRAMES:
                action_locked = False
        else:
            release_frames = 0

        if (
            current_action is not None and
            action_frames >= HOLD_FRAMES and
            not action_locked
        ):
            action_locked = True

            if current_action == "SAVE":
                if last_number_count is None:
                    print("Show a number with your fingers first!")
                elif number1 is None:
                    number1 = last_number_count
                    result = None
                    print("Number 1 saved:", number1)
                elif number2 is None:
                    number2 = last_number_count
                    result = None
                    print("Number 2 saved:", number2)
                else:
                    print("Both numbers are saved. Reset to start again.")

            elif current_action == "CALCULATE":
                calculate()

            elif current_action == "RESET":
                number1 = None
                number2 = None
                result = None
                last_number_count = None
                operation = "+"
                print("Calculator reset!")

        # Display information
        cv2.putText(
            frame, f"Number 1: {number1}", (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
        )
        cv2.putText(
            frame, f"Number 2: {number2}", (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
        )
        cv2.putText(
            frame, f"Operation: {operation}", (20, 105),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2
        )
        cv2.putText(
            frame, f"Number to save: {last_number_count}", (20, 140),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2
        )
        cv2.putText(
            frame, f"Gesture: {detected_action or 'None'}", (20, 175),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
        )

        if result is not None:
            cv2.putText(
                frame, f"Result: {result}", (20, 220),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3
            )

        cv2.putText(
            frame, "A:+  B:-  M:*  D:/  Q:Quit", (20, 270),
            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2
        )

        cv2.imshow("AI Gesture Calculator", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("a"):
            operation = "+"
            result = None
        elif key == ord("b"):
            operation = "-"
            result = None
        elif key == ord("m"):
            operation = "*"
            result = None
        elif key == ord("d"):
            operation = "/"
            result = None
        elif key == ord("q"):
            break

finally:
    hands.close()
    camera.release()
    cv2.destroyAllWindows()
