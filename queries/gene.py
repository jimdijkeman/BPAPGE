from .basequery import BaseQuery
from models.gene import Gene

class GeneQuery(BaseQuery):
    def __init__(self, table, cursor) -> None:
        super().__init__('gene', cursor)

    def insert(self, gene: Gene):
        query = f'INSERT INTO {self.table} (gene_name, nucleotide_sequence) VALUES (%s, %s) RETURNING id'
        self.cursor.execute(query, (gene.name, gene.nucleotide_sequence))
        self.cursor.connection.commit()
        return self.cursor.fetchone()[0]
    
    def get_id_by_name(self, gene_name: str):
        query = f'SELECT id FROM {self.table} WHERE gene_name = %s'
        self.cursor.execute(query, (gene_name,))
        self.cursor.connection.commit()
        return self.cursor.fetchone()