from ast import Try
import sys
import threading
import time
import tkinter as tk

from pong6 import Pong
from PSoCBridge import PSoCBridge
from CVCam import CV
from console import Console
from flappy_bird import FlappyBird


# TODO: change this to false if PSoC is connected.
# If true, simulates the laser path with a GUI

FLIP_X, FLIP_Y = True, True

try:
    PSoC = PSoCBridge(ignoreCOM=False, flipX=FLIP_X, flipY=FLIP_Y)
except Exception as e:
    PSoC = PSoCBridge(ignoreCOM=True, flipX=FLIP_X, flipY=FLIP_Y)

# Global variable to keep track of the currently active button (for modes)
active_button = None
preview_drawing = True
camera: int = 0
running_CV = None
featureThread: threading.Thread


def run_in_thread(function):
    global featureThread
    featureThread = threading.Thread(target=function)
    featureThread.start()

# Function to toggle button states for modes
def change_mode(button):
    global active_button

    if active_button and active_button != button:
        active_button.config(relief=tk.RAISED, bg="SystemButtonFace")

    if button["relief"] == tk.SUNKEN:
        button.config(relief=tk.RAISED, bg="SystemButtonFace")
        active_button = None
    else:
        button.config(relief=tk.SUNKEN, bg="grey")
        active_button = button

    # turn off all modes
    global running_CV
    if running_CV and active_button != camera_button:
        running_CV.stop()


# Function placeholders for other button actions
def shutdown_action():
    change_mode(shutdown_button)
    if running_CV is not None: running_CV.stop()
    root.destroy()
    sys.exit()

def settings_action():
    if active_button == settings_button:
        return
    change_mode(settings_button)


def draw_mode_action():
    if active_button == draw_button:
        return
    change_mode(draw_button)


def image_mode_action():
    if active_button == image_button:
        return
    change_mode(image_button)

    print("image pressed")
    console = Console(PSoC)

    run_in_thread(console.startConsole)


def runCV():
    global running_CV
    if running_CV is not None:
        running_CV.stop()
    running_CV = CV(PSoC, camera)

    try:
        running_CV.runCV()
    except Exception as e:
        write_error(e)


def camera_mode_action():
    if (
        active_button == camera_button
        and running_CV is not None
        and running_CV.camera == selected_camera
    ):
        return
    change_mode(camera_button)

    thread = threading.Thread(target=runCV)
    thread.start()


def flappy_action():
    change_mode(presets_button)
    fb = FlappyBird(PSoC)
    run_in_thread(fb.start_flappy_bird)

def pong_action():
    change_mode(presets_button)
    fb = Pong(PSoC)
    PSoC.flipX = True
    run_in_thread(fb.start_pong_game)


# Create the main window
root = tk.Tk()
root.title("Laser System Interface")
root.geometry("1024x640")
root.protocol("WM_DELETE_WINDOW", shutdown_action)
root.resizable(True, True)

# Top Frame for ON/OFF and SETTINGS buttons
top_frame = tk.Frame(root, width=1024, height=50, relief="solid", bd=1)
top_frame.pack(side="top", fill="x")


def write_error(error_message):
    print(error_message)
    error_frame = tk.Frame(
        root,
        width=1024,
        height=50,
        relief="solid",
        bd=1,
        highlightbackground="red",
        highlightthickness=4,
    )
    error_frame.place(x=100, y=100, width=800, height=500)
    error_label = tk.Label(
        error_frame,
        text=str(error_message)[0:100],
        font=("Arial", 40),
        foreground="red",
        wraplength=800,
    )
    error_label.pack(padx=10, pady=10)

    close_button = tk.Button(
        error_frame,
        text="OK",
        font=("Arial", 32),
        background="red",
        command=error_frame.destroy,
    )
    close_button.pack(side="bottom", pady=10)


# Function for FLIP OUTPUT
flip_output_state = 0
def flip_output_cycle():
    global flip_output_state
    if flip_output_state == 0:
        flip_output_button.config(text="FLIPPED X", bg="yellow", relief=tk.SUNKEN)
        flip_output_state = 1
        PSoC.flipX, PSoC.flipY = True, False
    elif flip_output_state == 1:
        flip_output_button.config(text="FLIPPED Y", bg="cyan", relief=tk.SUNKEN)
        flip_output_state = 2
        PSoC.flipX, PSoC.flipY = False, True
    elif flip_output_state == 2:
        flip_output_button.config(text="FLIPPED X & Y", bg="green", relief=tk.GROOVE)
        flip_output_state = 3
        PSoC.flipX, PSoC.flipY = True, True
    elif flip_output_state == 3:
        flip_output_button.config(text="FLIPPED NONE", bg="grey", relief=tk.RAISED)
        flip_output_state = 0
        PSoC.flipX, PSoC.flipY = False, False

