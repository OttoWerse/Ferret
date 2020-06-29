from tkinter import *
from Python.ui import list_ui


def GUI(action=None):
    root = Tk()

    # Setter for Icons, Colors and Labels
    def set_icons():
        list_ui.GUI(action.icons)

    def set_colors():
        list_ui.GUI(action.colors)

    def set_labels():
        list_ui.GUI(action.labels)

    # 4 Labels
    topic = Label(root, text="Topic")
    icons = Label(root, text="Icons")
    colors = Label(root, text="Colors")
    labels = Label(root, text="Labels")

    topic.grid(column=0, row=0)
    icons.grid(column=0, row=1)
    colors.grid(column=0, row=2)
    labels.grid(column=0, row=3)

    # 3 Buttons
    button1 = Button(root, text="+", width=10, command=set_icons)
    button2 = Button(root, text="+", width=10, command=set_colors)
    button3 = Button(root, text="+", width=10, command=set_labels)

    button1.grid(column=3, row=1)
    button2.grid(column=3, row=2)
    button3.grid(column=3, row=3)

    # 2 Entry Fields
    entry1 = Entry(root)
    entry1.insert(END, action.topic)
    entry1.grid(column=3, row=0)

    # saving the values of client and topic for further use
    # then closes the window
    def save():
        action.client = action.client
        action.topic = entry1.get()

        root.destroy()

    root.protocol("WM_DELETE_WINDOW", save)

    root.mainloop()


