from configparser import ConfigParser
import psycopg2

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

class Connection:

    def __init__(self, conn):
        self.conn = conn

    @staticmethod
    def connect_from_ini_config():
        params = config('database.ini', 'postgresql')
        conn = psycopg2.connect(**params)
        print("Connecting to database...")
        return Connection(conn)

    def __enter__(self):
        self.cursor = self.conn.cursor()
        return self.cursor, self.conn
    
    def __exit__(self, exc_type, exc_value, exec_traceback):
        self.cursor.close()
        self.conn.commit()
        print('Changes commited to database...')
        self.conn.close()
        print('Database connection closed...')
