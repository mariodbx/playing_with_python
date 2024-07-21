import pyautogui
import ast
import time

def replay_actions(file_path):
    with open(file_path, "r") as f:
        actions = f.readlines()

    print("Replaying actions...")

    for action_str in actions:
        action = ast.literal_eval(action_str.strip())
        if action[0] == 'move':
            pyautogui.moveTo(action[1], action[2])
        elif action[0] == 'click':
            pyautogui.click(action[1], action[2])

    print("Replay finished.")

if __name__ == "__main__":
    replay_actions("recorded_actions.txt")
