from typing import List, Tuple
from sqlite3.dbapi2 import Cursor, Connection

# Note: commit should be done by the caller after flushing in-memory buffer 
# to ensure consistency!

def db_insert(db_conn: Connection, table_name: str, keys: Tuple[str], values: Tuple[str]):
    assert(len(keys) == len(values)), "key and value array length not equal"

    db_cursor = db_conn.cursor()
    template = "INSERT INTO {} ({}) values ({})".format(
        table_name,
        ",".join(keys),
        ",".join(["?" for _ in values])
    )
    
    db_cursor.execute(template, values)
    

def db_insert_many(db_conn: Connection, table_name: str, keys: Tuple[str], values: List[Tuple[str]]):
    assert(len(keys) == len(values)), "key and value array length not equal"

    db_cursor = db_conn.cursor()
    template = "INSERT INTO {} ({}) values ({})".format(
        table_name,
        ",".join(keys),
        ",".join(["?" for _ in values])
    )
    
    db_cursor.executemany(template, values)
 


def db_select_by_path(db_conn: Connection, table_name: str, path: str) -> List[Tuple]:

    db_cursor = db_conn.cursor()
    template = "SELECT * from {} WHERE path=?".format(
        table_name,
    )

    db_cursor.execute(template, (path,))
    return db_cursor.fetchall()


def db_update_by_path(db_conn: Connection, table_name: str, path: str, keys: Tuple[str], values: Tuple[str]):
    assert(len(keys) == len(values)), "key and value array length not equal"
    db_cursor = db_conn.cursor()

    template = "UPDATE {} SET {} WHERE path=?".format(
        table_name,
        ",".join(["{} = ?".format(key) for key in keys])
    )

    db_cursor.execute(template, values + (path,))
   

def db_delete_by_path(db_conn: Connection, table_name: str, path: str):
    db_cursor = db_conn.cursor()

    template = "DELETE FROM {} WHERE path=?".format(
        table_name
    )

    db_cursor.execute(template, (path,))


def db_delete_all(db_conn: Connection, table_name: str):
    db_cursor = db_conn.cursor()

    template = "DELETE FROM {}".format(
        table_name
    )

    db_cursor.execute(template)



def db_count_all(db_conn: Connection, table_name: str):
    db_cursor = db_conn.cursor()

    template = "SELECT COUNT (*) FROM {}".format(
        table_name
    )

    db_cursor.execute(template)
    return db_cursor.fetchone()[0]


## TODO: paging here


