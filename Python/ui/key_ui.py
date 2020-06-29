import logging
from tkinter import *
import paho.mqtt.client as mqtt
from Python.logic import ferret
from Python.ui import mqtt_action_ui, mqtt_toggle_ui, view_action_ui

logging.basicConfig(level=logging.INFO)
dropdown = ["Mqtt Action", "Mqtt Toggle", "View Action"]


def GUI(key):
    root = Tk()

    def egalfunction(args):
        if args == "Mqtt Action":
            if not isinstance(key.action, ferret.MqttAction):
                logging.info("adding a new MQTT action")
                key.set_action(ferret.MqttAction())
            mqtt_action_ui.GUI(key.action)
        elif args == "Mqtt Toggle":
            if not isinstance(key.action, ferret.MqttToggle):
                logging.info("adding a new MQTT toggle")
                key.set_action(ferret.MqttToggle())
            mqtt_toggle_ui.GUI(key.action)
        elif args == "View Action":
            if isinstance(key.action, ferret.ViewAction):
                logging.info("adding a new view action")
                key.set_action(ferret.ViewAction())
            view_action_ui.GUI(key.action)

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

    if key.action:
        if isinstance(key.action, ferret.MqttToggle):
            variable.set(dropdown[1])
        elif isinstance(key.action, ferret.MqttAction):
            variable.set(dropdown[0])
        elif isinstance(key.action, ferret.ViewAction):
            variable.set(dropdown[2])
        else:
            logging.info(f'unknown action type: {type(key.action)}')

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
