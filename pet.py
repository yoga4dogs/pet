import random
import tkinter as tk
import ctypes

# set taskbar height/ground plane for yellowman
taskbar_size = 48

image_path = '.\\images\\yellowman\\'
sprite_size = 128
frame_count = 0

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
yellowman = new_yellowman()

def load_frames(action, file_name):
    for i in range(4):
        action.append(tk.PhotoImage(file=image_path+file_name,format = 'gif -index '+str(i)))
def load_frames_talk(action, file_name, index):
    action.append([])
    for i in range(4):
        action[index].append(tk.PhotoImage(file=image_path+file_name,format = 'gif -index '+str(i)))

# idle
idle = []
load_frames(idle, 'idle.gif')
# walk
walkL = []
load_frames(walkL, 'walkL.gif')
walkR = []
load_frames(walkR, 'walkR.gif')
# flip
fallL = []
load_frames(fallL, 'fallL.gif')
fallR = []
load_frames(fallR, 'fallR.gif')
# flip
flipL = []
load_frames(flipL, 'flipL.gif')
flipR = []
load_frames(flipR, 'flipR.gif')
# talk
talk = []
load_frames_talk(talk, 'talk_snake.gif', 0)
load_frames_talk(talk, 'talk_ghost.gif', 1)
load_frames_talk(talk, 'talk_grape.gif', 2)
load_frames_talk(talk, 'talk_potential.gif', 3)
load_frames_talk(talk, 'talk_neighbor.gif', 4)
load_frames_talk(talk, 'talk_revenge.gif', 5)
load_frames_talk(talk, 'talk_odo.gif', 6)
load_frames_talk(talk, 'talk_blue.gif', 7)
load_frames_talk(talk, 'talk_marbles.gif', 8)
load_frames_talk(talk, 'talk_laughing.gif', 9)

def update(frame_count, yellowman):
    if frame_count < 3:
        frame_count += 1
    else:
        frame_count = 0
    if yellowman.state == 'idle':
        frame = idle[frame_count]
        if random.randint(1,1000) == 1:
            select_topic(yellowman)
            yellowman.state = 'talk'
            frame_count = 0
        elif random.randint(1,25) == 1:
            yellowman.state = 'walk'
            frame_count = 0
    elif yellowman.state == 'walk':
        if yellowman.facing > 0:
            frame = walkR[frame_count]
        else:
            frame = walkL[frame_count]
        if random.randint(1,1000) == 1:
            select_topic(yellowman)
            yellowman.state = 'talk'
            frame_count = 0
        elif random.randint(1,100) == 1:
            yellowman.facing = 1-random.randint(0,1)*2
            yellowman.state = 'idle'
            frame_count = 0
        elif random.randint(1,50) == 1:
            yellowman.state = 'flip'
            frame_count = 0
        else:
            yellowman = move_x(yellowman)
    elif yellowman.state == 'flip':
        if yellowman.facing > 0:
            frame = flipR[frame_count]
        else:
            frame = flipL[frame_count]
        yellowman = move_x(yellowman)
        if frame_count == 3:
            yellowman.state = 'walk'
            frame_count = 0
    elif yellowman.state == 'held':
        if yellowman.facing > 0:
            frame = fallR[frame_count]
        else:
            frame = fallL[frame_count]
        pass
    elif yellowman.state == 'fall':
        if yellowman.facing > 0:
            frame = flipR[frame_count]
        else:
            frame = flipL[frame_count]
        if yellowman.y + yellowman.speed * 2 > bottom_bounds:
            yellowman.y = bottom_bounds
            yellowman.state = 'idle'
            frame_count = 0
        else:
            yellowman.y += yellowman.speed * 2
    elif yellowman.state == 'talk':
        frame = talk[yellowman.topic][frame_count]

    if yellowman.y > bottom_bounds:
        yellowman.y = bottom_bounds

    label.configure(image=frame)
    root.geometry('128x128+'+str(yellowman.x)+'+'+str(yellowman.y))
    root.after(update_loop_time,update, frame_count, yellowman)

def move_x(yellowman):
    if yellowman.state == 'flip':
        speed_mod = 4
    else:
        speed_mod = 1
    if yellowman.x + (yellowman.speed * yellowman.facing) > screen_size[0]-sprite_size:
        yellowman.x = screen_size[0]-sprite_size
        yellowman.facing *= -1
    elif yellowman.x + (yellowman.speed * yellowman.facing) < 0:
        yellowman.x = 0
        yellowman.facing *= -1
    else:
        yellowman.x += yellowman.speed * speed_mod * yellowman.facing
    return yellowman

def select_topic(yellowman):
    yellowman.topic = random.randint(0,len(talk)-1)

def click_handler(event):
    if yellowman.state == 'held':
        frame_count = 0
        yellowman.state = 'fall'
    elif yellowman.state == 'idle':
        yellowman.state = 'walk'
    elif yellowman.state == 'walk':
        yellowman.state = 'idle'
    elif yellowman.state == 'talk':
        frame_count = 0
        yellowman.state = 'idle'

def drag_handler(event):
    frame_count = 0
    yellowman.state = 'held'
    if yellowman.x < int(root.winfo_pointerx()-sprite_size/2):
        yellowman.facing = 1
    else:
        yellowman.facing = -1
    yellowman.x = int(root.winfo_pointerx()-sprite_size/2)
    yellowman.y = int(root.winfo_pointery()-sprite_size/4)

# init set label
label = tk.Label(root,bd=0,bg='black')
label.pack()

# set controls
label.bind("<B1-Motion>", drag_handler)
label.bind("<ButtonRelease>", click_handler)

root.after(update_loop_time,update, frame_count, yellowman)
root.mainloop()