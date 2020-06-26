from tkinter import *

root = Tk()

# 5 Labels
l1 = Label(root, text="Topic")
l2 = Label(root, text="Payload")
l3 = Label(root, text="Icons")
l4 = Label(root, text="Colors")
l5 = Label(root, text="Labels")

l1.grid(column=0, row=0)
l2.grid(column=0, row=1)
l3.grid(column=0, row=2)
l4.grid(column=0, row=3)
l5.grid(column=0, row=4)


# 3 Buttons
b1 = Button(root, text="+", width=10)
b2 = Button(root, text="+", width=10)
b3 = Button(root, text="+", width=10)

b1.grid(column=3, row=2)
b2.grid(column=3, row=3)
b3.grid(column=3, row=4)

# 2 Entries
e1 = Entry(root)
e2 = Entry(root)

e1.grid(column=3, row=0)
e2.grid(column=3, row=1)

root.mainloop()
