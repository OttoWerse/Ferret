#!/usr/bin/env python3

#         Python Stream Deck Library
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

# Example script showing basic library usage - updating key images with new
# tiles generated at runtime, and responding to button state change events.

import os
import threading
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
import paho.mqtt.client as mqtt

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")

# Group Icon IDs
terraGroup = 0
solarGroup = 1
bluetoothGroup = 2
charonGroup = 5
landsatGroup = 6
jupiterGroup = 7
vbanGroup = 10
dockGroup = 11

# Toggle Icon IDs
speakerToggle = 3
bluetoothToggle = 4
headsetToggle = 8
chatToggle = 9
broadcastToggle = 13

# Misc Icon IDs
resetEngineKey = 14

# Colors
colorInactive = "#ffffff"
colorActive = "#000000"

# Terra toggles
toggleTerra0 = None
toggleTerra1 = None
toggleTerra2 = None
toggleTerra3 = None
toggleTerra4 = None

# Solar toggles
toggleSolar0 = None
toggleSolar1 = None
toggleSolar2 = None
toggleSolar3 = None
toggleSolar4 = None

# Bluetooth toggles
toggleBluetooth0 = None
toggleBluetooth1 = None
toggleBluetooth2 = None
toggleBluetooth3 = None
toggleBluetooth4 = None

# Charon toggles
toggleCharon0 = None
toggleCharon1 = None
toggleCharon2 = None
toggleCharon3 = None
toggleCharon4 = None

# Landsat toggles
toggleLandsat0 = None
toggleLandsat1 = None
toggleLandsat2 = None
toggleLandsat3 = None
toggleLandsat4 = None

# Jupiter toggles
toggleJupiter0 = None
toggleJupiter1 = None
toggleJupiter2 = None
toggleJupiter3 = None
toggleJupiter4 = None

# VBAN toggles
toggleVBAN0 = None
toggleVBAN1 = None
toggleVBAN2 = None
toggleVBAN3 = None
toggleVBAN4 = None

# Dock toggles
toggleDock0 = None
toggleDock1 = None
toggleDock2 = None
toggleDock3 = None
toggleDock4 = None


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


# Default Layout
def key_change_callback_default(deck, key, state):
    # check for key
    if key == terraGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_terra)
            update_icons()
    if key == solarGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_solar)
            update_icons()
    if key == bluetoothGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_bluetooth)
            update_icons()
    if key == charonGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_charon)
            update_icons()
    if key == landsatGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_landsat)
            update_icons()
    if key == jupiterGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_jupiter)
            update_icons()
    if key == vbanGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_vban)
            update_icons()
    if key == dockGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_dock)
            update_icons()
    if key == resetEngineKey:
        # check for state
        if state:
            ret = client.publish("vban/saturn/system/restart/in", "0")


# sends MQTT packets for controlling "Terra"
def key_change_callback_terra(deck, key, state):
    # check for key
    if key == terraGroup:
        if state:
            deck.set_key_callback(key_change_callback_default)
            # Update Icons
            update_icons()
    if key == solarGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_solar)
            update_icons()
    if key == bluetoothGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_bluetooth)
            update_icons()
    if key == charonGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_charon)
            update_icons()
    if key == landsatGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_landsat)
            update_icons()
    if key == jupiterGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_jupiter)
            update_icons()
    if key == vbanGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_vban)
            update_icons()
    if key == dockGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_dock)
            update_icons()
    if key == speakerToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleTerra0:
                ret = client.publish("vban/saturn/terra/speakers/in", "false")
            if not toggleTerra0:
                ret = client.publish("vban/saturn/terra/speakers/in", "true")
    if key == headsetToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleTerra1:
                ret = client.publish("vban/saturn/terra/headset/in", "false")
            if not toggleTerra1:
                ret = client.publish("vban/saturn/terra/headset/in", "true")
    if key == bluetoothToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleTerra2:
                ret = client.publish("vban/saturn/terra/bluetooth-tx/in", "false")
            if not toggleTerra2:
                ret = client.publish("vban/saturn/terra/bluetooth-tx/in", "true")
    if key == broadcastToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleTerra3:
                ret = client.publish("vban/saturn/terra/broadcast/in", "false")
            if not toggleTerra3:
                ret = client.publish("vban/saturn/terra/broadcast/in", "true")
    if key == chatToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleTerra4:
                ret = client.publish("vban/saturn/terra/chat/in", "false")
            if not toggleTerra4:
                ret = client.publish("vban/saturn/terra/chat/in", "true")


# sends MQTT packets for controlling "Solar"
def key_change_callback_solar(deck, key, state):
    # check for key
    if key == terraGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_terra)
            update_icons()
    if key == solarGroup:
        if state:
            deck.set_key_callback(key_change_callback_default)
            # Update Icons
            update_icons()
    if key == bluetoothGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_bluetooth)
            update_icons()
    if key == charonGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_charon)
            update_icons()
    if key == landsatGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_landsat)
            update_icons()
    if key == jupiterGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_jupiter)
            update_icons()
    if key == vbanGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_vban)
            update_icons()
    if key == dockGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_dock)
            update_icons()
    if key == speakerToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleSolar0:
                ret = client.publish("vban/saturn/solar/speakers/in", "false")
            if not toggleSolar0:
                ret = client.publish("vban/saturn/solar/speakers/in", "true")
    if key == headsetToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleSolar1:
                ret = client.publish("vban/saturn/solar/headset/in", "false")
            if not toggleSolar1:
                ret = client.publish("vban/saturn/solar/headset/in", "true")
    if key == bluetoothToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleSolar2:
                ret = client.publish("vban/saturn/solar/bluetooth-tx/in", "false")
            if not toggleSolar2:
                ret = client.publish("vban/saturn/solar/bluetooth-tx/in", "true")
    if key == broadcastToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleSolar3:
                ret = client.publish("vban/saturn/solar/broadcast/in", "false")
            if not toggleSolar3:
                ret = client.publish("vban/saturn/solar/broadcast/in", "true")
    if key == chatToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleSolar4:
                ret = client.publish("vban/saturn/solar/chat/in", "false")
            if not toggleSolar4:
                ret = client.publish("vban/saturn/solar/chat/in", "true")


