from crypt import methods
import sqlite3

# Conecion de la Base de Datos

def connection():
    conn = sqlite3.connect('./db/AEdb.db')
    conn.row_factory = sqlite3.Row
    return conn