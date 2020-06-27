import os
import paho.mqtt.client as mqtt

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

# Set the path for finding assets
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
    """
    A StreamDeck object represents a hardware-level StreamDeck for higher level operations
    Attributes:
        hardware : deck object
            contains the associated hardware level deck given by the Elgato API
        views : dict
            contains all view objects assigned to this specific StreamDeck
        current_view : view
            contains the currently active view
    Methods:
        switch_view(view_name)
            switches the current view to the view with the given name
        add_view(view)
            adds a view to the views dict
        del_view(view)
            deletes a view from the views dict
    """

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

        if self.hardware:
            hardware.set_key_callback(callback)

    def switch_view(self, view_name):
        """
        Switches the active view of a deck to the one with the given name
        :param view_name: the name of the view to switch to (must be one found in the views dict)
        :return: None
        """
        # Delete the reverse reference to the deck inside the no longer current view
        self.current_view.deck = None
        # Assign a new current view
        self.current_view = self.views.get(view_name)
        # Add a reverse reference to this deck to the new current view
        self.current_view.deck = self

    def add_view(self, view):
        # add the view to the dict
        # TODO: Error handling (view names need to be unique)
        self.views[view.name] = view

    def del_view(self, view):
        # TODO: Implement properly
        self.views.pop(view)


class View:
    """
    A view object represents a set of keys to be displayed on a given StreamDeck
    Attributes:
        name : str
            the unique given name of the view
        keys : list
            a list of keys that are part of the view
    Methods:
        add_key(position, key)
            adds a key to the key list at the specified position
        del_key(position)
            removes a key from the key list
    """

    def __init__(self, name, keys):
        self.name = name
        # TODO: Add empty keys to fill the list
        self.keys = keys
        # add reverse references to all initial keys
        for key in self.keys:
            key.view = self

    def add_key(self, position, key):
        """
        Adds a key to the keys list
        :param position: the position where the key is to be added
        :param key: the key to add
        :return: None
        """
        # TODO: Error handling (if the position is already taken, ask for replacement confirmation)
        # Add the key to the keys list
        self.keys.insert(position, key)
        # Add a reverse reference to the key
        self.keys[position - 1].view = self

    def del_key(self, position):
        """
        deletes a key from the keys list
        :param position: the position to delete the key from
        :return: None
        """
        # TODO: Implement
        pass


class Key:
    """
    A key object represents a key, that is part of a view
    (not to be confused wit the keys from the Elgato API, which represent actual physical keys on a StreamDeck)
    Attributes:
        name : str
            the given name of the key
        image : str
            the name of the current image file (must be inside the assets folder)
        action : action object
            the action that is executed, when the key state is changed
        label : str
            the current label that is written on the key
    """

    def __init__(self, name, image, action, label=''):
        self.name = name
        # Adding assets path to image path
        self.image = os.path.join(ASSETS_PATH, image)
        self.action = action
        self.action.key = self
        self.label = label


class Action:
    """
    An action is a container object for methods that are to be executed when the associated key changes states.
    It also manages the image and label of the associated key based on the response of those functions.
    (this class is more or less abstract at this point)
    Attributes:
        on_press : method
            the method to be executed, when the key is pressed down
        on_release : method
            the method to be executed, when the key is released up
    """

    def __init__(self,
                 on_press=lambda: print("nothing to do"),
                 on_release=lambda: print("nothing to do")):
        self.on_press = on_press
        self.on_release = on_release