# sends MQTT packets for controlling "Bluetooth"
def key_change_callback_bluetooth(deck, key, state):
    # check for key
    if key == terraGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_terra)
            update_icons()
    if key == solarGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_solar)
            update_icons()
    if key == bluetoothGroup:
        if state:
            deck.set_key_callback(key_change_callback_default)
            # Update Icons
            update_icons()
    if key == charonGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_charon)
            update_icons()
    if key == landsatGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_landsat)
            update_icons()
    if key == jupiterGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_jupiter)
            update_icons()
    if key == vbanGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_vban)
            update_icons()
    if key == dockGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_dock)
            update_icons()
    if key == speakerToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleBluetooth0:
                ret = client.publish("vban/saturn/bluetooth-rx/speakers/in", "false")
            if not toggleBluetooth0:
                ret = client.publish("vban/saturn/bluetooth-rx/speakers/in", "true")
    if key == headsetToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleBluetooth1:
                ret = client.publish("vban/saturn/bluetooth-rx/headset/in", "false")
            if not toggleBluetooth1:
                ret = client.publish("vban/saturn/bluetooth-rx/headset/in", "true")
    if key == bluetoothToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleBluetooth2:
                ret = client.publish("vban/saturn/bluetooth-rx/bluetooth-tx/in", "false")
            if not toggleBluetooth2:
                ret = client.publish("vban/saturn/bluetooth-rx/bluetooth-tx/in", "true")
    if key == broadcastToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleBluetooth3:
                ret = client.publish("vban/saturn/bluetooth-rx/broadcast/in", "false")
            if not toggleBluetooth3:
                ret = client.publish("vban/saturn/bluetooth-rx/broadcast/in", "true")
    if key == chatToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleBluetooth4:
                ret = client.publish("vban/saturn/bluetooth-rx/chat/in", "false")
            if not toggleBluetooth4:
                ret = client.publish("vban/saturn/bluetooth-rx/chat/in", "true")


# sends MQTT packets for controlling "Charon"
def key_change_callback_charon(deck, key, state):
    ret = ""
    # check for key
    if key == terraGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_terra)
            update_icons()
    if key == solarGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_solar)
            update_icons()
    if key == bluetoothGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_bluetooth)
            update_icons()
    if key == charonGroup:
        if state:
            deck.set_key_callback(key_change_callback_default)
            # Update Icons
            update_icons()
    if key == landsatGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_landsat)
            update_icons()
    if key == jupiterGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_jupiter)
            update_icons()
    if key == vbanGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_vban)
            update_icons()
    if key == dockGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_dock)
            update_icons()
    if key == speakerToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleCharon0:
                ret = client.publish("vban/saturn/charon/speakers/in", "false")
            if not toggleCharon0:
                ret = client.publish("vban/saturn/charon/speakers/in", "true")
    if key == headsetToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleCharon1:
                ret = client.publish("vban/saturn/charon/headset/in", "false")
            if not toggleCharon1:
                ret = client.publish("vban/saturn/charon/headset/in", "true")
    if key == bluetoothToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleCharon2:
                ret = client.publish("vban/saturn/charon/bluetooth-tx/in", "false")
            if not toggleCharon2:
                ret = client.publish("vban/saturn/charon/bluetooth-tx/in", "true")
    if key == broadcastToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleCharon3:
                ret = client.publish("vban/saturn/charon/broadcast/in", "false")
            if not toggleCharon3:
                ret = client.publish("vban/saturn/charon/broadcast/in", "true")
    if key == chatToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleCharon4:
                ret = client.publish("vban/saturn/charon/chat/in", "false")
            if not toggleCharon4:
                ret = client.publish("vban/saturn/charon/chat/in", "true")
    print(ret)


# sends MQTT packets for controlling "Landsat"
def key_change_callback_landsat(deck, key, state):
    ret = ""
    # check for key
    if key == terraGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_terra)
            update_icons()
    if key == solarGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_solar)
            update_icons()
    if key == bluetoothGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_bluetooth)
            update_icons()
    if key == charonGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_charon)
            update_icons()
    if key == landsatGroup:
        if state:
            deck.set_key_callback(key_change_callback_default)
            # Update Icons
            update_icons()
    if key == jupiterGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_jupiter)
            update_icons()
    if key == vbanGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_vban)
            update_icons()
    if key == dockGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_dock)
            update_icons()
    if key == speakerToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleLandsat0:
                ret = client.publish("vban/saturn/landsat/speakers/in", "false")
            if not toggleLandsat0:
                ret = client.publish("vban/saturn/landsat/speakers/in", "true")
    if key == headsetToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleLandsat1:
                ret = client.publish("vban/saturn/landsat/headset/in", "false")
            if not toggleLandsat1:
                ret = client.publish("vban/saturn/landsat/headset/in", "true")
    if key == bluetoothToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleLandsat2:
                ret = client.publish("vban/saturn/landsat/bluetooth-tx/in", "false")
            if not toggleLandsat2:
                ret = client.publish("vban/saturn/landsat/bluetooth-tx/in", "true")
    if key == broadcastToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleLandsat3:
                ret = client.publish("vban/saturn/landsat/broadcast/in", "false")
            if not toggleLandsat3:
                ret = client.publish("Vvban/saturn/landsat/broadcast/in", "true")
    if key == chatToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleLandsat4:
                ret = client.publish("vban/saturn/landsat/chat/in", "false")
            if not toggleLandsat4:
                ret = client.publish("vban/saturn/landsat/chat/in", "true")
    print(ret)


