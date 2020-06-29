from tkinter import *

import paho.mqtt.client as mqtt

from Python.logic import ferret
from Python.ui import mqtt_action_ui, mqtt_toggle_view, view_action_ui

dropdown = ["Mqtt Action", "Mqtt Toggle", "View Action"]


def GUI(key):
    root = Tk()
    action = key.action

    def egalfunction(args):
        if args == "Mqtt Action":
            if isinstance(key.action, ferret.MqttAction):
                mqtt_action_ui.GUI(action)
            else:
                mqtt_action_ui.GUI()
        elif args == "Mqtt Toggle":
            if isinstance(key.action, ferret.MqttToggle):
                mqtt_toggle_view.GUI(action)
            else:
                mqtt_toggle_view.GUI()
        elif args == "View Action":
            if isinstance(key.action, ferret.ViewAction):
                view_action_ui.GUI(action)
            else:
                view_action_ui.GUI()

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
    e2.insert(END, key.label)
    e3.insert(END, key.image)

    e1.grid(column=1, row=0)
    e2.grid(column=1, row=1)
    e3.grid(column=1, row=2)

    variable = StringVar(root)

    d1 = OptionMenu(root, variable, *dropdown, command=egalfunction)
    d1.grid(column=1, row=3)

    if isinstance(action, ferret.MqttToggle):
        variable.set(dropdown[1])
    elif isinstance(action, ferret.MqttAction):
        variable.set(dropdown[0])
    elif isinstance(action, ferret.ViewAction):
        variable.set(dropdown[2])
    else:
        print(type(action))

    def save():
        key.name = e1.get()
        key.label = e2.get()
        key.image = e3.get()

        root.destroy()

    root.protocol("WM_DELETE_WINDOW", save)

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
