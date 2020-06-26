from tkinter import *

import paho.mqtt.client as mqtt

from Python import ferret, FerretUI


def GUI(action=None):
    root = Tk()

    if action:
        client = action.client
        topic = action.topic
        payload = action.payload
        icons = action.icons
        colors = action.colors
        labels = action.labels
    else:
        client = None
        topic = ""
        payload = ""
        icons = {}
        colors = {}
        labels = {}

    def setIcons():
        FerretUI.GUI(icons)

    def setColors():
        FerretUI.GUI(colors)

    def setLabels():
        FerretUI.GUI(labels)

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
    b1 = Button(root, text="+", width=10, command=setIcons)
    b2 = Button(root, text="+", width=10, command=setColors)
    b3 = Button(root, text="+", width=10, command=setLabels)

    b1.grid(column=3, row=2)
    b2.grid(column=3, row=3)
    b3.grid(column=3, row=4)

    # 2 Entries
    e1 = Entry(root)
    e2 = Entry(root)
    e1.insert(END, topic)
    e2.insert(END, payload)

    e1.grid(column=3, row=0)
    e2.grid(column=3, row=1)

    def save():
        global action
        client = mqtt.Client("Ferret-1")
        topic = e1.get()
        payload = e2.get()

        action = ferret.MqttAction(client, topic, payload, icons, labels, colors)

        print(action)

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