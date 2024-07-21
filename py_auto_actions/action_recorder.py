import pyautogui
import time
import keyboard

class ActionRecorder:
    def __init__(self):
        self.actions = []
        self.recording = False

    def start_recording(self, duration=10):
        """Starts recording various actions for a specified duration."""
        self.recording = True
        print("Recording actions...")

        start_time = time.time()
        while (time.time() - start_time) < duration:
            x, y = pyautogui.position()
            self.actions.append(('move', x, y, time.time() - start_time))
            print(f"Recorded move to ({x}, {y})")

            if pyautogui.mouseDown():
                self.actions.append(('click', x, y, 'left', time.time() - start_time))
                print(f"Recorded left click at ({x}, {y})")

            if pyautogui.mouseDown(button='right'):
                self.actions.append(('click', x, y, 'right', time.time() - start_time))
                print(f"Recorded right click at ({x}, {y})")

            if keyboard.is_pressed('a'):  # Example of recording a key press
                self.actions.append(('keypress', 'a', time.time() - start_time))
                print("Recorded key press 'a'")

            if keyboard.is_pressed('ctrl'):
                self.actions.append(('keyrelease', 'ctrl', time.time() - start_time))
                print("Recorded key release 'ctrl'")

            scroll = pyautogui.scroll(0)
            if scroll != 0:
                self.actions.append(('scroll', scroll, time.time() - start_time))
                print(f"Recorded scroll {scroll}")

            time.sleep(0.1)  # Adjust this for the desired recording frequency

        self.recording = False
        print("Recording finished.")

    def record_action(self, action_type, *args):
        """Records a specific action."""
        if self.recording:
            self.actions.append((action_type, *args))
            print(f"Recorded action {action_type} with arguments {args}")