# FLIP OUTPUT BUTTON
flip_output_button = tk.Button(
    top_frame,
    text="FLIP IMAGE",
    command=flip_output_cycle,
    width=20,
    height=2,
    bg="orange",
    relief=tk.RAISED,
)
flip_output_button.pack(side="left", padx= 10, pady=10)

# SHUTDOWN button
shutdown_button = tk.Button(
    top_frame,
    text="SHUTDOWN",
    command=shutdown_action,
    width=20,
    height=2,
    background="red",
    foreground="white",
)
#shutdown_button.pack(side="right", padx=10, pady=10)

# SETTINGS button
settings_button = tk.Button(
    top_frame,
    text="Settings",
    command=settings_action,
    width=20,
    height=2,
    background="grey",
)
settings_button.pack(side="left", padx=10, pady=10)

# Left Frame for mode selection and settings
left_frame = tk.Frame(root, width=520, height=590, relief="solid", bd=1)
left_frame.pack(side="left", fill="y")

# Mode selection frame
mode_frame = tk.Frame(left_frame, width=520, height=150, relief="solid", bd=1)
mode_frame.pack(pady=10)


# camera select
def on_camera_change(event):
    selected_option = selected_camera.get()
    print(f"Selected Camera: {selected_option}")
    global camera
    camera = int(selected_option)
    camera_mode_action()  # rerun CV
    change_mode(camera_button)


frame = tk.Frame(mode_frame)
frame.pack()

label = tk.Label(frame, text="Camera:")
label.pack(side="left")

camera_options = ["0", "1", "2", "3"]
selected_camera = tk.StringVar(mode_frame)
selected_camera.set(camera_options[0])  # Set the initial value

dropdown = tk.OptionMenu(
    frame, selected_camera, *camera_options, command=on_camera_change
)
dropdown.pack(side="left")
frame.grid(row=3, column=0, padx=5, pady=5)

# Buttons for modes
draw_button = tk.Button(
    mode_frame, text="DRAW", command=draw_mode_action, width=15, height=4
)
draw_button.grid(row=1, column=0, padx=5, pady=5)

image_button = tk.Button(
    mode_frame, text="TESTS", command=image_mode_action, width=15, height=4
)
image_button.grid(row=1, column=1, padx=5, pady=5)

camera_button = tk.Button(
    mode_frame, text="COMPUTER VISION", command=camera_mode_action, width=15, height=4
)
camera_button.grid(row=2, column=0, padx=5, pady=5)

presets_button = tk.Button(
    mode_frame, text="GAMES", command=pong_action, width=15, height=4
)
presets_button.grid(row=2, column=1, padx=5, pady=5)

# Mode settings frame
mode_settings_frame = tk.Frame(left_frame, width=340, height=300, relief="solid", bd=1)
mode_settings_frame.pack(pady=10)

mode_settings_label = tk.Label(
    mode_settings_frame, text="MODE SETTINGS", font=("Arial", 18)
)
mode_settings_label.pack(expand=True)

# General settings frame
general_settings_frame = tk.Frame(
    left_frame, width=520, height=120, relief="solid", bd=1
)
general_settings_frame.pack(pady=10)

general_settings_label = tk.Label(
    general_settings_frame, text="GENERAL SETTINGS", font=("Arial", 14)
)
general_settings_label.pack(expand=True)

# Right Frame for the Laser Preview Panel
right_frame = tk.Frame(root, width=520, height=520, relief="solid", bd=1, bg="black")
right_frame.pack(side="right", fill="both", expand=True)

preview_controls = tk.Frame(right_frame, width=520, height=520, relief="solid", bd=1, bg="black")
preview_controls.pack(expand=True)

laser_preview_label = tk.Label(
    preview_controls,
    text="LASER PREVIEW PANEL",
    font=("Arial", 24),
    background="black",
    foreground="white",
)
laser_preview_label.grid(column=1, row=0, padx=10, pady=0)

