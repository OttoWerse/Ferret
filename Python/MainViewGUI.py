from tkinter import *
from tkinter.ttk import *

dropdown = ["Kill", "Me", "Please"]

root = Tk()

# Buttons mit Bildern

p1 = PhotoImage(file=r"C:\Users\Yannis\Desktop\OOSL Projekt\Ferret-master\Ferret-master\Assets\SELECTED_home-heart.png")

b1 = Button(root, image=p1)

b1.grid(column=0, row=1)

# Dropdown Menu
variable = StringVar(root)
variable.set(dropdown[0])

d1 = OptionMenu(root, variable, *dropdown)
d1.grid(column=0, row=0)

root.mainloop()
