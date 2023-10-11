import tkinter as tk

class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Changer de Frame")

        self.frames = {}
        for F in (PageOne, PageTwo):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageOne)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class PageOne(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bd=2, relief="solid")
        label = tk.Label(self, text="Cliquez sur cette page pour aller à la Page 2", font=("Helvetica", 14), fg="blue", cursor="hand2")
        label.pack(pady=10, padx=10)
        label.bind("<Button-1>", lambda event, cont=PageTwo: parent.show_frame(cont))

        self.bind("<Button-1>", lambda event, cont=PageTwo: parent.show_frame(cont))

class PageTwo(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bd=2, relief="solid")
        label = tk.Label(self, text="Cliquez sur cette page pour revenir à la Page 1", font=("Helvetica", 14), fg="blue", cursor="hand2")
        label.pack(pady=10, padx=10)
        label.bind("<Button-1>", lambda event, cont=PageOne: parent.show_frame(cont))

        self.bind("<Button-1>", lambda event, cont=PageOne: parent.show_frame(cont))

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
