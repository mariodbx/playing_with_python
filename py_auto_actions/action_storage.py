import ast

class ActionStorage:
    def save_actions(self, file_path, actions):
        """Saves the recorded actions to a file."""
        try:
            with open(file_path, "w") as f:
                for action in actions:
                    f.write(str(action) + "\n")
            print(f"Recorded actions saved to '{file_path}'")
        except Exception as e:
            print(f"An error occurred while saving actions: {e}")

    def load_actions(self, file_path):
        """Loads recorded actions from a file."""
        try:
            with open(file_path, "r") as f:
                actions = f.readlines()
            actions = [ast.literal_eval(action.strip()) for action in actions]
            print(f"Actions loaded from '{file_path}'")
            return actions
        except Exception as e:
            print(f"An error occurred while loading actions: {e}")
            return []
