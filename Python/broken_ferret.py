import os
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
import paho.mqtt.client as mqtt
import time

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(os.getcwd()), "Assets")
print(ASSETS_PATH)

# Dictionaries
topics = dict()
buttons = dict()
actions = dict()

# Colors
colorInactive = "#ffffff"
colorActive = "#000000"

# MQTT broker Settings
broker = "192.169.0.203"
port = 1883

# Create MQTT client
client = mqtt.Client("Ferret14")


# Create function for receiving messages
def on_message(client, userdata, message):
    # get button from buttons list
    button = topics.get(message.topic)
    # decode message
    str = message.payload.decode("utf-8")
    print(str)
    # change button attributes
    button.icon = button.icons.get(str)
    button.label = str
    button.state = str == 'true'


# Create function for publishing callback
def on_publish(client, userdata, result):
    # print(result)
    pass


# Assign on methods
client.on_publish = on_publish
client.on_message = on_message


class Button:
    def __init__(self, id=-1, label='', icon='', action=None):
        self.id = id
        self.label = label
        self.icon = icon
        self.action = action


class Action:
    def __init__(self, onPress=None, onHold=None, onRelease=None):
        self.onPress = onPress
        self.onHold = onHold
        self.onRelease = onRelease


class MqttToggle(Action):
    def __init__(self, topic, state):
        def onPress():
            self.state = not self.state
            client.publish(self.topic + '/in', str(self.state).lower())

        self.onPress = onPress
        self.topic = topic
        self.state = state
        actions[topic] = self


if __name__ == "__main__":
    # Connect to broker
    client.connect(broker, port)
    print('connected')

    test_topic = 'mqtt-test'
    test_mqtt_toggle = MqttToggle(test_topic, False)
    test_button = Button(0, 'test', 'repeat.png', test_mqtt_toggle)

    test_button.action.onPress()
    time.sleep(1)
    test_button.action.onPress()

    client.loop_forever()
