import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ Erstellt die Datenbank """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def tables(db_file):
    """
    Erstellen einer Datenbank mit Tabellen zum Speichern für ausfälle
    :param db_file:
    """

    #Deck Tabelle
    sql_create_views_table = """ CREATE TABLE IF NOT EXISTS views (
                                            id integer PRIMARY KEY,
                                            name text,
                                            FOREIGN KEY (view_id) REFERENCES views (id)
                                        ); """

    #View Tabelle
    sql_create_views_table = """ CREATE TABLE IF NOT EXISTS views (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                    ); """

    #Key Tabelle
    sql_create_keys_table = """CREATE TABLE IF NOT EXISTS keys (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    icon_path text,
                                    label text,
                                    FOREIGN KEY (view_id) REFERENCES views (id)
                                );"""


    #Actions

    #Action Tabelle
    sql_create_actions_table = """ CREATE TABLE IF NOT EXISTS actions (
                                            id integer PRIMARY KEY
                                        ); """


    #MQTT-Action Tabelle
    sql_create_mqtt_action_table = """ CREATE TABLE IF NOT EXISTS mqtt_actions (
                                            id integer PRIMARY KEY,
                                            client text NOT NULL,
                                            topic text NOT NULL,
                                            payload text NOT NULL,
                                            FOREIGN KEY (action_id) REFERENCES actions (id)
                                        ); """

    #View_Action Tabelle
    sql_create_view_action_table = """ CREATE TABLE IF NOT EXISTS actions (
                                            id integer PRIMARY KEY,
                                            FOREIGN KEY (view_id) REFERENCES views (id)
                                            FOREIGN KEY (actions_id) REFERENCES actions (id)
                                        ); """


    #DICS

    #DIC-Icons Tabelle
    sql_create_dic_icons_table = """ CREATE TABLE IF NOT EXISTS  dic_icons (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                FOREIGN KEY (mqtt-actions_id) REFERENCES mqtt_actions (id),
                                                icon text NOT NULL
                                            ); """

    #DIC_Labels Tabelle
    sql_create_dic_icons_table = """ CREATE TABLE IF NOT EXISTS  dic_icons (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                FOREIGN KEY (mqtt-actions_id) REFERENCES mqtt_actions (id),
                                                label text NOT NULL
                                            ); """

    # DIC_Colors Tabelle
    sql_create_dic_colors_table = """ CREATE TABLE IF NOT EXISTS  dic_colors (
                                                    id integer PRIMARY KEY,
                                                    name text NOT NULL,
                                                    FOREIGN KEY (mqtt-actions_id) REFERENCES mqtt_actions (id),
                                                    hexvalue text NOT NULL
                                                ); """

