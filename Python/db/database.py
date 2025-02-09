import sqlite3
import Python.logic.ferret as ferret

from paho import mqtt
from sqlite3 import Error


# Funktionen zum verbinden mit einer Datenbank


def create_connection(db_file):
    """ Erstellt/verbindet sich mit der Datenbank und gibt diese verbindung zurück"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        execute_sql(conn, "PRAGMA foreign_keys = ON")
        return conn
    except Error as e:
        print(e)

    return conn


# Funktionen zum ausfuehren eines SQL strinbgs auf einer Datenbank
def execute_sql(conn, sql_string):
    """ Führt SQL-Statements aus
    :param conn: Verbindung zur DB
    :param sql_string: SQL-Statement
    :return: Nothing
    """
    try:
        cur = conn.cursor()
        cur.execute(sql_string)
        conn.commit()

        return cur.fetchall()
    except Error as e:
        print(e)


# Funktionen zum erstellen der Tabellen in der Datenbank
def create_tables(conn):
    """
    Erstellen einer Datenbank mit Tabellen zum Speichern für ausfälle
    :param db_file:
    """

    # Deck Tabelle
    sql_create_decks_table = """ CREATE TABLE IF NOT EXISTS decks (
                                            serial text PRIMARY KEY,
                                            current_view_name text
                                        ); """

    # View Tabelle
    sql_create_views_table = """ CREATE TABLE IF NOT EXISTS views (
                                            name text PRIMARY KEY,
                                            deck_serial text,
                                            FOREIGN KEY (deck_serial) REFERENCES decks (serial) 
                                            ON DELETE CASCADE
                                        ); """

    # Key Tabelle
    sql_create_keys_table = """CREATE TABLE IF NOT EXISTS keys (
                                    id integer PRIMARY KEY,
                                    name text,
                                    icon_path text,
                                    label text,
                                    view_name text NOT NULL,
                                    FOREIGN KEY (view_name) REFERENCES views (name) 
                                    ON DELETE CASCADE
                                );"""

    # Actions

    # Action Tabelle
    sql_create_actions_table = """ CREATE TABLE IF NOT EXISTS actions (
                                            id integer PRIMARY KEY,
                                            type text,
                                            key_id integer NOT NULL,
                                            FOREIGN KEY (key_id) REFERENCES keys (id) 
                                            ON DELETE CASCADE
                                        ); """

    # MQTT-Action Tabelle
    sql_create_mqtt_action_table = """ CREATE TABLE IF NOT EXISTS mqtt_actions (
                                            id integer PRIMARY KEY,
                                            client text,
                                            topic text,
                                            payload text,
                                            action_id integer NOT NULL,
                                            FOREIGN KEY (action_id) REFERENCES actions (id) ON DELETE CASCADE
                                        ); """

    # View_Action Tabelle
    sql_create_view_action_table = """ CREATE TABLE IF NOT EXISTS view_actions (
                                            id integer PRIMARY KEY,
                                            view_name text,
                                            action_id integer NOT NULL,
                                            FOREIGN KEY (view_name) REFERENCES views (name),
                                            FOREIGN KEY (action_id) REFERENCES actions (id) ON DELETE CASCADE
                                        ); """

    # MQTT Toggle Tabelle
    sql_create_mqtt_toggle_table = """ CREATE TABLE IF NOT EXISTS mqtt_toggles (
                                            id integer PRIMARY KEY,
                                            topic text,
                                            payload text,
                                            action_id integer NOT NULL,
                                            FOREIGN KEY (action_id) REFERENCES actions (id) ON DELETE CASCADE
                                        ); """

    # MQTT Clients
    sql_create_mqtt_clients_table = """ CREATE TABLE IF NOT EXISTS  mqtt_clients (
                                                        id integer PRIMARY KEY,
                                                        client_name text,
                                                        broker text,
                                                        port int,
                                                        action_id integer NOT NULL,
                                                        FOREIGN KEY (action_id) REFERENCES actions (id) ON DELETE CASCADE
                                                    ); """

    # DICS

    sql_create_dic_icons_table = """ CREATE TABLE IF NOT EXISTS  dic_icons (
                                                id integer PRIMARY KEY,
                                                icon text,
                                                state text,
                                                action_id integer NOT NULL,
                                                FOREIGN KEY (action_id) REFERENCES actions (id) ON DELETE CASCADE
                                            ); """

    # DIC_Labels Tabelle
    sql_create_dic_labels_table = """ CREATE TABLE IF NOT EXISTS  dic_labels (
                                                id integer PRIMARY KEY,
                                                label text,
                                                state text,
                                                action_id integer NOT NULL,
                                                FOREIGN KEY (action_id) REFERENCES actions (id) ON DELETE CASCADE
                                            ); """

    # DIC_Colors Tabelle
    sql_create_dic_colors_table = """ CREATE TABLE IF NOT EXISTS  dic_colors (
                                                    id integer PRIMARY KEY,
                                                    hexvalue text,
                                                    state text,
                                                    action_id integer NOT NULL,
                                                    FOREIGN KEY (action_id) REFERENCES actions (id) ON DELETE CASCADE
                                                ); """

    # Tabellen erstellen
    execute_sql(conn, sql_create_decks_table)
    execute_sql(conn, sql_create_views_table)
    execute_sql(conn, sql_create_keys_table)

    execute_sql(conn, sql_create_actions_table)
    execute_sql(conn, sql_create_mqtt_action_table)
    execute_sql(conn, sql_create_view_action_table)
    execute_sql(conn, sql_create_mqtt_toggle_table)

    execute_sql(conn, sql_create_mqtt_clients_table)

    execute_sql(conn, sql_create_dic_icons_table)
    execute_sql(conn, sql_create_dic_labels_table)
    execute_sql(conn, sql_create_dic_colors_table)


# Funktionen zum speichern in der Datenbank

# Funktionen zum resetten der Datenbank und die aktuellen Daten abzuspeichern
def update_data(deck, db_file):
    # DB Verbindung aufbauen /datenbank neu erstellen
    conn = create_connection(db_file)

    # Alle Tables neu aufsetzen
    create_tables(conn)

    # Deck Speichern
    save_deck(conn, deck)

    # Connection nach beendigen schließen
    conn.close()


# Funktionen zum speichern eines Decks
def save_deck(conn, streamdeck):
    # Zwischenspeichern der Seriennummer eines Decks
    serial = streamdeck.hardware.get_serial_number()

    # Falls ein Streamdeck, mit der Seriennummner schon vorhanden, ist dies löschenn
    sql_delete_deck = f"""DELETE FROM decks WHERE serial = '{serial}';"""
    execute_sql(conn, sql_delete_deck)

    # Streamdeck eintragen
    sql_insert_deck = f"""INSERT INTO decks (serial, current_view_name) VALUES("{serial}","{streamdeck.current_view.name}"); """
    execute_sql(conn, sql_insert_deck)

    # Views eintragen die im deck enthalten sind mit der save_view-Methode
    for view in streamdeck.views:
        save_view(conn, streamdeck.views[view], serial)


# Funktionen zum speichern eines Views
def save_view(conn, view, serial):
    # View eintragen
    sql_insert_view = f"""INSERT INTO views (name, deck_serial)VALUES("{view.name}","{serial}");"""
    execute_sql(conn, sql_insert_view)

    # Alle Keys von diesem View mit save_key-Methode eintragen
    for key in view.keys:
        save_key(conn, key, view.name)


# Funktionen zum speichern eines Keys
def save_key(conn, key, viewName):
    # Diesen Key eintragen
    sql_insert_key = f"""INSERT INTO keys(name, icon_path, label, view_name) VALUES("{key.name}","{key.image}","{key.label}","{viewName}");"""
    execute_sql(conn, sql_insert_key)

    # id vom Key abrufen
    id = execute_sql(conn, """SELECT MAX(id) from keys""")[0][0]

    # Action vom Key abspeichern
    save_action(conn, key.action, id)


# Funktionen zum speichern einer Action
def save_action(conn, action, keyID):
    name = ""

    # Bestimmen was es fuer ein Action ist
    if (type(action).__name__ == 'MqttAction'):
        name = "MQTT_Action"
    elif (type(action).__name__ == 'MqttToggle'):
        name = "MQTT_Toggle"
    elif (type(action).__name__ == 'ViewAction'):
        name = "View_Action"
    else:
        name = "None"
    # und demnach in Action eintragen
    sql_insert_action = f"""INSERT INTO actions(type,key_id) VALUES("{name}",{keyID});"""
    execute_sql(conn, sql_insert_action)

    # ID abrufen
    id = execute_sql(conn, """SELECT MAX(id) from actions;""")[0][0]

    # Je nach typ die passende Speichermethode aufrufen
    if (type(action).__name__ == 'MqttAction'):
        save_mqtt_action(conn, action, id)
    elif (type(action).__name__ == 'MqttToggle'):
        save_mqtt_toggle(conn, action, id)
    elif (type(action).__name__ == 'ViewAction'):
        save_view_action(conn, action, id)
    else:
        name = "None"


# Funktionen zum speichern einer View Action
def save_view_action(conn, view_action, actionID):
    # View Action eintragen
    sql_insert_view_action = f"""INSERT INTO view_actions (view_name,action_id) VALUES("{view_action.view}",{actionID});"""
    execute_sql(conn, sql_insert_view_action)


# Funktionen zum speichern einer MQTT Action
def save_mqtt_action(conn, mqtt_action, actionID):
    # MQTT Action eintragen
    sql_insert_mqtt_action = f"""INSERT INTO mqtt_actions (topic,payload,action_id) VALUES("{mqtt_action.topic}","{mqtt_action.payload}",{actionID});"""
    execute_sql(conn, sql_insert_mqtt_action)

    # Die Unteratribute in weitere listen speichern
    for x in mqtt_action.icons:
        save_icons(conn, mqtt_action.icons[x], x, actionID)
    for x in mqtt_action.labels:
        save_labels(conn, mqtt_action.labels[x], x, actionID)
    for x in mqtt_action.colors:
        save_colors(conn, mqtt_action.colors[x], x, actionID)


# Funktionen zum speichern eines MQTT Toggles
def save_mqtt_toggle(conn, mqtt_toggle, actionID):
    # MQTT Toggle eintragen
    sql_insert_mqtt_toggle = f"""INSERT INTO mqtt_toggles (topic,payload,action_id) VALUES("{mqtt_toggle.topic}","{mqtt_toggle.payload}",{actionID}); """
    execute_sql(conn, sql_insert_mqtt_toggle)

    # client abspeichern
    save_client(conn, mqtt_toggle.client, actionID)

    # Die Unteratribute in weitere listen speichern
    for x in mqtt_toggle.icons:
        save_icons(conn, mqtt_toggle.icons[x], x, actionID)
    for x in mqtt_toggle.labels:
        save_labels(conn, mqtt_toggle.labels[x], x, actionID)
    for x in mqtt_toggle.colors:
        save_colors(conn, mqtt_toggle.colors[x], x, actionID)


# Funktionen zum speichern eines Clients
def save_client(conn, client, actionID):
    # MQTT Client eintragen
    sql_insert_mqtt_client = f"""INSERT INTO mqtt_clients (client_name,broker,port,action_id) VALUES("{client._client_id.decode("utf-8")}","{client._host}","{client._port}",{actionID}); """
    execute_sql(conn, sql_insert_mqtt_client)


# Funktionen zum speichern eines Icon Dicts
def save_icons(conn, icon, state, actionID):
    # Icon Pfad und ihren dazu gehörigen Wert eintragen
    sql_insert_icons = f"""INSERT INTO dic_icons (icon,state,action_id) VALUES("{icon}","{state}",{actionID});"""
    execute_sql(conn, sql_insert_icons)


# Funktionen zum speichern eines Label Dicts
def save_labels(conn, label, state, actionID):
    # Labelinhalt und ihren dazu gehörigen Wert eintragen
    sql_insert_labels = f"""INSERT INTO dic_labels (label,state,action_id) VALUES("{label}","{state}",{actionID});"""
    execute_sql(conn, sql_insert_labels)


# Funktionen zum speichern eines Color Dicts
def save_colors(conn, color, state, actionID):
    # Farben und ihren dazu gehörigen Wert eintragen
    sql_insert_colors = f"""INSERT INTO dic_colors (hexvalue,state,action_id) VALUES("{color}","{state}",{actionID});"""
    execute_sql(conn, sql_insert_colors)


# Funktion zum abrufen der Daten aus der Datenbank

# Funktion zum abrufen der Daten zu einem Streamdeck
def load_deck(streamdeck, db_file):
    # Abrufen der Serial des Decks
    serial = streamdeck.get_serial_number()

    # Verbindung zur Datenbank erstellen
    conn = create_connection(db_file)

    # Deck aus der Datenbank laden
    sql_select_current_view = f"""SELECT current_view_name FROM decks WHERE serial = "{serial}" ;"""
    deck_db = execute_sql(conn, sql_select_current_view)

    # Ueberpruefen ob das Deck in der Datenbank existiert
    if (deck_db):
        # Basisdaten fuer das Deck
        base_current_view = ferret.View("basis", [])
        base_views = {}
        base_views["basis"] = base_current_view

        # initialisiren des decks mit Basisdaten
        deck = ferret.StreamDeck(streamdeck, base_views, base_current_view)

        # Derzeitige View aus deck nehmen
        current_view = deck_db[0][0]

        # Views vom deck laden mit Funktionsaufruf
        views = load_views(conn, deck, serial)

        # Ueberschreiben der Basisdaten im deck
        deck.views = views
        deck.current_view = views[current_view]

        # Verbindung Schließen
        conn.close()

        # Deck Objekt zurueck liefern
        return deck
    else:
        # Basic View erstellen
        current_view = "MainView"
        baseView = ferret.View(current_view, [])
        deck = ferret.StreamDeck(streamdeck, {}, baseView)
        deck.add_view(baseView)

        # Verbindung schließen
        conn.close()

        # leeres Object zurueck liefern
        return deck


# Funktion zum abrufen der Views von einem Deck
def load_views(conn, deck, serial):
    # Views aus Datenbank laden
    sql_select_views = f"""SELECT * FROM views WHERE deck_serial = "{serial}" ;"""
    selected_views = execute_sql(conn, sql_select_views)

    # Views Objekt initialisieren
    views = {}

    # Ueberpruefen ob Views in der Datenbank existieren
    if (selected_views):

        # Views objekt mit daten aus der Datenbank befuellen und Funktionsaufruf um die Keys zu laden
        for view in selected_views:
            view_name = view[0]
            keys = load_keys(conn, deck, view_name)
            views[view_name] = ferret.View(view_name, keys)

        # Views zurueck liefern
        return views

    # Leeres Views zurueck liefern
    else:
        return views


# Funktion zum abrufen der Keys eines Views
def load_keys(conn, deck, viewn_name):
    # Keys aus Datenbank laden
    sql_select_keys = f"""SELECT * FROM keys WHERE view_name = "{viewn_name}" ;"""
    selected_keys = execute_sql(conn, sql_select_keys)

    # Keys Objekt initialisieren
    keys = []
    position = 0

    # Ueberpruefen ob Keys in der Datenbank existieren
    if (selected_keys):
        # Keys objekt mit daten aus der Datenbank befuellen und Funktionsaufruf um die Actionen zu laden
        for key in selected_keys:
            key_name = key[1]
            key_icon = key[2]
            key_action = load_action(conn, deck, key[0])
            key_label = key[3]
            current_key = ferret.Key(key_name, key_icon, key_action, key_label)
            keys.insert(position, current_key)
            position += 1

        return keys

    # Leeres Keys zurueck liefern
    else:
        return keys


# Funktion zum abrufen einer Action eines Keys
def load_action(conn, deck, key_id):
    # Alle Actions aus der Datenbank abrufen
    sql_select_action = f"""SELECT * FROM actions WHERE key_id = {key_id} ;"""
    selected_action = execute_sql(conn, sql_select_action)[0]

    if (selected_action):
        # Action_id abrufen zum zwischen speichern
        action_id = selected_action[0]

        # Bestimmen was fuer eine Action es ist und je nach dem die richtige Funktion aufrufen
        if (selected_action[1] == "MQTT_Action"):
            return load_mqtt_action(conn, action_id)
        elif (selected_action[1] == "MQTT_Toggle"):
            return load_mqtt_toggle(conn, action_id)
        elif (selected_action[1] == "View_Action"):
            return load_view_action(conn, deck, action_id)
        elif (selected_action[1] == "None"):
            return ferret.Action()

    # Sonst einfaches Action Objekt zurueck liefern
    else:
        return ferret.Action()


# Funktion zum abrufen einer MQTT Action eines Keys
def load_mqtt_action(conn, action_id):
    # MQTT Action aus Datenbank abrufen
    sql_select_mqtt_action = f"""SELECT * FROM mqtt_actions WHERE action_id = {action_id} ;"""
    selected_mqtt_action = execute_sql(conn, sql_select_mqtt_action)

    # Attribute bestrimmen mit Daten aus Datenbank oder Funktionsaufruf um sie abzufragen
    topic = selected_mqtt_action[0][2]
    payload = selected_mqtt_action[0][3]
    icons = load_icons(conn, action_id)
    labels = load_labels(conn, action_id)
    colors = load_colors(conn, action_id)

    # MqttAction Objekt zurueck liefern
    return ferret.MqttAction( topic, payload, icons, labels, colors)


# Funktion zum abrufen eines MQTT Toggles eines Keys
def load_mqtt_toggle(conn, action_id):
    # MQTT Action aus Datenbank abrufen
    sql_select_mqtt_toggle = f"""SELECT * FROM mqtt_toggles WHERE action_id = {action_id} ;"""
    selected_mqtt_toggle = execute_sql(conn, sql_select_mqtt_toggle)

    # Attribute bestrimmen mit Daten aus Datenbank oder Funktionsaufruf um sie abzufragen
    topic = selected_mqtt_toggle[0][2]
    payload = selected_mqtt_toggle[0][3]
    icons = load_icons(conn, action_id)
    labels = load_labels(conn, action_id)
    colors = load_colors(conn, action_id)

    # MQTT Toggle Objekt zurueck liefern
    return ferret.MqttToggle( topic, payload, icons, labels, colors)


# Funktion zum abrufen einer View Action eines Keys
def load_view_action(conn, deck, action_id):
    # Abrufen der View zu der gewaechselt wird aus der Datenbank
    sql_select_view_action = f"""SELECT view_name FROM view_action WHERE action_id = {action_id} ;"""
    selected_view_action = execute_sql(conn, sql_select_view_action)

    # View name zwischenspeichern
    view_name = selected_view_action[0]

    # View Action Objekt zurueck liefern
    return ferret.ViewAction(deck, view_name)


# Funktion zum abrufen von Clients einer MQTT Action / Toggles
def load_client(conn, action_id):
    # Client abrufen von der Action aus der Datenbank
    sql_select_clients = f"""SELECT * FROM mqtt_clients WHERE action_id = {action_id} ;"""
    selected_client = execute_sql(conn, sql_select_clients)

    print(selected_client)
    if(selected_client):
        # Client erstellen und initialisieren
        client = mqtt.Client(selected_client[0][1])
        client.connect(selected_client[0][2], selected_client[0][3])

        # Client zurueck liefern
        return client
    else:
        return mqtt.Client()


# Funktion zum abrufen von Icons einer MQTT Action / Toggles
def load_icons(conn, action_id):
    # Alle Icons einer Action aus der Datenbank abrufen
    sql_select_icons = f"""SELECT * FROM dic_icons WHERE action_id = {action_id} ;"""
    selected_icons = execute_sql(conn, sql_select_icons)

    # Icons leer initialieren
    icons = {}

    # Wenn Icons in der Datenbank existieren diese in Icons legen
    if (selected_icons):
        for icon in selected_icons:
            icons[icon[2]] = icon[1]

    # Icons Dictionary zurueck liefern
    return icons


# Funktion zum abrufen von Labels einer MQTT Action / Toggles
def load_labels(conn, action_id):
    # Alle Labels einer Action aus der Datenbank abrufen
    sql_select_labels = f"""SELECT * FROM dic_labels WHERE action_id = {action_id} ;"""
    selected_labels = execute_sql(conn, sql_select_labels)

    # Labels leer initialieren
    labels = {}

    # Wenn Labels in der Datenbank existieren diese in Labels legen
    if (selected_labels):
        for label in selected_labels:
            labels[label[2]] = label[1]

    # Labels Dictionary zurueck liefern
    return labels


# Funktion zum abrufen von colors einer MQTT Action / Toggles
def load_colors(conn, action_id):
    # Alle Colors einer Action aus der Datenbank abrufen
    sql_select_colors = f"""SELECT * FROM dic_colors WHERE action_id = {action_id} ;"""
    selected_colors = execute_sql(conn, sql_select_colors)

    # Colors leer initialieren
    colors = {}

    # Wenn Colors in der Datenbank existieren diese in Colors legen
    if (selected_colors):
        for color in selected_colors:
            colors[color[2]] = color[1]

    # Colors Dictionary zurueck liefern
    return colors
