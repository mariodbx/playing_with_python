import os
import subprocess
import asyncio
import threading
import keyboard
import logging
import time

# Set up logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.log')
error_log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'error.log')

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
error_logger = logging.getLogger('error')
error_handler = logging.FileHandler(error_log_file)
error_handler.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)

# Define paths to the scripts
script_dir = os.path.dirname(os.path.abspath(__file__))
text_extractor_script = os.path.join(script_dir, 'text_extractor.py')
text_reader_script = os.path.join(script_dir, 'text_reader.py')

# Flag to control text reader execution
text_reader_process = None

async def run_text_extractor():
    """Run the text extractor script and log its output."""
    logging.info("Running text extractor...")
    try:
        result = subprocess.run(['python', text_extractor_script], check=True, text=True, capture_output=True)
        logging.info(f"Text extraction completed. Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        error_logger.error(f"Error during text extraction: {e}\n{e.output}")
        logging.error(f"Error during text extraction: {e}")

async def run_text_reader():
    """Run the text reader script."""
    global text_reader_process
    if text_reader_process:
        text_reader_process.terminate()  # Terminate the existing process

    logging.info("Starting text reader...")
    try:
        text_reader_process = subprocess.Popen(['python', text_reader_script])
        logging.info("Text reader started.")
    except Exception as e:
        error_logger.error(f"Error starting text reader: {e}")
        logging.error(f"Error starting text reader: {e}")

async def execute_tasks():
    """Execute text extraction and reading asynchronously."""
    await run_text_extractor()
    await asyncio.sleep(1)  # Give time for text extraction to complete
    await run_text_reader()

def on_alt_press():
    """Handle Alt key press event."""
    logging.info("Alt key pressed. Executing tasks...")
    asyncio.run(execute_tasks())  # Run async tasks in the main thread

def monitor_keyboard():
    """Monitor keyboard for Alt key press."""
    keyboard.add_hotkey('alt', on_alt_press)
    logging.info("Press Alt to capture text and start reading...")
    keyboard.wait('esc')  # Press 'Esc' to exit the script

if __name__ == "__main__":
    # Start the keyboard monitoring in a separate thread
    keyboard_thread = threading.Thread(target=monitor_keyboard, daemon=True)
    keyboard_thread.start()

    # Keep the script running to listen for keyboard events
    try:
        while True:
            time.sleep(1)  # This keeps the main thread alive
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