# sends MQTT packets for controlling "Jupiter"
def key_change_callback_jupiter(deck, key, state):
    ret = ""
    # check for key
    if key == terraGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_terra)
            update_icons()
    if key == solarGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_solar)
            update_icons()
    if key == bluetoothGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_bluetooth)
            update_icons()
    if key == charonGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_charon)
            update_icons()
    if key == landsatGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_landsat)
            update_icons()
    if key == jupiterGroup:
        if state:
            deck.set_key_callback(key_change_callback_default)
            # Update Icons
            update_icons()
    if key == vbanGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_vban)
            update_icons()
    if key == dockGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_dock)
            update_icons()
    if key == speakerToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleJupiter0:
                ret = client.publish("vban/saturn/saturn/speakers/in", "false")
            if not toggleJupiter0:
                ret = client.publish("vban/saturn/saturn/speakers/in", "true")
    if key == headsetToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleJupiter1:
                ret = client.publish("vban/saturn/saturn/headset/in", "false")
            if not toggleJupiter1:
                ret = client.publish("vban/saturn/saturn/headset/in", "true")
    if key == bluetoothToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleJupiter2:
                ret = client.publish("vban/saturn/saturn/bluetooth-tx/in", "false")
            if not toggleJupiter2:
                ret = client.publish("vban/saturn/saturn/bluetooth-tx/in", "true")
    if key == broadcastToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleJupiter3:
                ret = client.publish("vban/saturn/saturn/broadcast/in", "false")
            if not toggleJupiter3:
                ret = client.publish("vban/saturn/saturn/broadcast/in", "true")
    if key == chatToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleJupiter4:
                ret = client.publish("vban/saturn/saturn/chat/in", "false")
            if not toggleJupiter4:
                ret = client.publish("vban/saturn/saturn/chat/in", "true")
    print(ret)


# sends MQTT packets for controlling "VBAN"
def key_change_callback_vban(deck, key, state):
    ret = ""
    # check for key
    if key == terraGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_terra)
            update_icons()
    if key == solarGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_solar)
            update_icons()
    if key == bluetoothGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_bluetooth)
            update_icons()
    if key == charonGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_charon)
            update_icons()
    if key == landsatGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_landsat)
            update_icons()
    if key == jupiterGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_jupiter)
            update_icons()
    if key == vbanGroup:
        if state:
            deck.set_key_callback(key_change_callback_default)
            # Update Icons
            update_icons()
    if key == dockGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_dock)
            update_icons()
    if key == speakerToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleVBAN0:
                ret = client.publish("vban/saturn/vban/speakers/in", "false")
            if not toggleVBAN0:
                ret = client.publish("vban/saturn/vban/speakers/in", "true")
    if key == headsetToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleVBAN1:
                ret = client.publish("vban/saturn/vban/headset/in", "false")
            if not toggleVBAN1:
                ret = client.publish("vban/saturn/vban/headset/in", "true")
    if key == bluetoothToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleVBAN2:
                ret = client.publish("vban/saturn/vban/bluetooth-tx/in", "false")
            if not toggleVBAN2:
                ret = client.publish("vban/saturn/vban/bluetooth-tx/in", "true")
    if key == broadcastToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleVBAN3:
                ret = client.publish("vban/saturn/vban/broadcast/in", "false")
            if not toggleVBAN3:
                ret = client.publish("vban/saturn/vban/broadcast/in", "true")
    if key == chatToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleVBAN4:
                ret = client.publish("vban/saturn/vban/chat/in", "false")
            if not toggleVBAN4:
                ret = client.publish("vban/saturn/vban/chat/in", "true")
    print(ret)


# sends MQTT packets for controlling "Dock"
def key_change_callback_dock(deck, key, state):
    ret = ""
    # check for key
    if key == terraGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_terra)
            update_icons()
    if key == solarGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_solar)
            update_icons()
    if key == bluetoothGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_bluetooth)
            update_icons()
    if key == charonGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_charon)
            update_icons()
    if key == landsatGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_landsat)
            update_icons()
    if key == jupiterGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_jupiter)
            update_icons()
    if key == vbanGroup:
        # check for state
        if state:
            # screen switching stuff
            deck.set_key_callback(key_change_callback_vban)
            update_icons()
    if key == dockGroup:
        if state:
            deck.set_key_callback(key_change_callback_default)
            # Update Icons
            update_icons()
    if key == speakerToggle:
        # check for state
        if state:
            print("0T")
            # check for global toggle
            if toggleDock0:
                ret = client.publish("vban/saturn/dock/speakers/in", "false")
            if not toggleDock0:
                ret = client.publish("vban/saturn/dock/speakers/in", "true")
    if key == headsetToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleDock1:
                ret = client.publish("vban/saturn/dock/headset/in", "false")
            if not toggleDock1:
                ret = client.publish("vban/saturn/dock/headset/in", "true")
    if key == bluetoothToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleDock2:
                ret = client.publish("vban/saturn/dock/bluetooth-tx/in", "false")
            if not toggleDock2:
                ret = client.publish("vban/saturn/dock/bluetooth-tx/in", "true")
    if key == broadcastToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleDock3:
                ret = client.publish("vban/saturn/dock/broadcast/in", "false")
            if not toggleDock3:
                ret = client.publish("vban/saturn/dock/broadcast/in", "true")
    if key == chatToggle:
        # check for state
        if state:
            # check for global toggle
            if toggleDock4:
                ret = client.publish("vban/saturn/dock/chat/in", "false")
            if not toggleDock4:
                ret = client.publish("vban/saturn/dock/chat/in", "true")
    print(ret)


