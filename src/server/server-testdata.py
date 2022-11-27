from flask import Flask, json
import os
import datetime
import time

import sqlite3

api = Flask(__name__)

@api.route('/api/history', methods=['GET'])
def get_history():

    path_ws = os.path.dirname(os.path.abspath(__file__))
    conn = create_connection(path_ws + '/../database/spotify-data.db')

    history = select_all_history(conn)

    return json.dumps(history)


@api.route('/api/last_stamp', methods=['GET'])
def get_last_stamp():

    path_ws = os.path.dirname(os.path.abspath(__file__))
    conn = create_connection(path_ws + '/../database/spotify.db')

    sql = ''' SELECT MAX(history_stamp) FROM history; '''
    cur = conn.cursor()
    max_stamp = cur.execute(sql).fetchone()[0]

    print(max_stamp)

    return  str(datetime.datetime.utcfromtimestamp(max_stamp).strftime('%d.%m.%Y - %H:%M:%S'))


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    conn = sqlite3.connect(db_file)

    return conn


def select_all_history(conn):
    """
    Query all rows in the history table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM history")

    rows = cur.fetchall()

    return rows


if __name__ == '__main__':
    api.run()
