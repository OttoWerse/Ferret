import sqlite3
import os
from sqlite3 import Error


def create_connection(db_file):
    """ Erstellt/verbindet sich mit der Datenbank und gibt diese verbindung zurück"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


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


def create_tables(conn, db_file):
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
                                        ); """

    # Key Tabelle
    sql_create_keys_table = """CREATE TABLE IF NOT EXISTS keys (
                                    id integer PRIMARY KEY,
                                    name text,
                                    icon_path text,
                                    label text,
                                    view_name text NOT NULL,
                                    FOREIGN KEY (view_name) REFERENCES views (name)
                                );"""

    # Actions

    # Action Tabelle
    sql_create_actions_table = """ CREATE TABLE IF NOT EXISTS actions (
                                            id integer PRIMARY KEY,
                                            type text,
                                            key_id integer NOT NULL,
                                            FOREIGN KEY (key_id) REFERENCES keys (id)
                                        ); """

    # MQTT-Action Tabelle
    sql_create_mqtt_action_table = """ CREATE TABLE IF NOT EXISTS mqtt_actions (
                                            id integer PRIMARY KEY,
                                            client text,
                                            topic text,
                                            payload text,
                                            action_id integer NOT NULL,
                                            FOREIGN KEY (action_id) REFERENCES actions (id)
                                        ); """

    # View_Action Tabelle
    sql_create_view_action_table = """ CREATE TABLE IF NOT EXISTS view_actions (
                                            id integer PRIMARY KEY,
                                            view_name text,
                                            deck_serial text,
                                            action_id integer NOT NULL,
                                            FOREIGN KEY (deck_serial) REFERENCES decks (serial)
                                            FOREIGN KEY (view_name) REFERENCES views (name),
                                            FOREIGN KEY (action_id) REFERENCES actions (id)
                                        ); """

    sql_create_mqtt_toggle_table = """ CREATE TABLE IF NOT EXISTS mqtt_toggles (
                                            id integer PRIMARY KEY,
                                            client text,
                                            topic text,
                                            payload text,
                                            action_id integer NOT NULL,
                                            FOREIGN KEY (action_id) REFERENCES actions (id)
                                        ); """

    # DICS

    # DIC-Icons Tabelle
    sql_create_dic_icons_table = """ CREATE TABLE IF NOT EXISTS  dic_icons (
                                                id integer PRIMARY KEY,
                                                icon text,
                                                state text,
                                                actions_id integer NOT NULL,
                                                FOREIGN KEY (actions_id) REFERENCES actions (id)
                                            ); """

    # DIC_Labels Tabelle
    sql_create_dic_labels_table = """ CREATE TABLE IF NOT EXISTS  dic_labels (
                                                id integer PRIMARY KEY,
                                                label text,
                                                state text,
                                                actions_id integer NOT NULL,
                                                FOREIGN KEY (actions_id) REFERENCES actions (id)
                                            ); """

    # DIC_Colors Tabelle
    sql_create_dic_colors_table = """ CREATE TABLE IF NOT EXISTS  dic_colors (
                                                    id integer PRIMARY KEY,
                                                    hexvalue text,
                                                    state text,
                                                    actions_id integer NOT NULL,
                                                    FOREIGN KEY (actions_id) REFERENCES actions (id)
                                                ); """

    # Tabellen erstellen
    execute_sql(conn, sql_create_decks_table)
    execute_sql(conn, sql_create_views_table)
    execute_sql(conn, sql_create_keys_table)

    execute_sql(conn, sql_create_actions_table)
    execute_sql(conn, sql_create_mqtt_action_table)
    execute_sql(conn, sql_create_view_action_table)
    execute_sql(conn, sql_create_mqtt_toggle_table)

    execute_sql(conn, sql_create_dic_icons_table)
    execute_sql(conn, sql_create_dic_labels_table)
    execute_sql(conn, sql_create_dic_colors_table)


