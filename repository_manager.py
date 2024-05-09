import sqlite3
from datetime import datetime

DB_NAME = 'documents.db'

# Create the documents table
def create_documents_table():
    """ Connect to the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create the documents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            extension TEXT,
            owner TEXT,
            visibility TEXT,
            last_modified_date TEXT
        )
    ''')

     # Create the Historical table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historical (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            extension TEXT,
            owner TEXT,
            visibility TEXT,
            last_modified_date TEXT,
            date TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def insert_or_update_files(files):
    """ Insert or update the files in the database """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        for file in files:
            # Check if the file is public
            if file['visibility'] == "Público":
                # If the file is public insert in the historical
                insert_historical(cursor, file)
                        
                # Check if the file already exists in the database
            file_exist = verify_file_exist(cursor, file['file_name'])

            if file_exist:
                # If the file exists, update the file data
                cursor.execute("""
                    UPDATE documents
                    SET extension = ?, owner = ?, visibility = ?, last_modified_date = ?
                    WHERE id = ?
                """, (file['extension'], file['owner'], file['visibility'], file['last_modified_date'], file_exist[0]))
            else:
                # If the file does not exist, insert a new record in the database.
                cursor.execute("""
                    INSERT INTO documents (file_name, extension, owner, visibility, last_modified_date)
                    VALUES (?, ?, ?, ?, ?)
                """, (file['file_name'], file['extension'], file['owner'], file['visibility'], file['last_modified_date']))

        # Confirm the changes and close the connection.
        conn.commit()
        conn.close()

        print("Operación completada: Archivos insertados y actualizados correctamente.")
        
    except sqlite3.Error as e:
        print("Error al insertar o actualizar archivos en la base de datos:", e)

def verify_file_exist(cursor, file_name):
    """ Verify if the file already exists in the database """
    cursor.execute("SELECT file_name FROM documents WHERE file_name = ?", (file_name,))
    file_exist = cursor.fetchone()
    return file_exist

def insert_historical(cursor, file):
    """ Insert the file in the historical table"""
    cursor.execute("SELECT file_name FROM historical WHERE file_name = ?", (file['file_name'],))
    file_exist = cursor.fetchone()
    if file_exist:
        cursor.execute("""
        UPDATE historical
        SET date = ?
        WHERE file_name = ?
        """, (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file['file_name']))
    else:
         # Execute the SQL query to insert into the historical table
        cursor.execute("""
        INSERT INTO historical (file_name, extension, owner, visibility, last_modified_date, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (file['file_name'], file['extension'], file['owner'], file['visibility'], file['last_modified_date'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))   