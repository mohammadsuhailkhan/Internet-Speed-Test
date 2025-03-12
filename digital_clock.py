import tkinter as tk
import time
win=tk.Tk()
win.title("DIGITAL CLOCK")
label=tk.Label(win,font=('calibri',40,'bold'),bg='black', fg='white')
label.pack()
def update_time():
    current_time=time.strftime('%H:%M:%S')
    label.config(text=current_time)
    label.after(1000, update_time)
update_time()
win.mainloop()
