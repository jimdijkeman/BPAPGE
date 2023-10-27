from .basequery import BaseQuery
from models.function import Function

class FunctionQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('function', cursor)

    def insert(self, function: Function):
        query = f'INSERT INTO {self.table} (description, protein_id) VALUES (%s, %s) RETURNING id'
        self.cursor.execute(query, (function.description, function.protein_id))
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0] 
