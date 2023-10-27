from configparser import ConfigParser
import psycopg2

def config(filename='database.ini', section='postgresql'):
    """
    Read database configuration file and return a dictionary of database parameters.

    Parameters:
    filename (str): The name of the configuration file. Default is 'database.ini'.
    section (str): The section of the database configuration. Default is 'postgresql'.

    Returns:
    dict: A dictionary containing the database parameters.
    """
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
    """
    Context manager class for database connections.

    This class creates a database connection and is used with a 'with' statement.
    It commits and closes the connection upon exiting the 'with' block.
    """
    def __init__(self, conn):
        """
        Initialize the Connection object.

        Parameters:
        conn (obj): A psycopg2 connection object.
        """
        self.conn = conn

    @staticmethod
    def connect_from_ini_config():
        """
        Create a database connection using parameters from a configuration file.

        Returns:
        Connection: A Connection object.
        """
        params = config('database.ini', 'postgresql')
        conn = psycopg2.connect(**params)
        print("Connecting to database...")
        return Connection(conn)

    def __enter__(self):
        """
        Enter the runtime context related to this object.

        Returns:
        tuple: A tuple containing a psycopg2 cursor and connection object.
        """
        self.cursor = self.conn.cursor()
        return self.cursor, self.conn

    def __exit__(self, exc_type, exc_value, exec_traceback):
        """
        Exit the runtime context related to this object.

        Closes the cursor, commits any changes, and closes the connection.
        """
        self.cursor.close()
        self.conn.commit()
        print('Changes commited to database...')
        self.conn.close()
        print('Database connection closed...')
