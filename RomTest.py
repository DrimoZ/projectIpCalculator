# from tkinter import *
import ipaddress

# root = Tk()
# root.state('zoomed')
# frm = Frame(root)
# frm.grid()
# lab = Label(frm, text="Hello World!").grid(column=0, row=0)
# but = Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

# root.mainloop()
ip = "1006401"
try:
    ip_object = ipaddress.ip_address(ip)
    print(f"The IP address {ip_object} is valid.")
except ValueError:
    print("The IP address '{ip}' is not valid")