# Function for ON/OFF PREVIEW
def path_preview_toggle():
    global preview_drawing
    if path_preview_button["text"] == "PATH PREVIEW: OFF":
        path_preview_button.config(text="PATH PREVIEW: ON", bg="green", relief=tk.SUNKEN)
        preview_drawing = True
    else:
        path_preview_button.config(text="PATH PREVIEW: OFF", bg="red", relief=tk.RAISED)
        preview_drawing = False

# ON/OFF switch button (default to OFF)
path_preview_button = tk.Button(
    preview_controls,
    text="PATH PREVIEW: ON",
    command=path_preview_toggle,
    width=20,
    height=2,
    bg="green",
    relief=tk.RAISED,
)
path_preview_button.grid(column=0, row=0, padx=10, pady=0)

# Function for CV CAMERA PREVIEW
preview_camera_button_state = 0

def camera_preview_cycle():
    global preview_camera_button_state
    if preview_camera_button_state == 0:
        preview_camera_button.config(text="CV PREVIEW: ON", bg="yellow", relief=tk.SUNKEN)
        preview_camera_button_state = 1
    elif preview_camera_button_state == 1:
        preview_camera_button.config(text="CAMERA PREVIEW", bg="cyan", relief=tk.SUNKEN)
        preview_camera_button_state = 2
    elif preview_camera_button_state == 2:
        preview_camera_button.config(text="CV PREVIEW: OFF", bg="light grey", relief=tk.RAISED)
        preview_camera_button_state = 0

    if running_CV is not None:
        running_CV.camera_preview(preview_camera_button_state)  # Pause the camera preview

# CV cycle switch button (default to OFF)
preview_camera_button = tk.Button(
    preview_controls,
    text="CV PREVIEW: OFF",
    command=camera_preview_cycle,
    width=20,
    height=2,
    bg="red",
    relief=tk.RAISED,
)
preview_camera_button.grid(column=2, row=0, padx=10, pady=0)

# Create a canvas for drawing
canvas = tk.Canvas(
    right_frame,
    width=520,
    height=520,
    bg="black",
    highlightbackground="#222222",
    highlightthickness=1,
)
canvas.pack(pady=10)


# Function to draw a line between two points if the laser is on
def draw_line(x1, y1, x2, y2, color):
    if x1 == x2 and y1 == y2:
        return  # Prevent drawing lines to the same point
    canvas.create_line(x1, y1, x2, y2, fill=color)


# Function to process the data stream and draw lines
def draw_data(data_stream):
    canvas.delete("all")
    data_stream = data_stream
    prev_x, prev_y = None, None
    n =  max(0, len(data_stream))
    if n % 3 != 0 or n == 0:
        return

    for i in range(0, n-3, 3):  
        xpos, ypos, color = data_stream[i], data_stream[i + 1], data_stream[i + 2]

        if prev_x is not None and prev_y is not None:
            if color > 0:  # Laser is on
                colorStr = "#"
                colorStr += "ff" if ((color >> 6) & 0b11) > 0 else "00"
                colorStr += "ff" if ((color >> 4) & 0b11) > 0 else "00"
                colorStr += "ff" if ((color >> 2) & 0b11) > 0 else "00"
            else:
                colorStr = "#222222"

            draw_line(5 + prev_x * 2, 5 + prev_y * 2, 5 + xpos * 2, 5 + ypos * 2, colorStr)
        prev_x, prev_y = xpos, ypos

    xpos, ypos, color = data_stream[0], data_stream[1], data_stream[2]
    draw_line(5 + prev_x * 2, 5 + prev_y * 2, 5 + xpos * 2, 5 + ypos * 2, "#222222")


# Example data stream (continuous array)
data_stream = [
    0,
    100,
    255,
    10,
    110,
    0,
    20,
    120,
    255,
    30,
    130,
    0,
    40,
    140,
    255,
    50,
    150,
    0,
    60,
    160,
    255,
]


# Asynchronous function to process the data stream
def update_preview():

    if preview_drawing:
        draw_data(PSoC.get_data_stream())
    # Add a delay if needed to control the processing rate
    time.sleep(0.1)
    root.after(50, update_preview)


def GUI_worker():
    root.after(0, update_preview)


# Start the asynchronous task in a separate thread
GUI_update_thread = threading.Thread(target=GUI_worker)
GUI_update_thread.start()

# Start the Tkinter event loop
try:
    root.mainloop()
except KeyboardInterrupt:
    print("KeyboardInterrupt received, exiting...")
    shutdown_action()

GUI_update_thread.join()
