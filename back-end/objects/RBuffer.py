from utils.path_utils import to_unix
from sqlite3.dbapi2 import Connection
from utils.db_ops import *
from collections import defaultdict

INFLUENCE_TABLE_NAME = "influ_rel"


class RBuffer:
    """
    This class serves as a write-through in-memory cache to the database.
    We use Python dictionary as the underlying datastructure.
    """
    def __init__(self, db_conn: Connection, table_name: str):
        self.dict: dict[str, list] = dict()
        self.db_conn = db_conn
        self.table_name = table_name

    def contains(self, key: str):
        return to_unix(key) in self.dict

    def set(self, key: str, arr: list):
        self.dict[key] = arr

    def add(self, key: str, val):
        if key not in self.dict():
            self.dict[key] = []
        self.dict[key].append(val)

    def get(self, key: str):
        return self.dict.get(key)



class RInfluenceBuffer(RBuffer):
    """
    This class keeps track of meta data for calculated influence 
    It uses dict as underlining datastructure. Key is the influenced image path (path to a test image), and
    value is a list of source paths (paths to train images).
    """

    def __init__(self, db_conn: Connection):
        super(RInfluenceBuffer, self).__init__(db_conn, INFLUENCE_TABLE_NAME)

        # fill the cache
        values = db_select_all(self.db_conn, self.table_name)
        values.sort(key=lambda tup: (tup[0])) # group by 'path' field
        temp_dict = defaultdict(list)
        for path, source_path, order in values:
            temp_dict[path].append((order, source_path))
        for arr in temp_dict.values():
            arr.sort() # sort dictionary according to order
        
        # get rid of 'order' field in temp_dict
        self.dict = {key: [elem[1] for elem in arr] for key, arr in temp_dict.items()}
             

    def set(self, key: str, arr: list):
        # 1. push all values to database
        # 'order' is a keyword in sql, so wrapping it with square brackets.
        db_insert_many(self.db_conn, self.table_name, ('path', 'source_path', '[order]'), values=[(key, val, idx) for idx, val in enumerate(arr)])

        # 2. update buffer
        super().set(key, arr)

        # 3. commit
        self.db_conn.commit()


    def add(self, key: str, val):
        raise NotImplementedError






