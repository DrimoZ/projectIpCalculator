from tkinter import *

<<<<<<< HEAD
var = Tk()

def leftclick(event):

    print("left")

def middleclick(event):

    print("middle")

def rightclick(event):

    print("right")

frame = Frame(var, width=300, height=250)

frame.bind("<Button-1>", leftclick)

frame.bind("<Button-2>", middleclick)

frame.bind("<Button-3>", rightclick)

frame.pack()

var.mainloop()
=======
def motion(event):
  print("Mouse position: (%s %s)" % (event.x, event.y))
  return

master = Tk()
whatever_you_do = "Whatever you do will be insignificant, but it is very important that you do it.\n(Mahatma Gandhi)"
msg = Message(master, text = whatever_you_do)
msg.config(bg='lightgreen', font=('times', 24, 'italic'))
msg.bind('<Motion>',motion)
msg.pack()
mainloop()
>>>>>>> 451f9e73629306eaf0a6ecb243ee9b1f8a9edea6
