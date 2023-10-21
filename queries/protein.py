from .basequery import BaseQuery
from models.protein import Protein

class ProteinQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('protein', cursor)

    def insert(self, protein: Protein):
        query = f'INSERT INTO {self.table} (name, aminoacid_sequence) VALUES (%s, %s) RETURNING id'
        self.cursor.execute(query, (protein.name, protein.amino_acid_sequence))
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0]
    
    def get_id_by_name(self, prot_name: str):
        query = f'SELECT id FROM {self.table} WHERE name = %s'
        self.cursor.execute(query, (prot_name,))
        self.cursor.connection.commit()
        return self.cursor.fetchone()

#def get_alignment(self):    
