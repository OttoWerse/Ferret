import types
from types import FunctionType
import paho.mqtt.client as mqtt


class Button:
    def __init__(self, id=-1, label='', icon='', code='pass'):
        self.id = id
        self.label = label
        self.icon = icon
        self.code = code
        self.add_action(self.code)

    def add_action(self, code):
        return setattr(self, 'action', types.MethodType(
            FunctionType(compile(f'def action(self):\n    {code}', "file", "exec").co_consts[0], globals(), "action"),
            self))


# Create function for receiving messages
def on_message(client, userdata, message):
    print(message)


# Create function for publishing callback
def on_publish(client, userdata, result):
    print(result)


if __name__ == "__main__":
    # MQTT broker Settings
    broker = "192.169.4.5"
    port = 1883

    # Create MQTT client
    client = mqtt.Client("Deck")

    # Assign on methods
    client.on_publish = on_publish
    client.on_message = on_message

    # Connect to broker
    client.connect(broker, port)

    # Start the loop
    client.loop_start()

    vban_server = 'saturn'
    vban_input = 'landsat'
    vban_output = 'speakers'
    topic = f'vban/{vban_server}/{vban_input}/{vban_output}/out'

    code1 = '''
    client.publish("testi", "test")
    print(self.icon)
    print("test")
    '''
    code2 = 'print(self.icon)'

    bu1 = Button(0, "Button 1", "test.png", code1)
    bu2 = Button(1, "Button 2", "test.png", code2)
    bu3 = Button(1, "Button 3", "test.png")

    bu1.action()
    bu2.action()
    bu3.action()

    client.loop_stop()