class MqttAction(Action):
    """
    A MQTT action is a type of action that sends and receives data over MQTT
    Attributes:
        on_press : method
            the method to be executed, when the key is pressed down (as for now this is unused)
        on_release : method
            the method to be executed, when the key is released up (sends an MQTT packet)
        client : MQTT client object
            the MQTT client to use for sending packages
        topic: str
            the MQTT topic (base) with which to communicate
        payload : str
            the payload to send an a button press
        icons : dict
            a dict of icons corresponding to received payload
        labels : dict
            a dict of labels corresponding to received payload
        colors : dict
            a dict of colors corresponding to received payload
    """

    def __init__(self, client, topic, payload, icons, labels, colors):
        self.client = client
        self.topic = topic
        self.payload = payload
        self.icons = icons
        self.labels = labels
        self.colors = colors

        # Subscribing to the given topics "out" channel (convention)
        self.client.subscribe(self.topic + '/out')

        # Create a function to be executed on press (this might be used in the future)
        def on_press():
            pass

        # Assign the function to the attribute of the same name
        self.on_press = on_press

        # Create a function to be executed on release (using the given topics "in" channel)
        def on_release():
            # Sending the given topic as a normalized string (homie convention)
            # TODO: Handle spaces and special characters
            self.client.publish(self.topic + '/in', str(self.get_payload()).lower())

        # Assign the function to the attribute of the same name
        self.on_release = on_release

        # Creating a function to be executed, when a new message arrives on the "out" channel
        def on_message(client, userdata, message):
            # Decode the message
            str = message.payload.decode("utf-8")
            # Determine the StreamDeck hardware the key is currently displayed on
            hardware = self.key.view.deck.hardware
            print(hardware)
            # Determine the index of the key on the StreamDeck hardware
            index = self.key.view.deck.current_view.keys.index(self.key)
            print(index)
            # Get Icon, label and color from the dicts
            icon = icons[str]
            label = labels[str]
            color = colors[str]
            print(icon, label, color)
            # Update the image on the hardware key
            update_key_image(hardware, index, icon, label, color)
            self.set_payload(str)

        # Assigning the function to the MQTT client
        self.client.on_message = on_message

    def get_payload(self):
        return self.payload

    def set_payload(self, payload):
        pass


class MqttToggle(MqttAction):
    """
    A MQTT toggle is a type of MQTT action that specifically deals with boolean payloads
    Attributes:
        on_press : method
            the method to be executed, when the key is pressed down (as for now this is unused)
        on_release : method
            the method to be executed, when the key is released up (sends an MQTT packet)
    """

    def __init__(self, client, topic, payload, icons, labels, colors):
        MqttAction.__init__(self, client, topic, payload, icons, labels, colors)

    def get_payload(self):
        print(f'GET {self.payload}')
        self.payload = not self.payload
        print(f'NOW {self.payload}')
        return self.payload

    def set_payload(self, payload):
        print(f'SET {payload}')
        if payload.lower() == 'true':
            self.payload = True
        elif payload.lower() == 'false':
            self.payload = False


class ViewAction(Action):
    """
    A view action is a type of action that changes the view of the associated deck
    Attributes:
        on_press : method
            the method to be executed, when the key is pressed down (as for now this is unused)
        on_release : method
            the method to be executed, when the key is released up (changes the view)
        deck : deck object
            the deck where the view is to be changed
    """

    def __init__(self, deck, view):
        self.deck = deck
        self.view = view

        # Create a function to be executed on press (this might be used in the future)
        def on_press():
            pass

        # Assign the function to the attribute of the same name
        self.on_press = on_press

        # Create a function to be executed on release
        def on_release():
            self.deck.switch_view(view)

        # Assign the function to the attribute of the same name
        self.on_release = on_release


if __name__ == "__main__":
    # Create a client
    broker = "192.169.0.203"
    port = 1883

    clients = []

    client1 = mqtt.Client("Ferret-1")
    client1.connect(broker, port)
    clients.append(client1)

    client2 = mqtt.Client("Ferret-2")
    client2.connect(broker, port)
    clients.append(client2)

    client3 = mqtt.Client("Ferret-3")
    client3.connect(broker, port)
    clients.append(client3)

    pseudoclient = mqtt.Client("pseudo")
    pseudoclient.connect(broker, port)

    # Create Keys
    keys0 = []
    # Create a View
    view0 = View('mainView', keys0)
    # Create Views
    views = {
        'mainView': view0
    }
    # Create an MQTT Action
    topic1 = 'mqtt-test'
    topic2 = 'mqtt-test-2'
    topic3 = 'mqtt-test-3'
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
    # Add a key
    view0.add_key(1, Key('Key', 'test.png', MqttToggle(client1, topic1, payload, icons, labels, colors)))
    view0.add_key(2,
                  Key('Key', 'test.png', MqttToggle(client2, topic2, payload, icons, labels, colors)))
    view0.add_key(3,
                  Key('Key', 'test.png', MqttToggle(client3, topic3, payload, icons, labels, colors)))

    # Find StreamDeck
    streamdecks = DeviceManager().enumerate()
    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, streamdeck in enumerate(streamdecks):
        streamdeck.open()
        streamdeck.reset()
        print("Opened '{}' device (serial number: '{}')".format(streamdeck.deck_type(), streamdeck.get_serial_number()))

        # Create a Stream Deck
        deck = StreamDeck(streamdeck, views, views.get('mainView'))

    for client in clients:
        client.loop_start()

    pseudoclient.loop_forever()
