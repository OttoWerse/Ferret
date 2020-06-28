from tkinter import *
from tkinter import simpledialog
from tkinter.ttk import *
from PIL import Image, ImageTk
import paho.mqtt.client as mqtt
import StreamDeck

from Python import ferret, AddEditKeyGUI

root = Tk()


def GUI(deck):
    images = []
    buttons = []

    if isinstance(deck, StreamDeck.Devices.StreamDeckMini.StreamDeckMini):
        h = 2
        b = 3
    elif isinstance(deck, StreamDeck.Devices.StreamDeckOriginal.StreamDeckOriginal):
        h = 3
        b = 5
    elif isinstance(deck, StreamDeck.Devices.StreamDeckOriginalV2.StreamDeckOriginalV2):
        h = 3
        b = 5
    elif isinstance(deck, StreamDeck.Devices.StreamDeckXL.StreamDeckXL):
        h = 4
        b = 8
    else:
        h = 3
        b = 5

    def update():
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
                return lambda: AddEditKeyGUI.GUI(key)

            b1 = Button(root, image=p1, command=addit(key))
            b1.grid(column=y, row=x)

            buttons.append(b1)
            y = y + 1

        d1["menu"].delete(0, "end")
        for something in deck.views:
            print(something)
            d1["menu"].add_command(label=something, command=lambda selection=something: DD(selection))

    def DD(args):
        deck.current_view = deck.views[args]
        variable.set(args)
        update()

    def dialog():
        answer = simpledialog.askstring("Input", "Benenne deine View",
                                        parent=root)
        if answer is not None:
            deck.views[answer] = ferret.View(name=answer, keys=[])
            update()
        else:
            print("Also kein Name")

    def edview():
        kays = [
            ferret.Key(name1, image, action, label),
            ferret.Key(name1, "repeat-off.png", action, label),
            ferret.Key(name1, image, action, label),
        ]
        deck.views["test"] = ferret.View(name="Probe", keys=kays)
        deck.current_view = deck.views["test"]
        update()

    # Dropdown Menu
    variable = StringVar(root)
    variable.set(deck.current_view.name)
    d1 = OptionMenu(root, variable, command=DD)
    d1.config(width=22)
    d1.grid(column=0, row=0, columnspan=b - 1, sticky=W)

    b2 = Button(root, command=dialog)
    b2.grid(column=b - 1, row=0)

    update()

    # Button in Dropdown per if-case

    root.mainloop()


if __name__ == "__main__":
    name = "beastieboy"
    name1 = "keyny loggins"
    image = "repeat.png"
    broker = "192.169.0.203"
    port = 1883

    client1 = mqtt.Client("Ferret-1")
    # client1.connect(broker, port)

    topic1 = 'mqtt-test'
    payload = 'ping'
    icons = {
        'true': 'repeat.png',
        'false': 'repeat-off.png',
    }
    labels = {
        'true': 'An',
        'false': 'Aus',
    }
    colors = {
        'true': '#ff00ff',
        'false': '#00ffff',
    }

    label = "labell delphine"
    action = ferret.MqttAction(client1, topic1, payload, icons, labels, colors)
    keys = [
        ferret.Key(name1, image, action, label),
        ferret.Key(name1, "repeat-off.png", action, label),
        ferret.Key(name1, image, action, label),
        ferret.Key(name1, image, action, label),
        ferret.Key(name1, image, action, label),
        ferret.Key(name1, image, action, label),
    ]

    keys1 = [
        ferret.Key(name1, image, action, label),
        ferret.Key(name1, image, action, label),
        ferret.Key(name1, image, action, label),
        ferret.Key(name1, "repeat-off.png", action, label),
    ]
    view = ferret.View(name, keys)
    view1 = ferret.View("irgendein name", keys1)
    views = {"beastieboy": view, "irgendein name": view1}
    deck = ferret.StreamDeck(None, views, view)
    GUI(deck)
    print("Hurensohn")
