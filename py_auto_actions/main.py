from action_recorder import ActionRecorder
from action_storage import ActionStorage
from action_replayer import ActionReplayer

def main():
    recorder = ActionRecorder()
    storage = ActionStorage()
    replayer = ActionReplayer()

    # Record actions
    recorder.start_recording(duration=10)

    # Save actions to a file
    storage.save_actions("recorded_actions.txt", recorder.actions)

    # Load actions from a file
    actions = storage.load_actions("recorded_actions.txt")

    # Replay the recorded actions
    replayer.replay_actions(actions)

if __name__ == "__main__":
    main()
