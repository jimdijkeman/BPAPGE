from .basequery import BaseQuery

class PathwayQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('pathway', cursor)

    def insert(self, name, description):
        query = f'INSERT INTO {self.table} (name, description) VALUES (%s, %s) RETURNING id'
        self.cursor.execute(query, (name, description))
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0]

    def get_by_kegg_id(self, kegg_id):
        query = f'SELECT * FROM {self.table} WHERE name = %s'
        self.cursor.execute(query, (kegg_id,))
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0]
