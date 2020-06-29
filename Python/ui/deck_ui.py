import logging
import Python.db.database as db
from tkinter import *
from tkinter import simpledialog
from tkinter.ttk import *
from PIL import Image, ImageTk
from StreamDeck.Devices import StreamDeckMini, StreamDeckOriginal, StreamDeckOriginalV2, StreamDeckXL
from Python.logic import ferret
from Python.ui import key_ui

logging.basicConfig(level=logging.INFO)

root = Tk()
images = []
buttons = []
variable = None
d1 = None
h, b = 0, 0


def GUI(deck):
    global images, buttons, variable, d1, h, b

    if isinstance(deck.hardware, StreamDeckMini.StreamDeckMini):
        h = 2
        b = 3
    elif isinstance(deck.hardware, StreamDeckOriginal.StreamDeckOriginal):
        h = 3
        b = 5
    elif isinstance(deck.hardware, StreamDeckOriginalV2.StreamDeckOriginalV2):
        h = 3
        b = 5
    elif isinstance(deck.hardware, StreamDeckXL.StreamDeckXL):
        h = 4
        b = 8
    else:
        h = 3
        b = 5

    def dialog():
        answer = simpledialog.askstring("Input", "Benenne deine View",
                                        parent=root)
        if answer is not None:
            deck.add_view(ferret.View(name=answer))
            update(deck)
        else:
            logging.info("Name is missing!")

    # Dropdown Menu
    variable = StringVar(root)
    variable.set(deck.current_view.name)
    d1 = OptionMenu(root, variable, command=DD)
    d1.config(width=22)
    d1.grid(column=0, row=0, columnspan=b - 1, sticky=W)

    b2 = Button(root, command=dialog)
    b2.grid(column=b - 1, row=0)

    update(deck)

    # Button in Dropdown per if-case

    root.mainloop()


def DD(deck, args):
    deck.switch_view(args)
    variable.set(args)
    update(deck)


def update(deck):
    view = deck.current_view
    x = 1
    y = 0
    for button in buttons:
        button.destroy()
    for key in view.keys:

        if y == b:
            x = x + 1
            y = 0

        i1 = Image.open(key.image)
        p1 = ImageTk.PhotoImage(i1)
        images.append(p1)

        def addit(key):
            return lambda: key_ui.GUI(key)

        b1 = Button(root, image=p1, command=addit(key))
        b1.grid(column=y, row=x)

        buttons.append(b1)
        y = y + 1

        #Save current data in database
        db.update_data(deck,ferret.db_file)


    d1["menu"].delete(0, "end")
    for something in deck.views:
        d1["menu"].add_command(label=something, command=lambda deck=deck, selection=something: DD(deck, selection))

