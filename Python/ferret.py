import os
import paho.mqtt.client as mqtt

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

ASSETS_PATH = os.path.join(os.path.dirname(os.getcwd()), "Assets")


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
    icon = os.path.join(ASSETS_PATH, icon)

    font = os.path.join(ASSETS_PATH, "arial.ttf")

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, icon, font, label, fill)

    # Update requested key with the generated image.
    deck.set_key_image(key, image)


class StreamDeck:
    def __init__(self, hardware, views, current_view):
        self.hardware = hardware
        self.views = views
        self.current_view = current_view
        self.current_view.deck = self

        def callback(deck, key, state):
            if key < len(self.current_view.keys):
                if self.current_view.keys[key]:
                    if state:
                        self.current_view.keys[key].action.on_press()
                    if not state:
                        self.current_view.keys[key].action.on_release()

        hardware.set_key_callback(callback)

    def switch_view(self, view):
        self.current_view.deck = None
        self.current_view = self.views.get(view)
        self.current_view.deck = self

    def add_view(self, view):
        self.views[view.name] = view

    def del_view(self, view):
        self.views.pop(view)


class View:
    def __init__(self, name, keys):
        self.name = name
        self.keys = keys
        for key in self.keys:
            key.view = self

    def add_key(self, position, key):
        self.keys.insert(position, key)
        self.keys[position - 1].view = self

    def del_key(self, key):
        self.keys.pop(key)


class Key:
    def __init__(self, name, image, action, label=''):
        self.name = name
        self.image = os.path.join(ASSETS_PATH, image)
        self.action = action
        self.action.key = self
        self.label = label


class Action:
    def __init__(self, on_press=lambda: print("nothing to do"),
                 on_release=lambda: print("nothing to do")):
        self.on_press = on_press
        self.on_release = on_release


class MqttAction(Action):
    def __init__(self, client, topic, payload, icons, labels, colors):
        self.client = client
        self.topic = topic
        self.payload = payload
        self.icons = icons
        self.labels = labels
        self.colors = colors

        self.client.subscribe(self.topic + '/out')

        def on_press():
            pass

        self.on_press = on_press

        def on_release():
            self.client.publish(self.topic + '/in', str(self.payload).lower())

        self.on_release = on_release

        def on_message(client, userdata, message):
            str = message.payload.decode("utf-8")
            print(str)
            print(f'Key: {self.key}')
            print(f'Hardware: {self.key.view.deck.hardware}')
            # self.key.label = str
            hardware = self.key.view.deck.hardware
            index = self.key.view.deck.current_view.keys.index(self.key)
            icon = icons[str]
            label = labels[str]
            color = colors[str]
            update_key_image(hardware, index, icon, label, color)

        self.client.on_message = on_message


class ViewAction(Action):
    def __init__(self, deck, view):
        self.deck = deck
        self.view = view

        def on_press():
            pass

        self.on_press = on_press

        def on_release():
            self.deck.switch_view(view)

        self.on_release = on_release


if __name__ == "__main__":
    # Create a client
    broker = "192.169.0.203"
    port = 1883
    client = mqtt.Client("Ferret419")
    client.connect(broker, port)

    # Create an MQTT Action
    topic = 'mqtt-test'
    payload = 'hello World'
    icons = {
        'hello world': 'repeat.png'
    }
    labels = {
        'hello world': 'Moin'
    }
    colors = {
        'hello world': '#ffffff'
    }
    action1 = MqttAction(client, topic, payload, icons, labels, colors)

    # Create another Key
    key1 = Key('testKey', 'test.png', action1)

    # Create Keys
    keys0 = []
    print(f'keys0: {keys0}')
    # Create more Keys
    keys1 = [key1]
    print(f'keys1: {keys1}')

    # Create a View
    view0 = View('mainView', keys0)

    # Create Views
    views = {
        'mainView': view0
    }
    print(views)

    # Find StreamDeck
    streamdecks = DeviceManager().enumerate()
    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, streamdeck in enumerate(streamdecks):
        streamdeck.open()
        streamdeck.reset()
        print("Opened '{}' device (serial number: '{}')".format(streamdeck.deck_type(), streamdeck.get_serial_number()))

        # Create a Stream Deck
        deck = StreamDeck(streamdeck, views, views.get('mainView'))

    deck.add_view(View('testView', keys1))
    # Add a key
    view0.add_key(1, Key('mainKey', 'test.png', ViewAction(deck, 'testView')))

    client.loop_forever()
