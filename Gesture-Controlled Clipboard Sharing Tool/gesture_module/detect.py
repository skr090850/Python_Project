import cv2
import mediapipe as mp

class HandGestureDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

    def get_gesture_state(self):
        success, image = self.cap.read()
        if not success:
            return None

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = self.hands.process(image_rgb)

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            landmarks = hand.landmark
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            dist = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
            self.mp_draw.draw_landmarks(image, hand, mp.solutions.hands.HAND_CONNECTIONS)
            cv2.imshow("Gesture Detection", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cap.release()
                cv2.destroyAllWindows()
            return "closed" if dist < 0.05 else "open"

        cv2.imshow("Gesture Detection", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
        return None