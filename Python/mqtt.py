import paho.mqtt.client as mqtt


# Create function for receiving messages
def on_message(client, userdata, message):
    print(f'{message.topic} = {message.payload}')


# Create function for publishing callback
def on_publish(client, userdata, result):
    # print(result)
    pass


if __name__ == "__main__":
    # MQTT broker Settings
    broker = "192.169.4.5"
    port = 1883

    # Create MQTT client
    client = mqtt.Client("Ferret12344")

    # Assign on methods
    client.on_publish = on_publish
    client.on_message = on_message

    # Connect to broker
    client.connect(broker, port)

    # Start the loop

    client.subscribe('testi')

    client.loop_forever()

