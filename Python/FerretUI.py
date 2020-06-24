from tkinter import *

i = 2


def addBox():
    global i
    ent = Entry(root)
    ent2 = Entry(root)

    def delBox():
        ent.destroy()
        ent2.destroy()
        but.destroy()

    but = Button(root, text="-", command=delBox)
    ent.grid(row=i)
    ent2.grid(row=i, column=1)
    but.grid(row=i, column=2)
    i = i + 1


root = Tk()
root.geometry("300x400")

e1 = Entry(root)
e2 = Entry(root)
button = Button(root, text="+", command=addBox)
e1.grid(column=0, row=0)
e2.grid(column=1, row=0)
button.grid(row=0, column=2)
e1.insert(END, "default_icon")
e2.insert(END, "default_aufgabe")

root.mainloop()
