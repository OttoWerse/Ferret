from tkinter import *

import paho.mqtt.client as mqtt

from Python.logic import ferret
from Python.ui import list_ui


def GUI(action=None):
    root = Tk()

    def setIcons():
        list_ui.GUI(action.icons)

    def setColors():
        list_ui.GUI(action.colors)

    def setLabels():
        list_ui.GUI(action.labels)

    # 4 Labels
    l1 = Label(root, text="Topic")
    l2 = Label(root, text="Icons")
    l3 = Label(root, text="Colors")
    l4 = Label(root, text="Labels")

    l1.grid(column=0, row=0)
    l2.grid(column=0, row=1)
    l3.grid(column=0, row=2)
    l4.grid(column=0, row=3)

    # 3 Buttons
    b1 = Button(root, text="+", width=10, command=setIcons)
    b2 = Button(root, text="+", width=10, command=setColors)
    b3 = Button(root, text="+", width=10, command=setLabels)

    b1.grid(column=3, row=1)
    b2.grid(column=3, row=2)
    b3.grid(column=3, row=3)

    # 2 Entries
    e1 = Entry(root)
    e1.insert(END, action.topic)
    e1.grid(column=3, row=0)

    def save():
        action.client = action.client
        action.topic = e1.get()

        print(action.icons)

        root.destroy()

    root.protocol("WM_DELETE_WINDOW", save)

    root.mainloop()


if __name__ == "__main__":
    # Create a client
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

    GUI(ferret.MqttAction(client1, topic1, payload, icons, labels, colors))
