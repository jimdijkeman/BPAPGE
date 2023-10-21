from .basequery import BaseQuery
from models.protein_alignment import ProteinAlignment

class ProteinAlignmentQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('protein_alignment', cursor)

    def insert(self, protein_alignment: ProteinAlignment):
        query = f'INSERT INTO {self.table} (protein_id, alignment_id) VALUES (%s, %s)'
        self.cursor.execute(query, (protein_alignment.protein_id, protein_alignment.alignment_id))
        self.cursor.connection.commit()
