from .basequery import BaseQuery

class ProteinPathwayQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('protein_pathway', cursor)

    def insert(self, protein_id, pathway_id):
        query = f'INSERT INTO {self.table} (protein_id, pathway_id) VALUES (%s, %s) RETURNING id'
        self.cursor.execute(query, (protein_id, pathway_id))
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0] 
