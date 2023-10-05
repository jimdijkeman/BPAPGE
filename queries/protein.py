from .basequery import BaseQuery

class ProteinQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('protein', cursor)

    def insert(self, values: tuple):
        query = f'INSERT INTO {self.table} (name, aminoacid_sequence, gene_id) VALUES (%s, %s, %s) RETURNING id'
        self.cursor.execute(query, values)
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0]
