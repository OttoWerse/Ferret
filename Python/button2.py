import os
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
import paho.mqtt.client as mqtt

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(os.getcwd()), "Assets")
print(ASSETS_PATH)

# Dictionaries
topics = dict()
buttons = dict()

# Colors
colorInactive = "#ffffff"
colorActive = "#000000"


# Generates a custom tile with run-time generated text and custom image via the
# PIL module.
def render_key_image(deck, icon_filename, font_filename, label_text, fill):
    # Create new key image of the correct dimensions, black background.
    image = PILHelper.create_image(deck)

    # Resize the source image asset to best-fit the dimensions of a single key,
    # and paste it onto our blank frame centered as closely as possible.
    icon = Image.open(icon_filename).convert("RGBA")
    icon.thumbnail((image.width, image.height), Image.LANCZOS)
    icon_pos = ((image.width - icon.width) // 2, (image.height - icon.height) // 2)
    image.paste(icon, icon_pos, icon)

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 14)
    label_w, label_h = draw.textsize(label_text, font=font)
    label_pos = ((image.width - label_w) // 2, image.height - 20)
    draw.text(label_pos, text=label_text, font=font, fill=fill)

    return PILHelper.to_native_format(deck, image)


# Creates a new key image based on the key index, style and current key state
# and updates the image on the StreamDeck.
def update_key_image(deck, key, icon, label, fill):
    name = "exit"
    icon = os.path.join(ASSETS_PATH, icon)

    font = os.path.join(ASSETS_PATH, "arial.ttf")

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, icon, font, label, fill)

    # Update requested key with the generated image.
    deck.set_key_image(key, image)


class Button:
    def __init__(self, id=-1, label='', icon='', action=None, icons=dict(), state=False):
        self.id = id
        self.label = label
        self.icon = icon
        self.action = action
        self.icons = icons
        self.state = state


def make_mqtt(topic):
    return lambda self: client.publish(topic + '/in', str(not self.state).lower())


# Create function for receiving messages
def on_message(client, userdata, message):
    # get button from buttons list
    button = topics.get(message.topic)
    # decode message
    str = message.payload.decode("utf-8")
    # change button attributes
    button.icon = button.icons.get(str)
    button.label = str
    button.state = str == 'true'
    update_key_image(deck, button.id, button.icon, button.label, colorInactive)
    # print result (for debugging purposes)
    print(topics.get(message.topic).__dict__)


# Create function for publishing callback
def on_publish(client, userdata, result):
    # print(result)
    pass


def key_change_callback_default(deck, key, state):
    button = buttons[key]
    if state:
        print(button)
        button.action(button)


if __name__ == "__main__":
    # MQTT broker Settings
    broker = "192.169.4.5"
    port = 1883

    # Create MQTT client
    client = mqtt.Client("Ferret2")

    # Assign on methods
    client.on_publish = on_publish
    client.on_message = on_message

    # Connect to broker
    client.connect(broker, port)

    # Start the loop
    # client.loop_start()

    client.subscribe('mqtt-test/out')

    test_topic = 'mqtt-test'
    test_button = Button(0, "Button 1", "test.png", make_mqtt(test_topic))
    print(test_button.__dict__)
    test_button.icons['true'] = 'repeat.png'
    test_button.icons['false'] = 'repeat-off.png'
    topics[test_topic + '/out'] = test_button
    print(topics)
    buttons[test_button.id] = test_button
    test_button.action(test_button)

    # Find StreamDeck
    streamdecks = DeviceManager().enumerate()
    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        deck.open()
        deck.reset()
        print("Opened '{}' device (serial number: '{}')".format(deck.deck_type(), deck.get_serial_number()))
        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback_default)


    client.loop_forever()
