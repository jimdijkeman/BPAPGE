from connection import Connection


with Connection.connect_from_ini_config() as (conn, curr):
    print(conn)