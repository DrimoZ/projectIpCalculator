from tkinter import *


root = Tk()
root.state('zoomed')
frm = Frame(root)
frm.grid()
lab = Label(frm, text="Hello World!").grid(column=0, row=0)
but = Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

root.mainloop()