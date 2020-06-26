from tkinter import *

import paho.mqtt.client as mqtt

from Python import ferret, FerretUI


def GUI(action):
    root = Tk()

    def setIcons():
        FerretUI.GUI(action.icons)

    def setColors():
        FerretUI.GUI(action.colors)

    def setLabels():
        FerretUI.GUI(action.labels)

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
    e1.insert(END, action.topic)
    e2.insert(END, action.payload)

    e1.grid(column=3, row=0)
    e2.grid(column=3, row=1)

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
