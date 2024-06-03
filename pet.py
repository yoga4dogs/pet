import random
import tkinter as tk
import ctypes

image_path = '.\\images\\yellowman\\'
sprite_size = 128
frame_count = 0

loop_interval = 125

user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
taskbar_size = 48
bottom_bounds = screen_size[1]-sprite_size-taskbar_size

class new_yellowman:
    def __init__(self):
        self.x = random.randrange(0, screen_size[0]-sprite_size)
    state = 'idle'
    facing = 1
    speed = 20
    y = bottom_bounds
    topic = 1
yellowman = new_yellowman()

# set window transparency
root = tk.Tk()
root.config(highlightbackground='black')
root.overrideredirect(True)
root.wm_attributes('-transparentcolor','black')
root.wm_attributes('-topmost', True)

# idle
idle = []
idle.append(tk.PhotoImage(file=image_path+'idle.gif',format = 'gif -index 0'))
idle.append(tk.PhotoImage(file=image_path+'idle.gif',format = 'gif -index 1'))
idle.append(tk.PhotoImage(file=image_path+'idle.gif',format = 'gif -index 2'))
idle.append(tk.PhotoImage(file=image_path+'idle.gif',format = 'gif -index 3'))
# walk
walkL = []
walkL.append(tk.PhotoImage(file=image_path+'walkL.gif',format = 'gif -index 0'))
walkL.append(tk.PhotoImage(file=image_path+'walkL.gif',format = 'gif -index 1'))
walkL.append(tk.PhotoImage(file=image_path+'walkL.gif',format = 'gif -index 2'))
walkL.append(tk.PhotoImage(file=image_path+'walkL.gif',format = 'gif -index 3'))
walkR = []
walkR.append(tk.PhotoImage(file=image_path+'walkR.gif',format = 'gif -index 0'))
walkR.append(tk.PhotoImage(file=image_path+'walkR.gif',format = 'gif -index 1'))
walkR.append(tk.PhotoImage(file=image_path+'walkR.gif',format = 'gif -index 2'))
walkR.append(tk.PhotoImage(file=image_path+'walkR.gif',format = 'gif -index 3'))
# flip
fallL = []
fallL.append(tk.PhotoImage(file=image_path+'fallL.gif',format = 'gif -index 0'))
fallL.append(tk.PhotoImage(file=image_path+'fallL.gif',format = 'gif -index 1'))
fallL.append(tk.PhotoImage(file=image_path+'fallL.gif',format = 'gif -index 2'))
fallL.append(tk.PhotoImage(file=image_path+'fallL.gif',format = 'gif -index 3'))
fallR = []
fallR.append(tk.PhotoImage(file=image_path+'fallR.gif',format = 'gif -index 0'))
fallR.append(tk.PhotoImage(file=image_path+'fallR.gif',format = 'gif -index 1'))
fallR.append(tk.PhotoImage(file=image_path+'fallR.gif',format = 'gif -index 2'))
fallR.append(tk.PhotoImage(file=image_path+'fallR.gif',format = 'gif -index 3'))
# flip
flipL = []
flipL.append(tk.PhotoImage(file=image_path+'flipL.gif',format = 'gif -index 0'))
flipL.append(tk.PhotoImage(file=image_path+'flipL.gif',format = 'gif -index 1'))
flipL.append(tk.PhotoImage(file=image_path+'flipL.gif',format = 'gif -index 2'))
flipL.append(tk.PhotoImage(file=image_path+'flipL.gif',format = 'gif -index 3'))
flipR = []
flipR.append(tk.PhotoImage(file=image_path+'flipR.gif',format = 'gif -index 0'))
flipR.append(tk.PhotoImage(file=image_path+'flipR.gif',format = 'gif -index 1'))
flipR.append(tk.PhotoImage(file=image_path+'flipR.gif',format = 'gif -index 2'))
flipR.append(tk.PhotoImage(file=image_path+'flipR.gif',format = 'gif -index 3'))
# talk
talk = [[], []]
talk[0].append(tk.PhotoImage(file=image_path+'talk_snake.gif',format = 'gif -index 0'))
talk[0].append(tk.PhotoImage(file=image_path+'talk_snake.gif',format = 'gif -index 1'))
talk[0].append(tk.PhotoImage(file=image_path+'talk_snake.gif',format = 'gif -index 2'))
talk[0].append(tk.PhotoImage(file=image_path+'talk_snake.gif',format = 'gif -index 3'))
talk[1].append(tk.PhotoImage(file=image_path+'talk_ghost.gif',format = 'gif -index 0'))
talk[1].append(tk.PhotoImage(file=image_path+'talk_ghost.gif',format = 'gif -index 1'))
talk[1].append(tk.PhotoImage(file=image_path+'talk_ghost.gif',format = 'gif -index 2'))
talk[1].append(tk.PhotoImage(file=image_path+'talk_ghost.gif',format = 'gif -index 3'))

def update(frame_count, yellowman):
    if frame_count < 3:
        frame_count += 1
    else:
        frame_count = 0
    if yellowman.state == 'idle':
        frame = idle[frame_count]
        if random.randint(1,500) == 1:
            select_topic(yellowman)
            yellowman.state = 'talk'
            frame_count = 0
        elif random.randint(1,20) == 1:
            yellowman.state = 'walk'
            frame_count = 0
    elif yellowman.state == 'walk':
        if yellowman.facing > 0:
            frame = walkR[frame_count]
        else:
            frame = walkL[frame_count]
        if random.randint(1,100) == 1:
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
    root.after(loop_interval,update, frame_count, yellowman)

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
    elif yellowman.state == 'talk':
        frame_count = 0
        yellowman.state = 'idle'
    else:
        select_topic(yellowman)
        yellowman.state = 'talk'

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

root.after(loop_interval,update, frame_count, yellowman)
root.mainloop()