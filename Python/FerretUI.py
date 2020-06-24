from tkinter import *

i = 2
Boxwurst = []
icons = {}


def addBox():
    global i
    ent = Entry(root)
    ent2 = Entry(root)
    Boxwurst.append((ent, ent2))

    def delBox():
        Boxwurst.remove((ent, ent2))
        ent.destroy()
        ent2.destroy()
        but.destroy()

    but = Button(root, text="-", command=delBox)
    ent.grid(row=i)
    ent2.grid(row=i, column=1)
    but.grid(row=i, column=2)
    i = i + 1


def boxen():
    for x in Boxwurst:
        Boxt0 = x[0].get()
        Boxt1 = x[1].get()
        if Boxt0 and Boxt1:
            # print(Boxt0, Boxt1)
            icons[Boxt0] = Boxt1
    print(icons)


root = Tk()

e1 = Entry(root)
e2 = Entry(root)
button = Button(root, text="+", command=addBox)
benjamin = Button(root, text="Ausgabe", command=boxen)
e1.grid(column=0, row=1)
e2.grid(column=1, row=1)
button.grid(column=2, row=1)
benjamin.grid(column=0, row=0)
Boxwurst.append((e1, e2))

root.mainloop()
