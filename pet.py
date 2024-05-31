import random
import tkinter as tk

impath = '.\\images\\'
impath += 'stupid_cat.png'

x = 500
y = 1080-256

window = tk.Tk()
window.config(highlightbackground='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','black')
window.wm_attributes('-topmost', True)

idle = [tk.PhotoImage(file=impath,format = 'png')]

label = tk.Label(window,bd=0,bg='black')
label.configure(image=idle)
label.pack()

window.geometry('128x128+'+str(x)+'+'+str(y))
window.mainloop()