def save_deck(streamdeck,  db_file):
    serial = streamdeck.hardware.get_serial_number()

    # Loeschen der alten datenbank
    os.remove(db_file)

    # DB Verbindung aufbauen
    conn = create_connection(db_file)

    # Alle Tables neu aufsetzen
    create_tables(conn, db_file)

    # Streamdeck eintragen
    sql_insert_deck = f"""INSERT INTO decks (serial, current_view_name) VALUES("{serial}","{streamdeck.current_view.name}"); """
    execute_sql(conn, sql_insert_deck)

    # Views eintragen die im deck enthalten sind mit der save_view-Methode
    for view in streamdeck.views:
        save_view(conn, streamdeck.views[view], serial)

    # Connection nach beendigen schließen
    conn.close()


def save_view(conn, view, deck_serial):
    # View eintragen
    sql_insert_view = f"""INSERT INTO views (name, deck_serial)VALUES("{view.name}","{deck_serial}");"""
    execute_sql(conn, sql_insert_view)

    # Alle Keys von diesem View mit save_key-Methode eintragen
    for key in view.keys:
        save_key(conn, key, view.name)


def save_key(conn, key, viewName):
    # Diesen Key eintragen
    sql_insert_key = f"""INSERT INTO keys(name, icon_path, label, view_name) VALUES("{key.name}","{key.image}","{key.label}","{viewName}");"""
    execute_sql(conn, sql_insert_key)

    # id vom Key abrufen
    id = execute_sql(conn, """SELECT MAX(id) from keys""")[0][0]

    # Action vom Key abspeichern
    save_action(conn, key.action, id)


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


def save_view_action(conn, view_action, actionID):
    # View Action eintragen
    sql_insert_view_action = f"""INSERT INTO view_actions (view_name,deck_serial,action_id) VALUES("{view_action.view}","leer bis fix",{actionID});"""
    execute_sql(conn, sql_insert_view_action)


def save_mqtt_action(conn, mqtt_action, actionID):
    # MQTT Action eintragen
    sql_insert_mqtt_action = f"""INSERT INTO mqtt_actions (client,topic,payload,action_id) VALUES("{mqtt_action.client}","{mqtt_action.topic}","{mqtt_action.payload}",{actionID});"""
    execute_sql(conn, sql_insert_mqtt_action)

    # Die Unteratribute in weitere listen speichern
    for x in mqtt_action.icons:
        save_icons(conn, mqtt_action.icons[x], x, actionID)
    for x in mqtt_action.labels:
        save_labels(conn, mqtt_action.labels[x], x, actionID)
    for x in mqtt_action.colors:
        save_colors(conn, mqtt_action.colors[x], x, actionID)


def save_mqtt_toggle(conn, mqtt_toggle, actionID):
    # MQTT Toggle eintragen
    sql_insert_mqtt_toggle = f"""INSERT INTO mqtt_toggles (client,topic,payload,action_id) VALUES("{mqtt_toggle.client}","{mqtt_toggle.topic}","{mqtt_toggle.payload}",{actionID}); """
    execute_sql(conn, sql_insert_mqtt_toggle)

    # Die Unteratribute in weitere listen speichern
    for x in mqtt_toggle.icons:
        save_icons(conn, mqtt_toggle.icons[x], x, actionID)
    for x in mqtt_toggle.labels:
        save_labels(conn, mqtt_toggle.labels[x], x, actionID)
    for x in mqtt_toggle.colors:
        save_colors(conn, mqtt_toggle.colors[x], x, actionID)


def save_icons(conn, icon, state, actionID):
    # Icon Pfad und ihren dazu gehörigen Wert eintragen
    sql_insert_icons = f"""INSERT INTO dic_icons (icon,state,actions_id) VALUES("{icon}","{state}",{actionID});"""
    execute_sql(conn, sql_insert_icons)


def save_labels(conn, label, state, actionID):
    # Labelinhalt und ihren dazu gehörigen Wert eintragen
    sql_insert_labels = f"""INSERT INTO dic_labels (label,state,actions_id) VALUES("{label}","{state}",{actionID});"""
    execute_sql(conn, sql_insert_labels)


def save_colors(conn, color, state, actionID):
    # Farben und ihren dazu gehörigen Wert eintragen
    sql_insert_colors = f"""INSERT INTO dic_colors (hexvalue,state,actions_id) VALUES("{color}","{state}",{actionID});"""
    execute_sql(conn, sql_insert_colors)
