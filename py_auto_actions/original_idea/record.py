import pyautogui
import time

def record_actions(duration=10):
    actions = []

    print("Recording actions...")

    start_time = time.time()
    while (time.time() - start_time) < duration:
        x, y = pyautogui.position()
        actions.append(('move', x, y))
        time.sleep(0.1)  # Adjust this for the desired recording frequency

    print("Recording finished.")
    return actions

if __name__ == "__main__":
    recorded_actions = record_actions()
    with open("recorded_actions.txt", "w") as f:
        for action in recorded_actions:
            f.write(str(action) + "\n")
    print("Recorded actions saved to 'recorded_actions.txt'")
