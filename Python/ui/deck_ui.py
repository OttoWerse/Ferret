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
current_view_selection = None
views_dropdown = None
deck_height, deck_width = 0, 0


def GUI(deck):
    global images, buttons, current_view_selection, views_dropdown, deck_height, deck_width

    if isinstance(deck.hardware, StreamDeckMini.StreamDeckMini):
        deck_height = 2
        deck_width = 3
    elif isinstance(deck.hardware, StreamDeckOriginal.StreamDeckOriginal):
        deck_height = 3
        deck_width = 5
    elif isinstance(deck.hardware, StreamDeckOriginalV2.StreamDeckOriginalV2):
        deck_height = 3
        deck_width = 5
    elif isinstance(deck.hardware, StreamDeckXL.StreamDeckXL):
        deck_height = 4
        deck_width = 8
    else:
        deck_height = 3
        deck_width = 5

    def dialog():
        answer = simpledialog.askstring("Input", "Enter view name",
                                        parent=root)
        if answer is not None:
            deck.add_view(ferret.View(name=answer))
            update(deck)
        else:
            logging.error("Name is missing!")

    # Dropdown Menu
    current_view_selection = StringVar(root)
    current_view_selection.set(deck.current_view.name)
    views_dropdown = OptionMenu(root, current_view_selection, command=select)
    views_dropdown.config(width=22)
    views_dropdown.grid(column=0, row=0, columnspan=deck_width - 1, sticky=W)

    b2 = Button(root, command=dialog)
    b2.grid(column=deck_width - 1, row=0)

    update(deck)

    root.mainloop()


def select(deck, new_view_selection):
    deck.switch_view(new_view_selection)
    current_view_selection.set(new_view_selection)
    update(deck)


def update(deck):
    view = deck.current_view
    x = 1
    y = 0
    for button in buttons:
        button.destroy()
    for key in view.keys:

        if y == deck_width:
            x = x + 1
            y = 0

        file_system_image = Image.open(key.image)
        tkinter_image = ImageTk.PhotoImage(file_system_image)
        images.append(tkinter_image)

        def add_action(key):
            return lambda: key_ui.GUI(key)

        key_button = Button(root, image=tkinter_image, command=add_action(key))
        key_button.grid(column=y, row=x)

        buttons.append(key_button)
        y = y + 1

        # Save current data in database
        db.update_data(deck, ferret.db_file)

    views_dropdown["menu"].delete(0, "end")
    for view in deck.views:
        views_dropdown["menu"].add_command(label=view,
                                           command=lambda containing_deck=deck, selection=view:
                                           select(containing_deck, selection))
