import random
import tkinter as tk
import ctypes

# set taskbar height/ground plane for yellowman
taskbar_size = 40

image_path = '.\\images\\yellowman\\'
sprite_size = 128
anim_frame_length = 4

update_loop_time = 125

user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
bottom_bounds = screen_size[1]-sprite_size-taskbar_size

# set window transparency
root = tk.Tk()
root.config(highlightbackground='black')
root.overrideredirect(True)
root.wm_attributes('-transparentcolor','black')
root.wm_attributes('-topmost', True)

class new_yellowman:
    def __init__(self):
        self.x = random.randrange(0, screen_size[0]-sprite_size)
    state = 'idle'
    facing = 1
    speed = 20
    y = bottom_bounds
    topic = 1
    frame_counter = 0
yellowman = new_yellowman()

def load_frames(action, file_name, nested):
    if nested:
        action.append([])
        index = len(action) - 1
        for i in range(anim_frame_length):
            action[index].append(tk.PhotoImage(file=image_path+file_name,format = 'gif -index '+str(i)))
    else:
        for i in range(anim_frame_length):
            action.append(tk.PhotoImage(file=image_path+file_name,format = 'gif -index '+str(i)))

# idle
idle = []
load_frames(idle, 'idle.gif', False)
# walk
walk = [[], []]
load_frames(walk[0], 'walkL.gif', False)
load_frames(walk[1], 'walkR.gif', False)
# flip
fall = [[], []]
load_frames(fall[0], 'fallL.gif', False)
load_frames(fall[1], 'fallR.gif', False)
# flip
flip = [[], []]
load_frames(flip[0], 'flipL.gif', False)
load_frames(flip[1], 'flipR.gif', False)
# talk
talk = []
load_frames(talk, 'talk_snake.gif', True)
load_frames(talk, 'talk_ghost.gif', True)
load_frames(talk, 'talk_grape.gif', True)
load_frames(talk, 'talk_potential.gif', True)
load_frames(talk, 'talk_neighbor.gif', True)
load_frames(talk, 'talk_revenge.gif', True)
load_frames(talk, 'talk_odo.gif', True)
load_frames(talk, 'talk_blue.gif', True)
load_frames(talk, 'talk_marbles.gif', True)
load_frames(talk, 'talk_laughing.gif', True)

def update(yellowman):
    if yellowman.frame_counter < anim_frame_length - 1:
        yellowman.frame_counter += 1
    else:
        yellowman.frame_counter = 0
    if yellowman.state == 'idle':
        frame = idle[yellowman.frame_counter]
        if random.randint(1,1000) == 1:
            select_topic(yellowman)
            yellowman.state = 'talk'
            yellowman.frame_counter = 0
        elif random.randint(1,25) == 1:
            yellowman.facing = random.randint(0,1)
            yellowman.state = 'walk'
            yellowman.frame_counter = 0
    elif yellowman.state == 'walk':
        frame = walk[yellowman.facing][yellowman.frame_counter]
        if random.randint(1,1000) == 1:
            select_topic(yellowman)
            yellowman.state = 'talk'
            yellowman.frame_counter = 0
        elif random.randint(1,100) == 1:
            yellowman.state = 'idle'
            yellowman.frame_counter = 0
        elif random.randint(1,50) == 1:
            yellowman.state = 'flip'
            yellowman.frame_counter = 0
        else:
            yellowman = move_x(yellowman)
    elif yellowman.state == 'flip':
        frame = flip[yellowman.facing][yellowman.frame_counter]
        yellowman = move_x(yellowman)
        if yellowman.frame_counter == 3:
            yellowman.state = 'walk'
            yellowman.frame_counter = 0
    elif yellowman.state == 'held':
        frame = fall[yellowman.facing][yellowman.frame_counter]
        pass
    elif yellowman.state == 'fall':
        frame = flip[yellowman.facing][yellowman.frame_counter]
        if yellowman.y + yellowman.speed * 2 > bottom_bounds:
            yellowman.y = bottom_bounds
            yellowman.state = 'idle'
            yellowman.frame_counter = 0
        else:
            yellowman.y += yellowman.speed * 2
    elif yellowman.state == 'talk':
        frame = talk[yellowman.topic][yellowman.frame_counter]

    if yellowman.y > bottom_bounds:
        yellowman.y = bottom_bounds

    label.configure(image=frame)
    root.geometry('128x128+'+str(yellowman.x)+'+'+str(yellowman.y))
    root.after(update_loop_time,update, yellowman)

def move_x(yellowman):
    if yellowman.state == 'flip':
        speed_mod = 4
    else:
        speed_mod = 1
    if yellowman.facing == 1:
        dir = 1
    else:
        dir = -1
    if yellowman.x + (yellowman.speed * speed_mod * dir) > screen_size[0]-sprite_size:
        yellowman.x = screen_size[0]-sprite_size
        yellowman.facing = 1 - yellowman.facing
    elif yellowman.x + (yellowman.speed * speed_mod * dir) < 0:
        yellowman.x = 0
        yellowman.facing = 1 - yellowman.facing
    else:
        yellowman.x += yellowman.speed * speed_mod * dir
    return yellowman

def select_topic(yellowman):
    yellowman.topic = random.randint(0,len(talk)-1)

def click_handler(event):
    if yellowman.state == 'held':
        yellowman.state = 'fall'
        yellowman.frame_counter = 0
    elif yellowman.state == 'idle':
        yellowman.state = 'walk'
        yellowman.frame_counter = 0
    elif yellowman.state == 'walk':
        yellowman.state = 'idle'
        yellowman.frame_counter = 0
    elif yellowman.state == 'talk':
        yellowman.state = 'idle'
        yellowman.frame_counter = 0

def drag_handler(event):
    yellowman.state = 'held'
    yellowman.frame_counter = 0
    if yellowman.x < int(root.winfo_pointerx()-sprite_size/2):
        yellowman.facing = 1
    else:
        yellowman.facing = 0
    yellowman.x = int(root.winfo_pointerx()-sprite_size/2)
    yellowman.y = int(root.winfo_pointery()-sprite_size/4)

# init set label
label = tk.Label(root,bd=0,bg='black')
label.pack()

# set controls
label.bind("<B1-Motion>", drag_handler)
label.bind("<ButtonRelease>", click_handler)

root.after(update_loop_time,update, yellowman)
root.mainloop()