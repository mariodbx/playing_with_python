import pyttsx3
import time
import os
import threading

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# File path for the text file
text_file_path = os.path.join(script_dir, 'extracted_text.txt')

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine_lock = threading.Lock()  # Lock to manage text-to-speech operations

def read_text(text):
    def speak():
        with engine_lock:
            # Stop any ongoing speech
            if engine.isBusy():
                engine.stop()
            engine.say(text)
            engine.runAndWait()

    threading.Thread(target=speak).start()

def monitor_file():
    last_modified_time = 0

    while True:
        try:
            current_modified_time = os.path.getmtime(text_file_path)
            if current_modified_time != last_modified_time:
                last_modified_time = current_modified_time
                with open(text_file_path, 'r', encoding='utf-8') as file:
                    text = file.read().strip()
                    if text:
                        print(f"Reading text: {text}")
                        read_text(text)
                    else:
                        print("File is empty or contains no valid text.")
            time.sleep(1)  # Check for file changes every second

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    monitor_file()
