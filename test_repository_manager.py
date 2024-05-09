import sqlite3
import pytest
from repository_manager import create_documents_table, verify_file_exist

@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(":memory:")
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
    
    yield conn
    conn.close()

def test_create_documents_table(in_memory_db):
    # Arrange
    cursor = in_memory_db.cursor()

    # Act
    create_documents_table()

    # Assert
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents'")
    result = cursor.fetchone()
    assert result is not None

    cursor.execute("PRAGMA table_info(documents)")
    columns = cursor.fetchall()
    assert len(columns) == 6

    expected_columns = [
        ("id", "INTEGER", 0, None, 1),
        ("file_name", "TEXT", 0, None, 0),
        ("extension", "TEXT", 0, None, 0),
        ("owner", "TEXT", 0, None, 0),
        ("visibility", "TEXT", 0, None, 0),
        ("last_modified_date", "TEXT", 0, None, 0)
    ]
    

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='historical'")
    result = cursor.fetchone()
    assert result is not None

    cursor.execute("PRAGMA table_info(historical)")
    columns = cursor.fetchall()
    assert len(columns) == 7

    expected_columns = [
        ("id", "INTEGER", 0, None, 1),
        ("file_name", "TEXT", 0, None, 0),
        ("extension", "TEXT", 0, None, 0),
        ("owner", "TEXT", 0, None, 0),
        ("visibility", "TEXT", 0, None, 0),
        ("last_modified_date", "TEXT", 0, None, 0),
        ("date", "TEXT", 0, None, 0)
    ]

    # Arrange
    cursor = in_memory_db.cursor()

    # Act
    create_documents_table()

    # Assert
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents'")
    result = cursor.fetchone()
    assert result is not None

    cursor.execute("PRAGMA table_info(documents)")
    columns = cursor.fetchall()
    assert len(columns) == 6

    expected_columns = [
        ("id", "INTEGER", 0, None, 1),
        ("file_name", "TEXT", 0, None, 0),
        ("extension", "TEXT", 0, None, 0),
        ("owner", "TEXT", 0, None, 0),
        ("visibility", "TEXT", 0, None, 0),
        ("last_modified_date", "TEXT", 0, None, 0)
    ]
    

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='historical'")
    result = cursor.fetchone()
    assert result is not None

    cursor.execute("PRAGMA table_info(historical)")
    columns = cursor.fetchall()
    assert len(columns) == 7

    expected_columns = [
        ("id", "INTEGER", 0, None, 1),
        ("file_name", "TEXT", 0, None, 0),
        ("extension", "TEXT", 0, None, 0),
        ("owner", "TEXT", 0, None, 0),
        ("visibility", "TEXT", 0, None, 0),
        ("last_modified_date", "TEXT", 0, None, 0),
        ("date", "TEXT", 0, None, 0)
    ]


def test_verify_file_exist(in_memory_db):
    # Arrange
    cursor = in_memory_db.cursor()
    create_documents_table()
    file_name = "test_file.txt"

    # Act
    file_exist = verify_file_exist(cursor, file_name)

    # Assert
    assert file_exist is None

    # Add a file to the database
    cursor.execute("INSERT INTO documents (file_name) VALUES (?)", (file_name,))
    in_memory_db.commit()

    # Act again
    file_exist = verify_file_exist(cursor, file_name)

    # Assert again
    assert file_exist == (file_name,)

    # Add another file to the database
    cursor.execute("INSERT INTO documents (file_name) VALUES (?)", ("another_file.txt",))
    in_memory_db.commit()

    # Act again
    file_exist = verify_file_exist(cursor, file_name)

    # Assert again
    assert file_exist == (file_name,)