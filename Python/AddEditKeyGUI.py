from tkinter import *

import paho.mqtt.client as mqtt

from Python import ferret, AddMQTTActionGUI, MQTTToggleGUI, ViewActionGUI

dropdown = ["Mqtt Action", "Mqtt Toggle", "View Action"]


def GUI(key):
    root = Tk()

    def egalfunction(args):
        if args == "Mqtt Action":
            if isinstance(key.action, ferret.MqttAction):
                AddMQTTActionGUI.GUI(key.action)
            else:
                AddMQTTActionGUI.GUI()
        elif args == "Mqtt Toggle":
            if isinstance(key.action, ferret.MqttToggle):
                MQTTToggleGUI.GUI(key.action)
            else:
                MQTTToggleGUI.GUI()
        elif args == "View Action":
            if isinstance(key.action, ferret.ViewAction):
                ViewActionGUI.GUI(key.action)
            else:
                ViewActionGUI.GUI()

    l1 = Label(root, text="Name")
    l2 = Label(root, text="Label")
    l3 = Label(root, text="Image")
    l4 = Label(root, text="Action")

    l1.grid(column=0, row=0)
    l2.grid(column=0, row=1)
    l3.grid(column=0, row=2)
    l4.grid(column=0, row=3)

    e1 = Entry(root)
    e2 = Entry(root)
    e3 = Entry(root)

    e1.insert(END, key.name)
    e2.insert(END, key.image)
    e3.insert(END, key.label)

    e1.grid(column=1, row=0)
    e2.grid(column=1, row=1)
    e3.grid(column=1, row=2)

    variable = StringVar(root)

    d1 = OptionMenu(root, variable, *dropdown, command=egalfunction)
    d1.grid(column=1, row=3)

    if isinstance(key.action, ferret.MqttAction):
        variable.set(dropdown[0])
    elif isinstance(key.action, ferret.MqttToggle):
        variable.set(dropdown[1])
    elif isinstance(key.action, ferret.ViewAction):
        variable.set(dropdown[2])

    root.mainloop()


if __name__ == "__main__":
    name = "keyanu-reaves"
    image = "dickpic.png"

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

    action = ferret.MqttAction(client1, topic1, payload, icons, labels, colors)

    label = "egal"

    GUI(ferret.Key(name, image, action, label))
