import logging
from tkinter import *
import paho.mqtt.client as mqtt
from Python.logic import ferret
from Python.ui import mqtt_action_ui, mqtt_toggle_ui, view_action_ui

logging.basicConfig(level=logging.INFO)
dropdown = ["Mqtt Action", "Mqtt Toggle", "View Action"]


def GUI(key):
    root = Tk()

    def evaluate_dropdown(current_selection):
        if current_selection == "Mqtt Action":
            if not isinstance(key.action, ferret.MqttAction):
                logging.info("adding a new MQTT action")
                key.set_action(ferret.MqttAction())
            mqtt_action_ui.GUI(key.action)
        elif current_selection == "Mqtt Toggle":
            if not isinstance(key.action, ferret.MqttToggle):
                logging.info("adding a new MQTT toggle")
                key.set_action(ferret.MqttToggle())
            mqtt_toggle_ui.GUI(key.action)
        elif current_selection == "View Action":
            if isinstance(key.action, ferret.ViewAction):
                logging.info("adding a new view action")
                key.set_action(ferret.ViewAction())
            view_action_ui.GUI(key.action)

    label_name = Label(root, text="Name")
    label_label = Label(root, text="Label")
    label_image = Label(root, text="Image")
    label_action = Label(root, text="Action")

    label_name.grid(column=0, row=0)
    label_label.grid(column=0, row=1)
    label_image.grid(column=0, row=2)
    label_action.grid(column=0, row=3)

    entry_name = Entry(root)
    entry_label = Entry(root)
    label_image = Entry(root)

    entry_name.insert(END, key.name)
    entry_label.insert(END, key.label)
    label_image.insert(END, key.image)

    entry_name.grid(column=1, row=0)
    entry_label.grid(column=1, row=1)
    label_image.grid(column=1, row=2)

    current_action_selection = StringVar(root)

    action_selector = OptionMenu(root, current_action_selection, *dropdown, command=evaluate_dropdown)
    action_selector.grid(column=1, row=3)

    if key.action:
        if isinstance(key.action, ferret.MqttToggle):
            current_action_selection.set(dropdown[1])
        elif isinstance(key.action, ferret.MqttAction):
            current_action_selection.set(dropdown[0])
        elif isinstance(key.action, ferret.ViewAction):
            current_action_selection.set(dropdown[2])
        else:
            logging.info(f'unknown action type: {type(key.action)}')

    def save():
        key.name = entry_name.get()
        key.label = entry_label.get()
        key.image = label_image.get()

        root.destroy()

    root.protocol("WM_DELETE_WINDOW", save)

    root.mainloop()
