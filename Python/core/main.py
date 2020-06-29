import logging
import Python.db.database as db
from StreamDeck.DeviceManager import DeviceManager
from Python.logic import ferret
from Python.ui import deck_ui

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # Find StreamDeck
    streamdecks = DeviceManager().enumerate()
    logging.info(f'Found {len(streamdecks)} Stream Deck(s)')

    for index, streamdeck in enumerate(streamdecks):
        streamdeck.open()
        streamdeck.reset()
        logging.info(f'Opened {streamdeck.deck_type()} device (serial number: {streamdeck.get_serial_number()})')

        # Create a Stream Deck
        deck = db.load_deck(streamdeck, ferret.db_file)

    deck_ui.GUI(deck)
