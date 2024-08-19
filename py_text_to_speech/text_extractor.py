import pytesseract
import pyscreenshot as ImageGrab
import tkinter as tk
import numpy as np
import cv2
import logging
import os

# Configure Tesseract executable path if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# File paths for logging
log_file_path = os.path.join(script_dir, 'extracted_text.txt')

# Configure logging
logging.basicConfig(filename=os.path.join(script_dir, 'text_extraction.log'), level=logging.INFO, format='%(asctime)s - %(message)s')

def capture_and_extract_text():
    print("Select the screen area to capture.")
    
    # Create a Tkinter window to handle the selection
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.6)  # Set the window to be slightly transparent
    root.overrideredirect(True)  # Remove window decorations

    # Fullscreen window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    canvas = tk.Canvas(root, cursor="cross", bg='#2C2C2C')  # Set canvas background to a darker gray
    canvas.pack(fill="both", expand=True)

    rect_start_x = rect_start_y = rect_end_x = rect_end_y = 0
    selection_done = tk.BooleanVar(value=False)
    
    def on_button_press(event):
        nonlocal rect_start_x, rect_start_y
        rect_start_x = event.x
        rect_start_y = event.y

    def on_mouse_move(event):
        nonlocal rect_end_x, rect_end_y
        rect_end_x = event.x
        rect_end_y = event.y
        canvas.delete("selection_rectangle")
        canvas.create_rectangle(rect_start_x, rect_start_y, rect_end_x, rect_end_y, outline='purple', width=2, tags="selection_rectangle", fill='', stipple='gray50')

    def on_button_release(event):
        nonlocal rect_end_x, rect_end_y
        rect_end_x = event.x
        rect_end_y = event.y
        root.quit()
        selection_done.set(True)

    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    root.mainloop()

    if not selection_done.get():
        print("Selection was not completed.")
        return

    # Correct coordinates of the selected rectangle
    x1 = min(rect_start_x, rect_end_x)
    y1 = min(rect_start_y, rect_end_y)
    x2 = max(rect_start_x, rect_end_x)
    y2 = max(rect_start_y, rect_end_y)

    x1_screen = root.winfo_rootx() + x1
    y1_screen = root.winfo_rooty() + y1
    x2_screen = root.winfo_rootx() + x2
    y2_screen = root.winfo_rooty() + y2

    print(f"Captured coordinates: ({x1_screen}, {y1_screen}) to ({x2_screen}, {y2_screen})")

    try:
        # Capture the selected area
        im = ImageGrab.grab(bbox=(x1_screen, y1_screen, x2_screen, y2_screen))
        im_np = np.array(im)
        gray = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray)
        print(f"Extracted text: {text}")

        if text.strip():
            # Save extracted text to a file
            with open(log_file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            logging.info(f"Text extracted: {text}")
        else:
            print("No text detected or text is empty.")
            logging.info("No text detected or text is empty.")

    except Exception as e:
        error_msg = f"An error occurred during text extraction: {e}"
        print(error_msg)
        logging.error(error_msg)

    # Explicitly destroy the Tkinter window to remove the overlay
    root.destroy()

if __name__ == "__main__":
    capture_and_extract_text()
