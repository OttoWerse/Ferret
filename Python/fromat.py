def generate_vban_topic(server, input, output):
    s = f'vban/{server}/{input}/{output}/out'
    return s


class mqtt_toggle:
    def __init__(self, icons, send, receive):
        self.icons = icons
        self.send = send
        self.receive = receive


if __name__ == "__main__":
    server = 'saturn'
    input = 'landsat'
    output = 'speakers'
    ic = 'repeat-off.png'
    print(ic)
    ot = f'vban/{server}/{input}/{output}/out'
    print(ot)
    it = f'vban/{server}/{input}/{output}/in'
    print(it)
    bu = mqtt_toggle(ic, ot, it)
    print(bu)
    print(bu.icons)
    print(bu.send)
    print(bu.receive)
