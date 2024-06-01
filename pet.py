import random
import tkinter as tk
from PIL import Image, ImageTk
import ctypes

user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
taskbar_size = 48

image_path = '.\\images\\'
sprite_size = 128
facing = 1

speed = 20
count = 0

x = random.randrange(0, screen_size[0]-sprite_size)
y = screen_size[1]-sprite_size-taskbar_size

window = tk.Tk()
window.config(highlightbackground='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','black')
window.wm_attributes('-topmost', True)

#call buddy's action .gif to an array
walk = []
walk.append(tk.PhotoImage(file=image_path+'yellowman\\walk.gif',format = 'gif -index 0'))
walk.append(tk.PhotoImage(file=image_path+'yellowman\\walk.gif',format = 'gif -index 1'))
walk.append(tk.PhotoImage(file=image_path+'yellowman\\walk.gif',format = 'gif -index 2'))
walk.append(tk.PhotoImage(file=image_path+'yellowman\\walk.gif',format = 'gif -index 3'))

def update(count, x, facing):
    walk_frame = walk[count]
    if count < 3:
        count += 1
    else:
        count = 0

    if x < screen_size[0]-sprite_size and facing == 1:
        x += speed
    elif x > screen_size[0]-sprite_size and facing == 1:
        facing *= -1
    elif x > 0 and facing == -1:
        x -= speed
    elif x < 0:
        facing *= -1

    window.geometry('128x128+'+str(x)+'+'+str(y))
        
    label.configure(image=walk_frame)

    window.after(125,update, count, x, facing)

label = tk.Label(window,bd=0,bg='black')
label.configure(image=walk[0])
label.pack()
window.geometry('128x128+'+str(x)+'+'+str(y))
window.after(1,update, count, x, facing)
window.mainloop()