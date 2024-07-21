import pyautogui
import time
import keyboard

class ActionReplayer:
    def replay_actions(self, actions):
        """Replays the recorded actions."""
        print("Replaying actions...")

        start_time = time.time()
        for action in actions:
            action_type = action[0]
            args = action[1:-1]
            timestamp = action[-1]
            elapsed = time.time() - start_time
            time.sleep(max(0, timestamp - elapsed))
            
            if action_type == 'move':
                pyautogui.moveTo(*args)
                print(f"Moved to {args}")
            elif action_type == 'click':
                button = args[2] if len(args) > 2 else 'left'
                pyautogui.click(*args[:2], button=button)
                print(f"Clicked {button} at {args[:2]}")
            elif action_type == 'keypress':
                keyboard.press(args[0])
                print(f"Pressed key {args[0]}")
            elif action_type == 'keyrelease':
                keyboard.release(args[0])
                print(f"Released key {args[0]}")
            elif action_type == 'scroll':
                pyautogui.scroll(args[0])
                print(f"Scrolled {args[0]}")

        print("Replay finished.")