# Create function for publishing callback
def on_publish(client, userdata, result):
    print("data published \n")
    pass


# Create function for receiving messages
def on_message(client, userdata, message):
    # Import global variables
    # Terra
    global toggleTerra0
    global toggleTerra1
    global toggleTerra2
    global toggleTerra3
    global toggleTerra4
    # Solar
    global toggleSolar0
    global toggleSolar1
    global toggleSolar2
    global toggleSolar3
    global toggleSolar4
    # Bluetooth
    global toggleBluetooth0
    global toggleBluetooth1
    global toggleBluetooth2
    global toggleBluetooth3
    global toggleBluetooth4
    # Charon
    global toggleCharon0
    global toggleCharon1
    global toggleCharon2
    global toggleCharon3
    global toggleCharon4
    # Landsat
    global toggleLandsat0
    global toggleLandsat1
    global toggleLandsat2
    global toggleLandsat3
    global toggleLandsat4
    # Jupiter
    global toggleJupiter0
    global toggleJupiter1
    global toggleJupiter2
    global toggleJupiter3
    global toggleJupiter4
    # VBAN
    global toggleVBAN0
    global toggleVBAN1
    global toggleVBAN2
    global toggleVBAN3
    global toggleVBAN4
    # Dock
    global toggleDock0
    global toggleDock1
    global toggleDock2
    global toggleDock3
    global toggleDock4

    # Translate message.payload into UTF-8
    msg = str(message.payload.decode("utf-8"))
    # print(message.topic)
    # print(msg)

    # System
    if message.topic == "lighting/ottos-room/stream-deck/brightness/out":
        deck.set_brightness(int(msg))

    # Terra
    if message.topic == "vban/saturn/terra/gain/out":
        # check for payload
        print("Gain")
    if message.topic == "vban/saturn/terra/speakers/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleTerra0 = True
        if msg == "false":
            # change global toggle variable
            toggleTerra0 = False
    if message.topic == "vban/saturn/terra/headset/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleTerra1 = True
        if msg == "false":
            # change global toggle variable
            toggleTerra1 = False
    if message.topic == "vban/saturn/terra/bluetooth-tx/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleTerra2 = True
        if msg == "false":
            # change global toggle variable
            toggleTerra2 = False
    if message.topic == "vban/saturn/terra/broadcast/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleTerra3 = True
        if msg == "false":
            # change global toggle variable
            toggleTerra3 = False
    if message.topic == "vban/saturn/terra/chat/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleTerra4 = True
        if msg == "false":
            # change global toggle variable
            toggleTerra4 = False

    # Solar
    if message.topic == "vban/saturn/solar/gain/out":
        # check for payload
        print("Gain")
    if message.topic == "vban/saturn/solar/speakers/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleSolar0 = True
        if msg == "false":
            # change global toggle variable
            toggleSolar0 = False
    if message.topic == "vban/saturn/solar/headset/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleSolar1 = True
        if msg == "false":
            # change global toggle variable
            toggleSolar1 = False
    if message.topic == "vban/saturn/solar/bluetooth-tx/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleSolar2 = True
        if msg == "false":
            # change global toggle variable
            toggleSolar2 = False
    if message.topic == "vban/saturn/solar/broadcast/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleSolar3 = True
        if msg == "false":
            # change global toggle variable
            toggleSolar3 = False
    if message.topic == "vban/saturn/solar/chat/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleSolar4 = True
        if msg == "false":
            # change global toggle variable
            toggleSolar4 = False

    # Bluetooth
    if message.topic == "vban/saturn/bluetooth-rx/gain/out":
        # check for payload
        print("Gain")
    if message.topic == "vban/saturn/bluetooth-rx/speakers/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleBluetooth0 = True
        if msg == "false":
            # change global toggle variable
            toggleBluetooth0 = False
    if message.topic == "vban/saturn/bluetooth-rx/headset/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleBluetooth1 = True
        if msg == "false":
            # change global toggle variable
            toggleBluetooth1 = False
    if message.topic == "vban/saturn/bluetooth-rx/bluetooth-tx/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleBluetooth2 = True
        if msg == "false":
            # change global toggle variable
            toggleBluetooth2 = False
    if message.topic == "vban/saturn/bluetooth-rx/broadcast/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleBluetooth3 = True
        if msg == "false":
            # change global toggle variable
            toggleBluetooth3 = False
    if message.topic == "vban/saturn/bluetooth-rx/chat/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleBluetooth4 = True
        if msg == "false":
            # change global toggle variable
            toggleBluetooth4 = False

    # Charon
    if message.topic == "vban/saturn/charon/gain/out":
        # check for payload
        print("Gain")
    if message.topic == "vban/saturn/charon/speakers/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleCharon0 = True
        if msg == "false":
            # change global toggle variable
            toggleCharon0 = False
    if message.topic == "vban/saturn/charon/headset/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleCharon1 = True
        if msg == "false":
            # change global toggle variable
            toggleCharon1 = False
    if message.topic == "vban/saturn/charon/bluetooth-tx/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleCharon2 = True
        if msg == "false":
            # change global toggle variable
            toggleCharon2 = False
    if message.topic == "vban/saturn/charon/broadcast/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleCharon3 = True
        if msg == "false":
            # change global toggle variable
            toggleCharon3 = False
    if message.topic == "vban/saturn/charon/chat/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleCharon4 = True
        if msg == "false":
            # change global toggle variable
            toggleCharon4 = False

    # Landsat
    if message.topic == "vban/saturn/landsat/gain/out":
        # check for payload
        print("Gain")
    if message.topic == "vban/saturn/landsat/speakers/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleLandsat0 = True
        if msg == "false":
            # change global toggle variable
            toggleLandsat0 = False
    if message.topic == "vban/saturn/landsat/headset/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleLandsat1 = True
        if msg == "false":
            # change global toggle variable
            toggleLandsat1 = False
    if message.topic == "vban/saturn/landsat/bluetooth-tx/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleLandsat2 = True
        if msg == "false":
            # change global toggle variable
            toggleLandsat2 = False
    if message.topic == "vban/saturn/landsat/broadcast/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleLandsat3 = True
        if msg == "false":
            # change global toggle variable
            toggleLandsat3 = False
    if message.topic == "vban/saturn/landsat/chat/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleLandsat4 = True
        if msg == "false":
            # change global toggle variable
            toggleLandsat4 = False

    # Jupiter
    if message.topic == "vban/saturn/saturn/gain/out":
        # check for payload
        print("Gain")
    if message.topic == "vban/saturn/saturn/speakers/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleJupiter0 = True
        if msg == "false":
            # change global toggle variable
            toggleJupiter0 = False
    if message.topic == "vban/saturn/saturn/headset/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleJupiter1 = True
        if msg == "false":
            # change global toggle variable
            toggleJupiter1 = False
    if message.topic == "vban/saturn/saturn/bluetooth-tx/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleJupiter2 = True
        if msg == "false":
            # change global toggle variable
            toggleJupiter2 = False
    if message.topic == "vban/saturn/saturn/broadcast/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleJupiter3 = True
        if msg == "false":
            # change global toggle variable
            toggleJupiter3 = False
    if message.topic == "vban/saturn/saturn/chat/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleJupiter4 = True
        if msg == "false":
            # change global toggle variable
            toggleJupiter4 = False

    # VBAN
    if message.topic == "vban/saturn/vban/gain/out":
        # check for payload
        print("Gain")
    if message.topic == "vban/saturn/vban/speakers/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleVBAN0 = True
        if msg == "false":
            # change global toggle variable
            toggleVBAN0 = False
    if message.topic == "vban/saturn/vban/headset/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleVBAN1 = True
        if msg == "false":
            # change global toggle variable
            toggleVBAN1 = False
    if message.topic == "vban/saturn/vban/bluetooth-tx/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleVBAN2 = True
        if msg == "false":
            # change global toggle variable
            toggleVBAN2 = False
    if message.topic == "vban/saturn/vban/broadcast/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleVBAN3 = True
        if msg == "false":
            # change global toggle variable
            toggleVBAN3 = False
    if message.topic == "vban/saturn/vban/chat/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleVBAN4 = True
        if msg == "false":
            # change global toggle variable
            toggleVBAN4 = False

    # Dock
    if message.topic == "vban/saturn/dock/gain/out":
        # check for payload
        print("Gain")
    if message.topic == "vban/saturn/dock/speakers/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleDock0 = True
        if msg == "false":
            # change global toggle variable
            toggleDock0 = False
    if message.topic == "vban/saturn/dock/headset/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleDock1 = True
        if msg == "false":
            # change global toggle variable
            toggleDock1 = False
    if message.topic == "vban/saturn/dock/bluetooth-tx/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleDock2 = True
        if msg == "false":
            # change global toggle variable
            toggleDock2 = False
    if message.topic == "vban/saturn/dock/broadcast/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleDock3 = True
        if msg == "false":
            # change global toggle variable
            toggleDock3 = False
    if message.topic == "vban/saturn/dock/chat/out":
        # check for payload
        if msg == "true":
            # change global toggle variable
            toggleDock4 = True
        if msg == "false":
            # change global toggle variable
            toggleDock4 = False

    # Update Icons
    update_icons()


