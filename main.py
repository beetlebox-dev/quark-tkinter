import tkinter as tk
import time
import math
import random
import triangle


FRAME_RATE = 1 / 24  # seconds
BLINK_RATE = 2  # in frames  # Applies when action == 'blink'
SPEED_FACTOR = 0.6

BLACK = "#000000"
WHITE = "#FFFFFF"

# In tests I've seen the Replit tkinter area height remain a constant 447 pixels, and width ranging from 341 on mobile to 704 on desktop. should remove 30 pixels or so from height to account for window title area.
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Creates random triangles using points within these xy coordinates.
BOUND_SPAN = 40  # pixels
UPPER_LEFT_BOUND = [int((WINDOW_WIDTH - BOUND_SPAN) / 2), int((WINDOW_HEIGHT - BOUND_SPAN) / 2)]
LOWER_RIGHT_BOUND = [int((WINDOW_WIDTH + BOUND_SPAN) / 2), int((WINDOW_HEIGHT + BOUND_SPAN) / 2)]


def button_func():
    global button_pressed
    button_pressed = True


def change_animation_params():

    global reset_timestamp
    global first_frame
    global button_pressed
    global action
    global move_distance
    global num_triangles
    global color
    global triangles

    first_frame = time.time()
    button_pressed = False

    if action == 'blink':
        reset_timestamp = time.time() + 8
        action = 'stretch'
        move_distance = 'rand'
        num_triangles = 111
        color = random.choice(['rand-same', 'rand-same', 'rand-diff'])

    else:
        reset_timestamp = math.inf
        action = 'blink'
        move_distance = 0
        num_triangles = 1
        # color = random.choice(['rand-same', 'rand-diff'])
        color = random.choice(['rand-same', 'rand-same', 'rand-blink'])

    if color == "rand-same":
        # Assign all triangles the same consistent random color.
        color = triangle.rand_hex_pure_hue()

    triangles = []
    for n in range(num_triangles):
        if color == "rand-diff":
            # Assign each triangle a different consistent random color.
            n_color = triangle.rand_hex_pure_hue()
        else:
            n_color = color
        triangles.append(triangle.Triangle(UPPER_LEFT_BOUND, LOWER_RIGHT_BOUND, action, move_distance=move_distance,
                                           color=n_color))


window = tk.Tk()
window.title("Volatile 3-gons")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BLACK)
canvas.pack()
button = tk.Button(text="change", command=button_func, bg=WHITE, fg=BLACK, activebackground=BLACK, activeforeground=WHITE, bd=0)
button.place(width=80, x=15, height=25, y=15, anchor="nw")

first_frame = time.time()
prev_frame = time.time()
reset_timestamp = 0
button_pressed = True
action = "stretch"  # rotate, stretch, blink
move_distance = None
num_triangles = None
color = None  # hex-string ("#FFFFFF" is white) or color-name-string,
# or "rand-same" (all shapes the same consistent random color),
# or "rand-diff" (each shape a different consistent random color),
# or "rand-blink" (each blink changes each shape's color)
triangles = None


while True:
    if button_pressed or reset_timestamp < time.time():
        change_animation_params()
    if action != "blink" or time.time() - prev_frame >= BLINK_RATE * FRAME_RATE:
        ngons = []
        for n in triangles:
            vertices = n.render((first_frame - time.time()) * SPEED_FACTOR / FRAME_RATE)
            if n.color == "rand-blink":
                frame_n_color = triangle.rand_hex_pure_hue()
            else:
                frame_n_color = n.color
            n_ngon = canvas.create_polygon(vertices, fill=frame_n_color)
            ngons.append(n_ngon)
        window.update()
        prev_frame = time.time()
        for ngon in ngons:
            canvas.delete(ngon)
    time.sleep(FRAME_RATE)
