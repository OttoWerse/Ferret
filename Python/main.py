from StreamDeck.DeviceManager import DeviceManager
from Python import MainViewGUI, ferret
from Python.ferret import StreamDeck, Key, View

import paho.mqtt.client as mqtt

if __name__ == "__main__":
    # Create a client
    broker = "192.169.0.203"
    port = 1883

    clients = []

    client1 = mqtt.Client("Ferret-10")
    client1.connect(broker, port)
    clients.append(client1)

    client2 = mqtt.Client("Ferret-20")
    client2.connect(broker, port)
    clients.append(client2)

    client3 = mqtt.Client("Ferret-30")
    client3.connect(broker, port)
    clients.append(client3)

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
    view0.add_key(1, Key('Key1', 'repeat.png', ferret.MqttAction(client1, topic1, payload, icons, labels, colors)))
    view0.add_key(2,
                  Key('Key2', 'repeat.png', ferret.MqttToggle(client2, topic2, payload, icons, labels, colors)))
    view0.add_key(3,
                  Key('Key3', 'repeat.png', ferret.MqttToggle(client3, topic3, payload, icons, labels, colors)))

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

    MainViewGUI.GUI(deck)
