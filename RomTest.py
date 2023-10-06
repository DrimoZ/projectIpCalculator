import tkinter as tk


def rand_func(eff=None, a=1, b=2, c=3):
    print(a + b + c)

root = tk.Tk()
root.bind("<Return>", lambda eff: rand_func(eff, a=10, b=20, c=30))

frame = tk.Frame(root)
frame.pack()

button = tk.Button(frame, text="click me",
                   command=lambda: rand_func(None, 1, 2, 3))
button.pack()

root.mainloop()