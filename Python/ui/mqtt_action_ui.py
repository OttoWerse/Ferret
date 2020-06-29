from tkinter import *
from Python.ui import list_ui


def GUI(action):
    root = Tk()

    # Setter for Icons, Colors and Labels
    def set_icons():
        list_ui.GUI(action.icons)

    def set_colors():
        list_ui.GUI(action.colors)

    def set_labels():
        list_ui.GUI(action.labels)

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
    b1 = Button(root, text="+", width=10, command=set_icons)
    b2 = Button(root, text="+", width=10, command=set_colors)
    b3 = Button(root, text="+", width=10, command=set_labels)

    b1.grid(column=3, row=2)
    b2.grid(column=3, row=3)
    b3.grid(column=3, row=4)

    # 2 Entries
    e1 = Entry(root)
    e2 = Entry(root)

    # Setting default entries
    e1.insert(END, action.topic)
    e2.insert(END, action.payload)

    e1.grid(column=3, row=0)
    e2.grid(column=3, row=1)

    # saving the values of client and topic for further use
    # then closes the window
    def save():
        action.client = action.client
        action.topic = e1.get()
        action.payload = e2.get()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", save)

    root.mainloop()

