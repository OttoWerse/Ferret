import sqlite3
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

        return cur.fetchall()
    except Error as e:
        print(e)

def create_tables(db_file):
    """
    Erstellen einer Datenbank mit Tabellen zum Speichern für ausfälle
    :param db_file:
    """

    # View Tabelle
    sql_create_views_table = """ CREATE TABLE IF NOT EXISTS views (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """

    # Deck Tabelle
    sql_create_decks_table = """ CREATE TABLE IF NOT EXISTS decks (
                                                id integer PRIMARY KEY,
                                                name text,
                                                current_view_id integer,
                                                FOREIGN KEY (current_view_id) REFERENCES views (id)
                                            ); """

    # Key Tabelle
    sql_create_keys_table = """CREATE TABLE IF NOT EXISTS keys (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    icon_path text,
                                    label text,
                                    view_id integer MOT NULL,
                                    FOREIGN KEY (view_id) REFERENCES views (id)
                                );"""

    # Actions

    # Action Tabelle
    sql_create_actions_table = """ CREATE TABLE IF NOT EXISTS actions (
                                            id integer PRIMARY KEY
                                        ); """

    # MQTT-Action Tabelle
    sql_create_mqtt_action_table = """ CREATE TABLE IF NOT EXISTS mqtt_actions (
                                            id integer PRIMARY KEY,
                                            client text NOT NULL,
                                            topic text NOT NULL,
                                            payload text NOT NULL,
                                            action_id integer NOT NULL,
                                            FOREIGN KEY (action_id) REFERENCES actions (id)
                                        ); """

    # View_Action Tabelle
    sql_create_view_action_table = """ CREATE TABLE IF NOT EXISTS view_actions (
                                            id integer PRIMARY KEY,
                                            view_id integer NOT NULL,
                                            action_id integer NOT NULL,
                                            FOREIGN KEY (view_id) REFERENCES views (id),
                                            FOREIGN KEY (action_id) REFERENCES actions (id)
                                        ); """

    # DICS

    # DIC-Icons Tabelle
    sql_create_dic_icons_table = """ CREATE TABLE IF NOT EXISTS  dic_icons (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                icon text NOT NULL,
                                                mqtt_actions_id NOT NULL,
                                                FOREIGN KEY (mqtt_actions_id) REFERENCES mqtt_actions (id)
                                            ); """

    # DIC_Labels Tabelle
    sql_create_dic_labels_table = """ CREATE TABLE IF NOT EXISTS  dic_labels (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                label text NOT NULL,
                                                mqtt_actions_id integer NOT NULL,
                                                FOREIGN KEY (mqtt_actions_id) REFERENCES mqtt_actions (id)
                                            ); """

    # DIC_Colors Tabelle
    sql_create_dic_colors_table = """ CREATE TABLE IF NOT EXISTS  dic_colors (
                                                    id integer PRIMARY KEY,
                                                    name text NOT NULL,
                                                    hexvalue text NOT NULL,
                                                    mqtt_actions_id integer NOT NULL,
                                                    FOREIGN KEY (mqtt_actions_id) REFERENCES mqtt_actions (id)
                                                ); """

    # DB Verbindung aufbauen
    conn = create_connection(db_file)

    # Tabellen erstellen
    execute_sql(conn,sql_create_decks_table)
    execute_sql(conn,sql_create_views_table)
    execute_sql(conn,sql_create_keys_table)

    execute_sql(conn,sql_create_actions_table)
    execute_sql(conn,sql_create_mqtt_action_table)
    execute_sql(conn,sql_create_view_action_table)

    execute_sql(conn,sql_create_dic_icons_table)
    execute_sql(conn,sql_create_dic_labels_table)
    execute_sql(conn,sql_create_dic_colors_table)


if __name__ == "__main__" :
    create_tables("data.db")


def save_view(view):

    sql_insert_view = f"""INSERT INTO views (name)
                                VALUES({view.name});  
                                """
    execute_sql(sql_insert_view)



    for e in execute_sql("""SELECT MAX(id) from views"""):
        id = e



    for key in view.keys:
        sql_insert_keys = f"""INSERT INTO keys (name, icon_path, label, view_id)
                                VALUES({key.name},{key.image},{key.label},{id})
                                """
        execute_sql(sql_insert_keys)