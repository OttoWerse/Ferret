from tkinter import *
import Python.FerretUI

icons = {}
colors = {}
labels = {}
root = Tk()


def setIcons():
    Python.FerretUI.GUI(icons)


def getIcons():
    print(icons)


def setColors():
    Python.FerretUI.GUI(colors)


def getColors():
    print(colors)


def setLabels():
    Python.FerretUI.GUI(labels)


def getLabels():
    print(labels)


e1 = Entry(root)
e2 = Entry(root)
button = Button(root, text="set Icons", command=setIcons)
benjamin = Button(root, text="get Icons", command=getIcons)
beavis = Button(root, text="set Colors", command=setColors)
buttonhead = Button(root, text="get Colors", command=getColors)
labeldor = Button(root, text="set Labels", command=setLabels)
labcoat = Button(root, text="get Labels", command=getLabels)
button.pack()
benjamin.pack()
beavis.pack()
buttonhead.pack()
labeldor.pack()
labcoat.pack()

root.mainloop()
