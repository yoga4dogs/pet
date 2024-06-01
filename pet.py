import random
import tkinter as tk
import ctypes

image_path = '.\\images\\'
sprite_size = 128

user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
taskbar_size = 48
bottom_bounds = screen_size[1]-sprite_size-taskbar_size

count = 0

class new_yellowman:
    def __init__(self):
        self.x = random.randrange(0, screen_size[0]-sprite_size)
    state = 'walk'
    facing = 1
    speed = 20
    y = bottom_bounds

yellowman = new_yellowman()

root = tk.Tk()
root.config(highlightbackground='black')
root.overrideredirect(True)
root.wm_attributes('-transparentcolor','black')
root.wm_attributes('-topmost', True)

idle = []
idle.append(tk.PhotoImage(file=image_path+'yellowman\\idle.gif',format = 'gif -index 0'))
idle.append(tk.PhotoImage(file=image_path+'yellowman\\idle.gif',format = 'gif -index 1'))
idle.append(tk.PhotoImage(file=image_path+'yellowman\\idle.gif',format = 'gif -index 2'))
idle.append(tk.PhotoImage(file=image_path+'yellowman\\idle.gif',format = 'gif -index 3'))
walkL = []
walkL.append(tk.PhotoImage(file=image_path+'yellowman\\walkL.gif',format = 'gif -index 0'))
walkL.append(tk.PhotoImage(file=image_path+'yellowman\\walkL.gif',format = 'gif -index 1'))
walkL.append(tk.PhotoImage(file=image_path+'yellowman\\walkL.gif',format = 'gif -index 2'))
walkL.append(tk.PhotoImage(file=image_path+'yellowman\\walkL.gif',format = 'gif -index 3'))
walkR = []
walkR.append(tk.PhotoImage(file=image_path+'yellowman\\walkR.gif',format = 'gif -index 0'))
walkR.append(tk.PhotoImage(file=image_path+'yellowman\\walkR.gif',format = 'gif -index 1'))
walkR.append(tk.PhotoImage(file=image_path+'yellowman\\walkR.gif',format = 'gif -index 2'))
walkR.append(tk.PhotoImage(file=image_path+'yellowman\\walkR.gif',format = 'gif -index 3'))
fallL = []
fallL.append(tk.PhotoImage(file=image_path+'yellowman\\fallL.gif',format = 'gif -index 0'))
fallL.append(tk.PhotoImage(file=image_path+'yellowman\\fallL.gif',format = 'gif -index 1'))
fallL.append(tk.PhotoImage(file=image_path+'yellowman\\fallL.gif',format = 'gif -index 2'))
fallL.append(tk.PhotoImage(file=image_path+'yellowman\\fallL.gif',format = 'gif -index 3'))
fallR = []
fallR.append(tk.PhotoImage(file=image_path+'yellowman\\fallR.gif',format = 'gif -index 0'))
fallR.append(tk.PhotoImage(file=image_path+'yellowman\\fallR.gif',format = 'gif -index 1'))
fallR.append(tk.PhotoImage(file=image_path+'yellowman\\fallR.gif',format = 'gif -index 2'))
fallR.append(tk.PhotoImage(file=image_path+'yellowman\\fallR.gif',format = 'gif -index 3'))
flipL = []
flipL.append(tk.PhotoImage(file=image_path+'yellowman\\flipL.gif',format = 'gif -index 0'))
flipL.append(tk.PhotoImage(file=image_path+'yellowman\\flipL.gif',format = 'gif -index 1'))
flipL.append(tk.PhotoImage(file=image_path+'yellowman\\flipL.gif',format = 'gif -index 2'))
flipL.append(tk.PhotoImage(file=image_path+'yellowman\\flipL.gif',format = 'gif -index 3'))
flipR = []
flipR.append(tk.PhotoImage(file=image_path+'yellowman\\flipR.gif',format = 'gif -index 0'))
flipR.append(tk.PhotoImage(file=image_path+'yellowman\\flipR.gif',format = 'gif -index 1'))
flipR.append(tk.PhotoImage(file=image_path+'yellowman\\flipR.gif',format = 'gif -index 2'))
flipR.append(tk.PhotoImage(file=image_path+'yellowman\\flipR.gif',format = 'gif -index 3'))

def update(count, yellowman):
    if count < 3:
        count += 1
    else:
        count = 0
    if yellowman.state == 'walk':
        if yellowman.facing > 0:
            frame = walkR[count]
        else:
            frame = walkL[count]
            
        if random.randint(1,100) == 1:
            yellowman.facing = 1-random.randint(0,1)*2
            yellowman.state = 'idle'
            count = 0
        elif random.randint(1,50) == 1:
            yellowman.state = 'flip'
            count = 0
        else:
            yellowman = move_x(yellowman)
    elif yellowman.state == 'flip':
        if yellowman.facing > 0:
            frame = flipR[count]
        else:
            frame = flipL[count]
        yellowman = move_x(yellowman)
        if count == 3:
            yellowman.state = 'walk'
            count = 0
    elif yellowman.state == 'held':
        if yellowman.facing > 0:
            frame = fallR[count]
        else:
            frame = fallL[count]
        pass
    elif yellowman.state == 'fall':
        if yellowman.facing > 0:
            frame = flipR[count]
        else:
            frame = flipL[count]
        if yellowman.y + yellowman.speed * 2 > bottom_bounds:
            yellowman.y = bottom_bounds
            yellowman.state = 'idle'
            count = 0
        else:
            yellowman.y += yellowman.speed * 2
    elif yellowman.state == 'idle':
        frame = idle[count]
        if random.randint(1,20) == 1:
            yellowman.state = 'walk'
            count = 0

    if yellowman.y > bottom_bounds:
        yellowman.y = bottom_bounds

    label.configure(image=frame)
    root.geometry('128x128+'+str(yellowman.x)+'+'+str(yellowman.y))
    root.after(125,update, count, yellowman)

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

def click_handler(event):
    if yellowman.state == 'held':
        count = 0
        yellowman.state = 'fall'
    # elif yellowman.state == 'walk':
    #     count = 0
    #     yellowman.state = 'flip'

def drag_handler(event):
    count = 0
    yellowman.state = 'held'
    if yellowman.x < int(root.winfo_pointerx()-sprite_size/2):
        yellowman.facing = 1
    else:
        yellowman.facing = -1
    yellowman.x = int(root.winfo_pointerx()-sprite_size/2)
    yellowman.y = int(root.winfo_pointery()-sprite_size/4)


label = tk.Label(root,bd=0,bg='black')
label.configure(image=walkR[0])
label.pack()

label.bind("<B1-Motion>", drag_handler)
label.bind("<ButtonRelease>", click_handler)

root.geometry('128x128+'+str(yellowman.x)+'+'+str(yellowman.y))
root.after(1,update, count, yellowman)
root.mainloop()