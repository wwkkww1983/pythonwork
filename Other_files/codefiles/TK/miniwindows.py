import tkinter as tk

window = tk.Tk()
window.title('Learning Python')
window.geometry('500x200')


var=tk.StringVar()
l=tk.Label(window,textvariable=var,bg='green',font=('Arial',16),width=20,height=2)
l.pack()

on_hit = False
def hit_me():
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('You hit me!')
    else:
        on_hit = False
        var.set('')

b = tk.Button(window,text='click me',bg='yellow',font=('Arial',16),width=20,height=2,command=hit_me)
b.pack()

window.mainloop()
