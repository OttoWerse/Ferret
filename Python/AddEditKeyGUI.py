from tkinter import *

dropdown = ["Kill", "Me", "Please"]

root = Tk()

l1 = Label(root, text="Name")
l2 = Label(root, text="Label")
l3 = Label(root, text="Image")
l4 = Label(root, text="Icon")

l1.grid(column=0, row=0)
l2.grid(column=0, row=1)
l3.grid(column=0, row=2)
l4.grid(column=0, row=3)

e1 = Entry(root)
e2 = Entry(root)
e3 = Entry(root)

e1.grid(column=1, row=0)
e2.grid(column=1, row=1)
e3.grid(column=1, row=2)

variable = StringVar(root)
variable.set(dropdown[0])

d1 = OptionMenu(root, variable, *dropdown)
d1.grid(column=1, row=3)

root.mainloop()
