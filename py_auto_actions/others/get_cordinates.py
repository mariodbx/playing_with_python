import pyautogui
import tkinter as tk

def get_mouse_position():
    # Get the current mouse position
    x, y = pyautogui.position()
    return x, y

def update_coordinates_label():
    # Update the label text with the current mouse position
    x, y = get_mouse_position()
    coordinates_label.config(text=f"X: {x}, Y: {y}")
    root.after(100, update_coordinates_label)  # Update every 100 milliseconds

# Create a tkinter window
root = tk.Tk()
root.title("Mouse Coordinates")

# Create a label to display the coordinates
coordinates_label = tk.Label(root, font=("Helvetica", 16))
coordinates_label.pack(padx=10, pady=10)

# Start updating the coordinates label
update_coordinates_label()

# Set up the window to close properly
root.protocol("WM_DELETE_WINDOW", root.quit)

# Start the tkinter event loop
root.mainloop()