# Create function for updating icons
def update_icons():
    # print("Updating Icons, Callback:", deck.key_callback)

    # Context = Default
    if deck.key_callback == key_change_callback_default:
        # print("Default Match!")
        for key in range(deck.key_count()):
            if key == terraGroup:
                update_key_image(deck, terraGroup, "desktop-classic.png", "Terra", colorInactive)
            elif key == solarGroup:
                update_key_image(deck, solarGroup, "monitor.png", "Solar", colorInactive)
            elif key == bluetoothGroup:
                update_key_image(deck, bluetoothGroup, "bluetooth.png", "Bluetooth", colorInactive)
            elif key == charonGroup:
                update_key_image(deck, charonGroup, "amazon-alexa.png", "Charon", colorInactive)
            elif key == landsatGroup:
                update_key_image(deck, landsatGroup, "home-heart.png", "Landsat", colorInactive)
            elif key == jupiterGroup:
                update_key_image(deck, jupiterGroup, "desktop-tower.png", "Jupiter", colorInactive)
            elif key == vbanGroup:
                update_key_image(deck, vbanGroup, "access-point-network.png", "VBAN", colorInactive)
            elif key == dockGroup:
                update_key_image(deck, dockGroup, "cellphone-android.png", "Dock", colorInactive)
            elif key == resetEngineKey:
                update_key_image(deck, resetEngineKey, "engine.png", "Reset", colorInactive)
            else:
                update_key_image(deck, key, "blank.png", "", colorInactive)
            # Context = Terra
    if deck.key_callback == key_change_callback_terra:
        # print("Terra Match!")
        for key in range(deck.key_count()):
            if key == terraGroup:
                update_key_image(deck, terraGroup, "SELECTED_desktop-classic.png", "Terra", colorActive)
            elif key == solarGroup:
                update_key_image(deck, solarGroup, "monitor.png", "Solar", colorInactive)
            elif key == bluetoothGroup:
                update_key_image(deck, bluetoothGroup, "bluetooth.png", "Bluetooth", colorInactive)
            elif key == charonGroup:
                update_key_image(deck, charonGroup, "amazon-alexa.png", "Charon", colorInactive)
            elif key == landsatGroup:
                update_key_image(deck, landsatGroup, "home-heart.png", "Landsat", colorInactive)
            elif key == jupiterGroup:
                update_key_image(deck, jupiterGroup, "desktop-tower.png", "Jupiter", colorInactive)
            elif key == vbanGroup:
                update_key_image(deck, vbanGroup, "access-point-network.png", "VBAN", colorInactive)
            elif key == dockGroup:
                update_key_image(deck, dockGroup, "cellphone-android.png", "Dock", colorInactive)
            elif key == speakerToggle:
                if toggleTerra0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker.png", "", colorInactive)
                elif not toggleTerra0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker-off.png", "", colorInactive)
            elif key == headsetToggle:
                if toggleTerra1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones.png", "", colorInactive)
                elif not toggleTerra1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones-off.png", "", colorInactive)
            elif key == bluetoothToggle:
                if toggleTerra2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth.png", "", colorInactive)
                elif not toggleTerra2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth-off.png", "", colorInactive)
            elif key == broadcastToggle:
                if toggleTerra3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network.png", "", colorInactive)
                elif not toggleTerra3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network-off.png", "", colorInactive)
            elif key == chatToggle:
                if toggleTerra4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat.png", "", colorInactive)
                elif not toggleTerra4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat-off.png", "", colorInactive)
            else:
                update_key_image(deck, key, "blank.png", "", colorInactive)

    # Context = Solar
    if deck.key_callback == key_change_callback_solar:
        # print("Solar Match!")
        for key in range(deck.key_count()):
            if key == terraGroup:
                update_key_image(deck, terraGroup, "desktop-classic.png", "Terra", colorInactive)
            elif key == solarGroup:
                update_key_image(deck, solarGroup, "SELECTED_monitor.png", "Solar", colorActive)
            elif key == bluetoothGroup:
                update_key_image(deck, bluetoothGroup, "bluetooth.png", "Bluetooth", colorInactive)
            elif key == charonGroup:
                update_key_image(deck, charonGroup, "amazon-alexa.png", "Charon", colorInactive)
            elif key == landsatGroup:
                update_key_image(deck, landsatGroup, "home-heart.png", "Landsat", colorInactive)
            elif key == jupiterGroup:
                update_key_image(deck, jupiterGroup, "desktop-tower.png", "Jupiter", colorInactive)
            elif key == vbanGroup:
                update_key_image(deck, vbanGroup, "access-point-network.png", "VBAN", colorInactive)
            elif key == dockGroup:
                update_key_image(deck, dockGroup, "cellphone-android.png", "Dock", colorInactive)
            elif key == speakerToggle:
                if toggleSolar0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker.png", "", colorInactive)
                elif not toggleSolar0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker-off.png", "", colorInactive)
            elif key == headsetToggle:
                if toggleSolar1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones.png", "", colorInactive)
                elif not toggleSolar1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones-off.png", "", colorInactive)
            elif key == bluetoothToggle:
                if toggleSolar2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth.png", "", colorInactive)
                elif not toggleSolar2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth-off.png", "", colorInactive)
            elif key == broadcastToggle:
                if toggleSolar3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network.png", "", colorInactive)
                elif not toggleSolar3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network-off.png", "", colorInactive)
            elif key == chatToggle:
                if toggleSolar4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat.png", "", colorInactive)
                elif not toggleSolar4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat-off.png", "", colorInactive)
            else:
                update_key_image(deck, key, "blank.png", "", colorInactive)

    # Context = Bluetooth
    if deck.key_callback == key_change_callback_bluetooth:
        # print("Bluetooth Match!")
        for key in range(deck.key_count()):
            if key == terraGroup:
                update_key_image(deck, terraGroup, "desktop-classic.png", "Terra", colorInactive)
            elif key == solarGroup:
                update_key_image(deck, solarGroup, "monitor.png", "Solar", colorInactive)
            elif key == bluetoothGroup:
                update_key_image(deck, bluetoothGroup, "SELECTED_bluetooth.png", "Bluetooth", colorActive)
            elif key == charonGroup:
                update_key_image(deck, charonGroup, "amazon-alexa.png", "Charon", colorInactive)
            elif key == landsatGroup:
                update_key_image(deck, landsatGroup, "home-heart.png", "Landsat", colorInactive)
            elif key == jupiterGroup:
                update_key_image(deck, jupiterGroup, "desktop-tower.png", "Jupiter", colorInactive)
            elif key == vbanGroup:
                update_key_image(deck, vbanGroup, "access-point-network.png", "VBAN", colorInactive)
            elif key == dockGroup:
                update_key_image(deck, dockGroup, "cellphone-android.png", "Dock", colorInactive)
            elif key == speakerToggle:
                if toggleBluetooth0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker.png", "", colorInactive)
                elif not toggleBluetooth0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker-off.png", "", colorInactive)
            elif key == headsetToggle:
                if toggleBluetooth1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones.png", "", colorInactive)
                elif not toggleBluetooth1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones-off.png", "", colorInactive)
            elif key == bluetoothToggle:
                if toggleBluetooth2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth.png", "", colorInactive)
                elif not toggleBluetooth2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth-off.png", "", colorInactive)
            elif key == broadcastToggle:
                if toggleBluetooth3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network.png", "", colorInactive)
                elif not toggleBluetooth3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network-off.png", "", colorInactive)
            elif key == chatToggle:
                if toggleBluetooth4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat.png", "", colorInactive)
                elif not toggleBluetooth4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat-off.png", "", colorInactive)
            else:
                update_key_image(deck, key, "blank.png", "", colorInactive)

    # Context = Charon
    if deck.key_callback == key_change_callback_charon:
        # print("Charon Match!")
        for key in range(deck.key_count()):
            if key == terraGroup:
                update_key_image(deck, terraGroup, "desktop-classic.png", "Terra", colorInactive)
            elif key == solarGroup:
                update_key_image(deck, solarGroup, "monitor.png", "Solar", colorInactive)
            elif key == bluetoothGroup:
                update_key_image(deck, bluetoothGroup, "bluetooth.png", "Bluetooth", colorInactive)
            elif key == charonGroup:
                update_key_image(deck, charonGroup, "SELECTED_amazon-alexa.png", "Charon", colorActive)
            elif key == landsatGroup:
                update_key_image(deck, landsatGroup, "home-heart.png", "Landsat", colorInactive)
            elif key == jupiterGroup:
                update_key_image(deck, jupiterGroup, "desktop-tower.png", "Jupiter", colorInactive)
            elif key == vbanGroup:
                update_key_image(deck, vbanGroup, "access-point-network.png", "VBAN", colorInactive)
            elif key == dockGroup:
                update_key_image(deck, dockGroup, "cellphone-android.png", "Dock", colorInactive)
            elif key == speakerToggle:
                if toggleCharon0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker.png", "", colorInactive)
                elif not toggleCharon0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker-off.png", "", colorInactive)
            elif key == headsetToggle:
                if toggleCharon1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones.png", "", colorInactive)
                elif not toggleCharon1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones-off.png", "", colorInactive)
            elif key == bluetoothToggle:
                if toggleCharon2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth.png", "", colorInactive)
                elif not toggleCharon2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth-off.png", "", colorInactive)
            elif key == broadcastToggle:
                if toggleCharon3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network.png", "", colorInactive)
                elif not toggleCharon3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network-off.png", "", colorInactive)
            elif key == chatToggle:
                if toggleCharon4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat.png", "", colorInactive)
                elif not toggleCharon4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat-off.png", "", colorInactive)
            else:
                update_key_image(deck, key, "blank.png", "", colorInactive)

    # Context = Landsat
    if deck.key_callback == key_change_callback_landsat:
        # print("Landsat Match!")
        for key in range(deck.key_count()):
            if key == terraGroup:
                update_key_image(deck, terraGroup, "desktop-classic.png", "Terra", colorInactive)
            elif key == solarGroup:
                update_key_image(deck, solarGroup, "monitor.png", "Solar", colorInactive)
            elif key == bluetoothGroup:
                update_key_image(deck, bluetoothGroup, "bluetooth.png", "Bluetooth", colorInactive)
            elif key == charonGroup:
                update_key_image(deck, charonGroup, "amazon-alexa.png", "Charon", colorInactive)
            elif key == landsatGroup:
                update_key_image(deck, landsatGroup, "SELECTED_home-heart.png", "Landsat", colorActive)
            elif key == jupiterGroup:
                update_key_image(deck, jupiterGroup, "desktop-tower.png", "Jupiter", colorInactive)
            elif key == vbanGroup:
                update_key_image(deck, vbanGroup, "access-point-network.png", "VBAN", colorInactive)
            elif key == dockGroup:
                update_key_image(deck, dockGroup, "cellphone-android.png", "Dock", colorInactive)
            elif key == speakerToggle:
                if toggleLandsat0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker.png", "", colorInactive)
                elif not toggleLandsat0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker-off.png", "", colorInactive)
            elif key == headsetToggle:
                if toggleLandsat1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones.png", "", colorInactive)
                elif not toggleLandsat1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones-off.png", "", colorInactive)
            elif key == bluetoothToggle:
                if toggleLandsat2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth.png", "", colorInactive)
                elif not toggleLandsat2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth-off.png", "", colorInactive)
            elif key == broadcastToggle:
                if toggleLandsat3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network.png", "", colorInactive)
                elif not toggleLandsat3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network-off.png", "", colorInactive)
            elif key == chatToggle:
                if toggleLandsat4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat.png", "", colorInactive)
                elif not toggleLandsat4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat-off.png", "", colorInactive)
            else:
                update_key_image(deck, key, "blank.png", "", colorInactive)

    # Context = Jupiter
    if deck.key_callback == key_change_callback_jupiter:
        # print("Jupiter Match!")
        for key in range(deck.key_count()):
            if key == terraGroup:
                update_key_image(deck, terraGroup, "desktop-classic.png", "Terra", colorInactive)
            elif key == solarGroup:
                update_key_image(deck, solarGroup, "monitor.png", "Solar", colorInactive)
            elif key == bluetoothGroup:
                update_key_image(deck, bluetoothGroup, "bluetooth.png", "Bluetooth", colorInactive)
            elif key == charonGroup:
                update_key_image(deck, charonGroup, "amazon-alexa.png", "Charon", colorInactive)
            elif key == landsatGroup:
                update_key_image(deck, landsatGroup, "home-heart.png", "Landsat", colorInactive)
            elif key == jupiterGroup:
                update_key_image(deck, jupiterGroup, "SELECTED_desktop-tower.png", "Jupiter", colorActive)
            elif key == vbanGroup:
                update_key_image(deck, vbanGroup, "access-point-network.png", "VBAN", colorInactive)
            elif key == dockGroup:
                update_key_image(deck, dockGroup, "cellphone-android.png", "Dock", colorInactive)
            elif key == speakerToggle:
                if toggleJupiter0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker.png", "", colorInactive)
                elif not toggleJupiter0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker-off.png", "", colorInactive)
            elif key == headsetToggle:
                if toggleJupiter1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones.png", "", colorInactive)
                elif not toggleJupiter1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones-off.png", "", colorInactive)
            elif key == bluetoothToggle:
                if toggleJupiter2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth.png", "", colorInactive)
                elif not toggleJupiter2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth-off.png", "", colorInactive)
            elif key == broadcastToggle:
                if toggleJupiter3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network.png", "", colorInactive)
                elif toggleJupiter3 == False:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network-off.png", "", colorInactive)
            elif key == chatToggle:
                if toggleJupiter4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat.png", "", colorInactive)
                elif not toggleJupiter4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat-off.png", "", colorInactive)
            else:
                update_key_image(deck, key, "blank.png", "", colorInactive)

    # Context = VBAN
    if deck.key_callback == key_change_callback_vban:
        # print("VBAN Match!")
        for key in range(deck.key_count()):
            if key == terraGroup:
                update_key_image(deck, terraGroup, "desktop-classic.png", "Terra", colorInactive)
            elif key == solarGroup:
                update_key_image(deck, solarGroup, "monitor.png", "Solar", colorInactive)
            elif key == bluetoothGroup:
                update_key_image(deck, bluetoothGroup, "bluetooth.png", "Bluetooth", colorInactive)
            elif key == charonGroup:
                update_key_image(deck, charonGroup, "amazon-alexa.png", "Charon", colorInactive)
            elif key == landsatGroup:
                update_key_image(deck, landsatGroup, "home-heart.png", "Landsat", colorInactive)
            elif key == jupiterGroup:
                update_key_image(deck, jupiterGroup, "desktop-tower.png", "Jupiter", colorInactive)
            elif key == vbanGroup:
                update_key_image(deck, vbanGroup, "SELECTED_access-point-network.png", "VBAN", colorActive)
            elif key == dockGroup:
                update_key_image(deck, dockGroup, "cellphone-android.png", "Dock", colorInactive)
            elif key == speakerToggle:
                if toggleVBAN0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker.png", "", colorInactive)
                elif not toggleVBAN0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker-off.png", "", colorInactive)
            elif key == headsetToggle:
                if toggleVBAN1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones.png", "", colorInactive)
                elif not toggleVBAN1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones-off.png", "", colorInactive)
            elif key == bluetoothToggle:
                if toggleVBAN2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth.png", "", colorInactive)
                elif not toggleVBAN2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth-off.png", "", colorInactive)
            elif key == broadcastToggle:
                if toggleVBAN3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network.png", "", colorInactive)
                elif not toggleVBAN3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network-off.png", "", colorInactive)
            elif key == chatToggle:
                if toggleVBAN4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat.png", "", colorInactive)
                elif not toggleVBAN4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat-off.png", "", colorInactive)
            else:
                update_key_image(deck, key, "blank.png", "", colorInactive)

    # Context = Dock
    if deck.key_callback == key_change_callback_dock:
        # print("Dock Match!")
        for key in range(deck.key_count()):
            if key == terraGroup:
                update_key_image(deck, terraGroup, "desktop-classic.png", "Terra", colorInactive)
            elif key == solarGroup:
                update_key_image(deck, solarGroup, "monitor.png", "Solar", colorInactive)
            elif key == bluetoothGroup:
                update_key_image(deck, bluetoothGroup, "bluetooth.png", "Bluetooth", colorInactive)
            elif key == charonGroup:
                update_key_image(deck, charonGroup, "amazon-alexa.png", "Charon", colorInactive)
            elif key == landsatGroup:
                update_key_image(deck, landsatGroup, "home-heart.png", "Landsat", colorInactive)
            elif key == jupiterGroup:
                update_key_image(deck, jupiterGroup, "desktop-tower.png", "Jupiter", colorInactive)
            elif key == vbanGroup:
                update_key_image(deck, vbanGroup, "access-point-network.png", "VBAN", colorInactive)
            elif key == dockGroup:
                update_key_image(deck, dockGroup, "SELECTED_cellphone-android.png", "Dock", colorActive)
            elif key == speakerToggle:
                if toggleDock0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker.png", "", colorInactive)
                elif not toggleDock0:
                    # change StreamDeck image
                    update_key_image(deck, speakerToggle, "speaker-off.png", "", colorInactive)
            elif key == headsetToggle:
                if toggleDock1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones.png", "", colorInactive)
                elif not toggleDock1:
                    # change StreamDeck image
                    update_key_image(deck, headsetToggle, "headphones-off.png", "", colorInactive)
            elif key == bluetoothToggle:
                if toggleDock2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth.png", "", colorInactive)
                elif not toggleDock2:
                    # change StreamDeck image
                    update_key_image(deck, bluetoothToggle, "bluetooth-off.png", "", colorInactive)
            elif key == broadcastToggle:
                if toggleDock3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network.png", "", colorInactive)
                elif not toggleDock3:
                    # change StreamDeck image
                    update_key_image(deck, broadcastToggle, "access-point-network-off.png", "", colorInactive)
            elif key == chatToggle:
                if toggleDock4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat.png", "", colorInactive)
                elif not toggleDock4:
                    # change StreamDeck image
                    update_key_image(deck, chatToggle, "repeat-off.png", "", colorInactive)
            else:
                update_key_image(deck, key, "blank.png", "", colorInactive)
    # print("Updating Icons done")


if __name__ == "__main__":
    # MQTT broker Settings
    broker = "192.169.4.5"
    port = 1883

    # Create MQTT client
    client = mqtt.Client("control1")

    # Assign on methods
    client.on_publish = on_publish
    client.on_message = on_message

    # Connect to broker
    client.connect(broker, port)

    # Start the loop
    client.loop_start()

    # Find StreamDeck
    streamdecks = DeviceManager().enumerate()
    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    # Subscribe to System Topics
    client.subscribe("lighting/ottos-room/stream-deck/brightness/out")

    # Subscribe to VBAN Topics
    client.subscribe("vban/saturn/#")

    # Initialize StreamDecks
    for index, deck in enumerate(streamdecks):
        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}')".format(deck.deck_type(), deck.get_serial_number()))

        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback_default)

        update_icons()

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            if t is threading.currentThread():
                continue

            if t.is_alive():
                t.join()
