import sqlite3

def create_db(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        
        c = conn.cursor()

        c.execute('''
                CREATE TABLE IF NOT EXISTS history
                ([history_id] INTEGER PRIMARY KEY, 
                    [artist] string, 
                    [song] string, 
                    [history_entry] string, 
                    [history_stamp] string,
                    [ms_played] string)
                ''')
                            
        conn.commit()
        print("Success! - DB Created")

    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    conn = sqlite3.connect(db_file)

    return conn

def get_last_timestamp(conn):
    """ Get latest timesstamp from db
    :param db_file: database file
    :return: Connection object or None
    """

    sql = ''' SELECT MAX(history_stamp) FROM history; '''
    cur = conn.cursor()
    max_stamp = cur.execute(sql).fetchone()[0]
    return max_stamp
    
def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO history(artist, song, history_entry, history_stamp, ms_played)
              VALUES(?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    
    return cur.lastrowid


if __name__ == "__main__":
    path_ws = os.path.dirname(os.path.abspath(__file__))
    create_db(path_ws + "/../database/spotify.db")