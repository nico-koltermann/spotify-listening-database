import sqlite3

def create_connection(db_file):
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
                    [history_stamp] string)
                ''')
                            
        conn.commit()
        print("Success! - DB Created")

    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    path_ws = os.path.dirname(os.path.abspath(__file__))
    create_connection(path_ws + "/../database/spotify.db")