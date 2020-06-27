from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import paho.mqtt.client as mqtt
import StreamDeck

from Python import ferret

dropdown = ["Kill", "Me", "Please"]

root = Tk()


def GUI(view):
    x = 1
    y = 0
    images = []
    for key in view.keys:
        if isinstance(key.view.deck, StreamDeck.Devices.StreamDeckMini.StreamDeckMini):
            h = 2
            b = 3
        elif isinstance(key.view.deck, StreamDeck.Devices.StreamDeckOriginal.StreamDeckOriginal):
            h = 3
            b = 5
        elif isinstance(key.view.deck, StreamDeck.Devices.StreamDeckOriginalV2.StreamDeckOriginalV2):
            h = 3
            b = 5
        elif isinstance(key.view.deck, StreamDeck.Devices.StreamDeckXL.StreamDeckXL):
            h = 4
            b = 8
        else:
            h = 420
            b = 69

        if y == b:
            x = x+1
            y = 0

        i1 = Image.open(key.image)
        p1 = ImageTk.PhotoImage(i1)
        images.append(p1)
        b1 = Button(root, image=p1)
        b1.grid(column=y, row=x)
        y = y+1

        print(p1.__dict__)

    # Dropdown Menu
    variable = StringVar(root)
    variable.set(dropdown[0])

    d1 = OptionMenu(root, variable, *dropdown)
    d1.grid(column=0, row=0)

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
    view = ferret.View(name, keys)
    views = {"dicktionary": view}
    deck = ferret.StreamDeck(None, views, view)
    GUI(view)
