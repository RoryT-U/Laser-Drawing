import tkinter as tk
from PSoCBridge import PSoCBridge
from CVCam import CV
from console import Console

PSoC = PSoCBridge(True)

# Global variable to keep track of the currently active button (for modes)
active_button = None


# Function to toggle button states for modes
def toggle_button(button):
    global active_button

    if active_button and active_button != button:
        active_button.config(relief=tk.RAISED, bg="SystemButtonFace")

    if button["relief"] == tk.SUNKEN:
        button.config(relief=tk.RAISED, bg="SystemButtonFace")
        active_button = None
    else:
        button.config(relief=tk.SUNKEN, bg="grey")
        active_button = button


# Function for ON/OFF switch
def switch_on_off():
    if on_off_button["text"] == "Off":
        on_off_button.config(text="On", bg="green", relief=tk.SUNKEN)
    else:
        on_off_button.config(text="Off", bg="red", relief=tk.RAISED)


# Function placeholders for other button actions
def settings_action():
    if active_button == settings_button:
        return
    toggle_button(settings_button)


def draw_mode_action():
    if active_button == draw_button:
        return
    toggle_button(draw_button)


def image_mode_action():
    if active_button == image_button:
        return
    toggle_button(image_button)

    print("image pressed")
    # console = Console(PSoC)
    # console.test()


def camera_mode_action():
    if active_button == camera_button:
        return
    toggle_button(camera_button)
    print("camera pressed")

    cv = CV(PSoC, 0)
    cv.runCV()


def presets_mode_action():
    toggle_button(presets_button)


# Create the main window
root = tk.Tk()
root.title("Laser System Interface")
root.geometry("1024x640")
root.resizable(False, False)

# Top Frame for ON/OFF and SETTINGS buttons
top_frame = tk.Frame(root, width=1024, height=50, relief="solid", bd=1)
top_frame.pack(side="top", fill="x")

# ON/OFF switch button (default to OFF)
on_off_button = tk.Button(
    top_frame,
    text="Off",
    command=switch_on_off,
    width=20,
    height=2,
    bg="red",
    relief=tk.RAISED,
)
on_off_button.pack(side="left", padx=10, pady=10)

# SETTINGS button
settings_button = tk.Button(
    top_frame, text="Settings", command=settings_action, width=20, height=2
)
settings_button.pack(side="right", padx=10, pady=10)

# Left Frame for mode selection and settings
left_frame = tk.Frame(root, width=340, height=590, relief="solid", bd=1)
left_frame.pack(side="left", fill="y")

# Mode selection frame
mode_frame = tk.Frame(left_frame, width=340, height=150, relief="solid", bd=1)
mode_frame.pack(pady=10)

# Buttons for modes
draw_button = tk.Button(
    mode_frame, text="Draw", command=draw_mode_action, width=15, height=4
)
draw_button.grid(row=0, column=0, padx=5, pady=5)

image_button = tk.Button(
    mode_frame, text="Image", command=image_mode_action, width=15, height=4
)
image_button.grid(row=0, column=1, padx=5, pady=5)

camera_button = tk.Button(
    mode_frame, text="Camera", command=camera_mode_action, width=15, height=4
)
camera_button.grid(row=1, column=0, padx=5, pady=5)

presets_button = tk.Button(
    mode_frame, text="Presets", command=presets_mode_action, width=15, height=4
)
presets_button.grid(row=1, column=1, padx=5, pady=5)

# Mode settings frame
mode_settings_frame = tk.Frame(left_frame, width=340, height=300, relief="solid", bd=1)
mode_settings_frame.pack(pady=10)

mode_settings_label = tk.Label(
    mode_settings_frame, text="MODE SETTINGS", font=("Arial", 18)
)
mode_settings_label.pack(expand=True)

# General settings frame
general_settings_frame = tk.Frame(
    left_frame, width=340, height=120, relief="solid", bd=1
)
general_settings_frame.pack(pady=10)

general_settings_label = tk.Label(
    general_settings_frame, text="GENERAL SETTINGS", font=("Arial", 14)
)
general_settings_label.pack(expand=True)

# Right Frame for the Laser Preview Panel
right_frame = tk.Frame(root, width=680, height=590, relief="solid", bd=1)
right_frame.pack(side="right", fill="both", expand=True)

laser_preview_label = tk.Label(
    right_frame, text="LASER PREVIEW PANEL", font=("Arial", 24)
)
laser_preview_label.pack(expand=True)

# Run the application
root.mainloop()
