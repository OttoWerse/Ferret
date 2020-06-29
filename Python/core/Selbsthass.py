from StreamDeck.DeviceManager import DeviceManager
from Python.logic import ferret
from Python.ui import deck_ui
from Python.logic.ferret import StreamDeck, Key, View


if __name__ == "__main__":
    # Create Keys
    keys0 = []
    keys1 = []
    # Create a View
    view0 = View('mainView', keys0)
    view1 = View('testView', keys1)
    # Create Views
    views = {
        'mainView': view0
    }
    # Create an MQTT Action
    topic1 = 'mqtt-test'
    topic2 = 'mqtt-test-2'
    topic3 = 'mqtt-test-3'
    payload = 'false'
    icons1 = {
        'ping': 'repeat.png',
    }
    labels1 = {
        'ping': 'ping',
    }
    colors1 = {
        'ping': '#ff00ff',
    }
    view1.add_key(1, Key('Key1', 'repeat.png', ferret.MqttAction(topic1, payload, icons1, labels1, colors1)))
    icons2 = {
        'true': 'repeat.png',
        'false': 'repeat-off.png',
    }
    icons2 = {
        'true': 'repeat.png',
        'false': 'repeat-off.png',
    }
    labels2 = {
        'true': 'An',
        'false': 'Aus',
    }
    colors2 = {
        'true': '#ff00ff',
        'false': '#00ffff',
    }
    view1.add_key(2,
                  Key('Key2', 'repeat.png', ferret.MqttToggle(topic2, payload, icons2, labels2, colors2)))

    # Find StreamDeck
    streamdecks = DeviceManager().enumerate()
    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, streamdeck in enumerate(streamdecks):
        streamdeck.open()
        streamdeck.reset()
        print("Opened '{}' device (serial number: '{}')".format(streamdeck.deck_type(), streamdeck.get_serial_number()))

        # Create a Stream Deck
        deck = StreamDeck(streamdeck, views, views.get('mainView'))

    deck.add_view(view1)

    for client in ferret.clients:
        client.loop_start()

    deck_ui.GUI(deck)
